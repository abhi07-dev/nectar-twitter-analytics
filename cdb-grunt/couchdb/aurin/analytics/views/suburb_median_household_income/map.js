function(doc) {
    emit(doc.suburb, [doc.median_household_income,1]);
}
