/**
 * 数据库连接操作
 */
var dbpool = require("../dbpool") 


async function tes6t(){
    sql = 'select count(*) as allCount from Repurchase'
    let rows = await dbpool.query(sql);
    console.log(sql);
    console.log(rows)
    
    console.log(rows[0].allCount);
    console.log(rows.length)
    sql = 'select * from Repurchase limit 10';
    let values = await  dbpool.query(sql);
    let len = values.length
    let result = []
    for( i = 0; i < len; i++){
        console.log(values[i]);
        result[i] = values[i]
    }
    console.log(JSON.stringify(values))
    console.log(result)
    //console.log(values);
    console.log("end...")
 }
 
 tes6t().then(result=>{
     console.log("test success"); 

 });
