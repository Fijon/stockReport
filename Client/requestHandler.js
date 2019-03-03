/**
 * 所有请求的处理方法
 */
var fs = require('fs');
var db = require('./dbpool.js');
var myUtils = require('./utils')

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
            console.log('error.....');
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
 * 读取购物信息
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
            //error_Req(res, 'error_param', '不支持该参数查询');
        }
    }
    query_dto.pageSize = pageSize
    query_dto.startRow = (page - 1) * pageSize
    if (myUtils.isEmptyObject(query_dto.code)) {
        sql_str = 'select * from Repurchase order by tradingDate desc limit ?, ?'
        result = await db.query(sql_str, [query_dto.startRow, query_dto.pageSize])
        res.end(JSON.stringify(result));
    } else {
        try {
            if (page == 0) {
                page = 1;
            }
            query_dto.startRow = (page - 1) * pageSize;
            query_dto.pageSize = pageSize;
            sql_str = 'select * from Repurchase where code=? order by tradingDate desc limit ?, ?'
            result = await db.query(sql_str, [query_dto.code, query_dto.startRow, query_dto.pageSize])
            res.end(JSON.stringify(result));
        } catch (error) {
            console.error('query db has error');
            console.log(error);
            error_Req(res, 'error_query_db', '查询数据库异常')
        }
    }


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