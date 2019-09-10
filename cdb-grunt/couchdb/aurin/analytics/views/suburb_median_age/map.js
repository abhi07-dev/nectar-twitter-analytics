function(doc) {
    emit(doc.suburb, [doc.median_age,1]);
}
