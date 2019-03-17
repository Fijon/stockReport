/**
 * 请求返回的基础对象
 */
class BaseResult{
    
    constructor(code,msg,data){
        this.code = code;
        this.msg = msg;
        this.data = data;
    }
    setCode(code){
        this.code = code;
    }
    getCode(){
        return this.code;
    }
    setMsg(msg){
        this.msg = msg;
    }
    getMsg(){
        return this.msg;
    }
    setData(data){
        this.data = data;
    }
    getData(){
        return this.data;
    }
    getRes(){
        return {'code':this.code,'msg':this.msg,'data':this.data};
    }
};

class BasePage extends BaseResult{ 
    constructor(code,msg,data, toPage, count){
        super(code, msg, data);
        this.toPage = toPage;
        this.count = count;
        this.allPage = count / pageSize + 1;
    }

    getPageSize(){
        return this.pageSize;
    }
    setPageSize(pageSize){
        this.pageSize  = pageSize;
    }
    getToPage(){
        return this.toPage;
    }
    setToPage(toPage){
        this.toPage = toPage;
    }
};


module.exports = {
    // 通用
    SUCCESS                 :       new BaseResult(0,'成功',{}),
    FAILED                  :       new BaseResult(1,'失败',{}),
    //用户
    USER_PASSWORD_ERROR     :       new BaseResult(101,'用户名或密码错误',{}),
    USER_CAPTCHA_ERROR      :       new BaseResult(102,'验证码错误',{}),
    PageResult              :       new BaseResult(0, '成功', {})
};
module.exports = BasePage;
module.exports = BaseResult;

