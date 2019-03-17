/**
 * 所有请求的处理方法
 */
var fs = require('fs');
var db = require('./dbpool.js');
var myUtils = require('./utils');
var result = require("./domain/Base.class");

/**
 * 错误请求的处理方法
 * @param {*} response 
 * @param {*} code 
 * @param {*} msg 
 */
function error_Req(response, code, msg) {
    var body = '<html lang="zh-CN"> ' +
        '<head>' +
        ' <meta charset="utf-8">' +
        '<meta http-equiv-"Content-Type" content="text/html;charset=UTF-8"/>' +
        '</head>' +
        '<body>' +
        '<div> ' + msg + '</div>' +
        '</body>' +
        '</html>';
    response.writeHead(200, { "Content-Type": "text/html" });
    //当Content-Type为"text/plain"时，返回的内容将直接显示
    response.write(body);
    response.end();
}

/**
 * 读取静态资源对象
 * @param {*} res 
 * @param {*} data 
 * @param {*} url_path 
 */
function readStatic(res, data, url_path) {

    fs.readFile(url_path, 'utf-8', function (err, data) {
        if (err) {
            console.log('error.....' + data);
            console.log(err)
            res.end();
        } else {
            console.log("read url_path, " + url_path)
            //console.log(data)
            res.write(data)
            res.end();
        }
    });
}

/**
 * 读取回购信息
 * @param {*} res 
 * @param {*} data 
 * @param {*} param 
 */
async function queryBuyReport(res, data, param) {
    length = param.length;
    var query_dto = {};
    var startRow = 0;
    var page = 1;
    var pageSize = 10;
    for (idx = 0; idx < length; idx++) {
        tmp_array = param[idx].split('=');
        if (tmp_array.length != 2) {
            console.error("param is not correct, " + param[idx]);
            continue;
        }
        if (tmp_array[0] === 'code') {
            query_dto.code = tmp_array[1];
        } else if ('name' === tmp_array[0]) {
            query_dto.name = tmp_array[1]
        } else if ('page' === tmp_array[0]) {
            page = parseInt(tmp_array[1]);
        } else if ('pageSize' === tmp_array[0]) {
            pageSize = parseInt(tmp_array[1])
        }
        else {
            console.error('param could not be : ' + tmp_array[0] + ', value: ' + tmp_array[1]);
        }
    }
    query_dto.pageSize = pageSize
    query_dto.startRow = (page - 1) * pageSize
    query_dto.page = page
    console.log(query_dto)
    if (myUtils.isEmptyObject(query_dto.code)) {
        let sql_str = 'select * from Repurchase order by tradingDate desc limit ?, ?'
        let result = await db.query(sql_str, [query_dto.startRow, query_dto.pageSize])
        let sql_count = 'select count(*) as allCount from Repurchase order by tradingDate desc '
        let result_count = await db.query(sql_count, [query_dto.startRow, query_dto.pageSize]) 
        console.log(JSON.stringify(result_count));
        console.log(JSON.stringify(result))
        const pageResult = {}; 
        pageResult.pageSize = query_dto.pageSize
        pageResult.allPage =  result_count[0].allCount / pageSize
        pageResult.allCount = result_count[0].allCount
        pageResult.nowPage = page
        pageResult.data = JSON.parse(JSON.stringify(result))
        pageResult.code = 0
        pageResult.msg = "success"
        console.log(pageResult)
        //res.end(JSON.stringify(pageResult));
        generateResult(query_dto, result,result_count[0].allCount, res)
    } else {
        try {
            if (page == 0) {
                page = 1;
            }
            query_dto.startRow = (page - 1) * pageSize;
            query_dto.pageSize = pageSize;
            
            let sql_str = 'select * from Repurchase where code=? order by tradingDate desc limit ?, ?'
            let result = await db.query(sql_str, [query_dto.code, query_dto.startRow, query_dto.pageSize])
            let sql_count = 'select count(*) as allCount from Repurchase where code=?'
            let result_count = await db.query(sql_str, [query_dto.code])
            
            console.log(JSON.stringify(result))
            //res.end(JSON.stringify(result));
            generateResult(query_dto, result,result_count[0].allCount, res)
        } catch (error) {
            console.error('query db has error');
            console.log(error);
            error_Req(res, 'error_query_db', '查询数据库异常')
        }
    }
}

/**
 * 将数据生成翻页数据返回
 * @param {*} pageSize 
 * @param {*} page 
 * @param {*} result 
 * @param {*} resultCount 
 * @param {*} response 
 */
function generateResult(query_dto, result, resultCount, response){
    const pageResult = {}; 
    pageResult.pageSize = query_dto.pageSize
    pageResult.allCount = resultCount
    pageResult.pageAmount =   Math.ceil(resultCount / query_dto.pageSize)
    pageResult.cur = query_dto.page
    pageResult.data = JSON.parse(JSON.stringify(result))
    pageResult.code = 0
    pageResult.msg = "success"
    response.end(JSON.stringify(pageResult))
}

function one(response, data) {
    var body = '<html>' +
        '<head>' +
        '<meta charset="UTF-8"/>' +
        '<meta http-equiv-"Content-Type" content="text/html;charset=UTF-8"/>' +
        '</head>' +
        '<body>' +
        '<a href="/two">two</a>' +
        '</body>' +
        '</html>';

    response.writeHead(200, { "Content-Type": "text/html;charset=utf-8" });
    //当Content-Type为"text/plain"时，返回的内容将直接显示
    response.write(body);
    response.end();
}
function two(response, data) {
    var body = '<html>' +
        '<head>' +
        '<meta http-equiv-"Content-Type" content="text/html;charset=UTF-8"/>' +
        '</head>' +
        '<body>' +
        '<a href="/one">one</a>' +
        '</body>' +
        '</html>';

    response.writeHead(200, { "Content-Type": "text/html" });
    response.write(body);
    response.end();
}
exports.readStatic = readStatic;
exports.queryReport = queryBuyReport;
exports.one = one;
exports.two = two;