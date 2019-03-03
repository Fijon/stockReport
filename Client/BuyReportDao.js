/**
 * 查询回购信息的数据接口
 */

var db = require('./newDB.js')

const reportDao = {
    "data":{},
    "result":true,
    "code":0,
    "msg":"",
    "page":1,
    "pageSize":10,
    "count":0
};

/**
 * 翻页查询数据
 * 返回结构格式
 */
async function queryBuyReport(){
    sql = 'select count(*) from Repurchase'
    let rows = await query(sql);
    console.log(sql);
    console.log(rows);
    sql = 'select * from Repurchase limit 10';
    let values = await query(sql);
    console.log(values);
 }
