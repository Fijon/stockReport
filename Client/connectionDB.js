var db = require('mysql');
var str_format = require('string.format');
const MYSQL_ENV = { host: 'mysql.sql122.cdncenter.net', port: 3306, user: 'sq_Fijon', password: 'Fijon920630', database: 'sq_Fijon' }


var connection;

sql = "select * from Repurchase order by tradingDate desc limit 10"
sql_count_with_param = 'select count(*) from Repurchase where code=\'{code}\' '
sql_param = 'select * from Repurchase where code=\'{code}\' order by tradingDate desc limit {startRow}, {pageSize}'

var query = function (sql, values) {
    // 返回一个 Promise
    return new Promise((resolve, reject) => {
        pool.getConnection(function (err, connection) {
            if (err) {
                reject(err)
            } else {
                connection.query(sql, values, (err, rows) => {

                    if (err) {
                        reject(err)
                    } else {
                        resolve(rows)
                    }
                    // 结束会话
                    connection.release()
                })
            }
        })
    })
}


function handleDisconnection() {
    var conn = db.createConnection(MYSQL_ENV);
    conn.connect(function (err) {
        if (err) {
            setTimeout('handleDisconnection()', 2000);
        }
    });

    conn.on('error', function (err) {
        console.error('db error', err);
        if (err.code === 'PROTOCOL_CONNECTION_LOST') {
            console.error('db error执行重连:' + err.message);
            handleDisconnection();
        } else {
            throw err;
        }
    });
    return conn;
}

function querySqlWithParam(response, param) {
    connection = handleDisconnection();
    query_sql = sql_param.format(param);
    console.log("query sql: " + query_sql)
    connection.query(query_sql, function (err, rows, fields) {
        if (err) throw err;
        len = rows.length;
        result = JSON.stringify(rows);
        console.log("query result:  " + result.length)
        response.end(result);
        connection.end();
    });
}

function querysql(response) {
    connection = handleDisconnection();
    connection.query(sql, function (err, rows, fields) {
        if (err) throw err;
        len = rows.length;
        result = JSON.stringify(rows);
        console.log("query result:  " + result.length)
        response.end(result);
        connection.end();
    });
}

exports.querysql = querysql;
exports.querySqlWithParam = querySqlWithParam;
