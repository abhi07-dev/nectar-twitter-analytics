import React from 'react';
import Plot from 'react-plotly.js';

const RegressionPlot = ({analysisInfo}) => {
    console.log(analysisInfo);
    let points = analysisInfo.points; 
    let gradient = analysisInfo.result.equation[0];
    let intercept = analysisInfo.result.equation[1]; 
    let predictorName = analysisInfo.predictorName; 
    let responseName = analysisInfo.responseName;

    let x = points.map((point) => point[0]);
    let y = points.map((point => point[1]));
    let xmin = Math.min(...x);
    let xmax = Math.max(...x);
    let ymin = gradient*xmin + intercept;
    let ymax = gradient*xmax + intercept;

    return (
        <div>
            <span>Equation: y = {gradient}x + {intercept}</span>
            <Plot
                data={[
                {
                    x: x,
                    y: y,
                    type: 'scatter',
                    mode: 'markers',
                    marker: {color: 'red'},
                },
                {
                    type: 'line', 
                    x: [xmin, xmax], 
                    y: [ymin, ymax]
                },]}
                layout={{
                    width: 500, 
                    height: 500, 
                    title: 'Regression',
                    xaxis: {
                        title: predictorName,
                    },
                    yaxis: {
                        title: responseName,
                    }
                }}
            />
        </div>
    );
}



export default RegressionPlot;