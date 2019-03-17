var http = require("http");
var url = require("url");
var requestHandler = require('./requestHandler')
var myUtils = require('./utils')

function start(route, handle) {
    function onRequest(request, response) {
        console.log(request.url)
        req_obj = url.parse(request.url);
        var pathname = req_obj.pathname;
        var postData = '';
        if (pathname.endsWith('js')) {
            pathname = pathname.slice(1, pathname.length)
            response.writeHead(200, { "Content-Type": "text/js" });

            requestHandler.readStatic(response, postData, pathname);
        } else if (pathname.endsWith('css')) {
            pathname = pathname.slice(1, pathname.length)
            response.writeHead(200, { "Content-Type": "text/css" });
            requestHandler.readStatic(response, postData, pathname);
        } else if (pathname.endsWith('html')) {
            idx = pathname.lastIndexOf('/');
            pathname = 'resource/html/' + pathname.slice(idx + 1, pathname.length);
            response.writeHead(200, { "Content-Type": "text/html" });
            requestHandler.readStatic(response, postData, pathname);
        } else if (pathname.endsWith('json')) {
            search_str = req_obj.search;
            param = []
            if (myUtils.isEmptyObject(search_str)) {
                param = []
            } else {
                param = req_obj.search.slice(1, req_obj.search.length).split('&');
            }
            response.writeHead(200, { "Content-Type": "text/json" });
            console.log("query with param: " + param)
            requestHandler.queryReport(response, postData, param)
        }
        else {
            route(handle, pathname, response, postData);
        }
    }
    http.createServer(onRequest).listen(8888);
}

exports.start = start;