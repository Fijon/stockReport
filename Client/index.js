/** 项目主页 */

var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandler");

var handle = {};
handle["/"] = requestHandlers.one;
handle["/one"] = requestHandlers.one;
handle["/two"] = requestHandlers.two;

server.start(router.route, handle);
console.log("start.....")