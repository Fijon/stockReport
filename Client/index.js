/** 项目主页 */

var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandler");

var handle = {};

server.start(router.route, handle);
console.log("start.....")