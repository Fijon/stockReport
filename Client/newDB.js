/**
 * 数据库连接操作
 */

 var mysql = require("mysql");
 const MYSQL_ENV = { host: 'mysql.sql122.cdncenter.net', port: 3306, user: 'sq_Fijon', password: '*******', database: 'sq_Fijon' };
 var pool = mysql.createPool(MYSQL_ENV);

 let query = function(sql, values){
     return new Promise((resolve, reject) =>{
        pool.getConnection(function(err, connection){
            if(err){
                reject(err);
            }else{
                connection.query(sql, values, (err, rows) =>{
                    if(err){
                        reject(err);
                    }else{
                        resolve(rows);
                    }
                    connection.release();
                });
            }
        })
     });
 }



async function tes6t(){
    sql = 'select count(*) from Repurchase'
    let rows = await query(sql);
    console.log(sql);
    console.log(rows);
    sql = 'select * from Repurchase limit 10';
    let values = await query(sql);
    console.log(values);
 }



 tes6t().then(result=>{
     console.log(result)
 });
