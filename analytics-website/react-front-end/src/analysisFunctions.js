import regression from 'regression';

export const extractCoordinates = (predictorSet, responseSet) => {
    let coords = predictorSet.map((ps) => {
        let rs = responseSet.find((suburb) => ps.key === suburb.key);
        if (rs) {
            let score1 = ps.value;
            let score2 = rs.value;
            return ([score1, score2]);
        }
    }).filter((x) => x);
    return coords;
}

export const suburbRegression = (predictorSet, responseSet) => {
    let coords = extractCoordinates(predictorSet, responseSet);
    console.log(coords);
    return regression.linear(coords);
}