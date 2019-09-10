function(doc) {
    if (doc.text && doc.username && doc.created_at && doc.coordinates) {
        emit(doc.created_at, {
            username: doc.username,
            tweet: doc.text,
            location: doc.coordinates
        });
    }
}