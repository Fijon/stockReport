function isEmptyObject(obj) {
    for (var tmp in obj) {
        return false;
    }
    return true;
}

exports.isEmptyObject = isEmptyObject;