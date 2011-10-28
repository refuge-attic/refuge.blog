function(doc) {
    if(doc.type && doc.type == "post") {
        emit(doc.created_at, doc);
    }
}