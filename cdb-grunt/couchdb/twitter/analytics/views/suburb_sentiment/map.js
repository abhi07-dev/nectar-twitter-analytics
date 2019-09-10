function(doc) {
    if (doc.suburb && 
        doc.score) {
        emit(doc.suburb, doc.score);
    }
}