import React from 'react';
import Polygon from "react-google-maps";


const SuburbMultiPolygon = ({suburb}) => {
    return (
        <React.Fragment>
            {suburb.polygons.map((polygon, index) => {
                return (
                    <Polygon
                        key={suburb.suburbName + '-' + index}
                        paths={polygon}
                        options={happyStyle}
                    />
                );
            })}
        </React.Fragment>
    );
}

export default SuburbMultiPolygon;