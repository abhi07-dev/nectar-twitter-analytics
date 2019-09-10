import React from 'react';
import { sprintf } from 'sprintf-js';
import { 
    withScriptjs,
    withGoogleMap, 
    GoogleMap, 
    Polygon,
} from "react-google-maps";

const melbCenter = { 
    lat: -37.8, 
    lng: 145.0 
};

const grayScaleFilter = [
    {
        featureType: "all",
        elementType: "all",
        stylers: [
            { saturation: -100 }
        ]
    }
];

// polygon styles
const polygonStyle = {
    strokeColor: 'black',
    strokeOpacity: 1,
    strokeWeight: 0.5,
    fillColor: 'rgb(255, 0, 0)',
    fillOpacity: 0.8
};

const interpolateColour = (lowColour, hiColour, mix) => {
    let intColour = [0, 0, 0];
    intColour[0] = lowColour[0]*(1 - mix) + hiColour[0]*mix;
    intColour[1] = lowColour[1]*(1 - mix) + hiColour[1]*mix;
    intColour[2] = lowColour[2]*(1 - mix) + hiColour[2]*mix;
    return sprintf('rgb(%d, %d, %d)', intColour[0], intColour[1], intColour[2]);
}

class SuburbHeatMap extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let lowColour = [0, 255, 0];
        let hiColour = [255, 0, 0];
        let suburbPolygons = this.props.suburbPolygons;
        let scores = suburbPolygons.map((sp) => {
            return sp.suburbScore;
        });
        let minScore = (this.props.datasetName !== 'suburbSentiment' ) ? Math.min(...scores) : -1;
        let maxScore = (this.props.datasetName !== 'suburbSentiment' ) ? Math.max(...scores) : 1;
        console.log(minScore, maxScore);
        console.log("rendering sentiment heat map");
        return (
            <GoogleMap
                defaultZoom={9}
                defaultCenter={melbCenter}
                defaultOptions={{ styles: grayScaleFilter }}
            >
                {suburbPolygons.map((sp, index) => {
                    let mix = (sp.suburbScore - minScore)/(maxScore - minScore);
                    let polygonColour = interpolateColour(lowColour, hiColour, mix);
                    let styleToUse = {
                        ...polygonStyle,
                        fillColor: polygonColour
                    };
                    return (
                        <React.Fragment key={index}>
                            {sp.polygons.map((polygon, index) => {
                                return (
                                    <Polygon
                                        key={sp.suburbName + '-' + index}
                                        paths={polygon}
                                        options={{
                                            ...styleToUse
                                        }}
                                    />
                                );
                            })}
                        </React.Fragment>
                    );
                })}
            </GoogleMap>
        );
    }
}

export default withScriptjs(withGoogleMap(SuburbHeatMap));