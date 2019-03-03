/**
 * 请求返回的基础对象
 */
class Base{
    constructor(data, msg, code){
        this.data = data;
        this.msg = msg;
        this.code = code;
    }

    toString(){
        return "(data: "this.data + ", msg: " + this.msg + ", code: " + this.code  + ")";
    }

}
module.exports = Base;