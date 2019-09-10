import React from 'react';
import datasetMetadata from '../data/datasetMetadata';

const ControlPanel = ({
    predictor,
    response,
    datasetToShow,
    datasets,
    actionHandlers
}) => {
    let onShowChange = (e) => actionHandlers.handleShowChange(e.target.value);
    let onPredictChange = (e) => actionHandlers.handlePredictorChange(e.target.value);
    let onResponseChange = (e) => actionHandlers.handleResponseChange(e.target.value);
    return (
        <form>
            <div>
                <label>Predictor</label>
                <select 
                    value={predictor} 
                    onChange={onPredictChange}
                >
                    <option value=''>Please select a predictor</option>
                    {datasetMetadata.map((dsm) => {
                        return (
                            <option 
                                key={dsm.name}
                                value={dsm.name}
                            >{dsm.name}</option>
                        );
                    })}
                </select>
            </div>
            <div>
                <label>Response</label>
                <select 
                    value={response}
                    onChange={onResponseChange}
                >
                    <option value=''>Please select a response</option>
                    {datasetMetadata.map((dsm) => {
                        return (
                            <option 
                                key={dsm.name}
                                value={dsm.name}
                            >{dsm.name}</option>
                        );
                    })}
                </select>
            </div>
            <div>
                <label>Show on map:</label>
                <select
                    value={datasetToShow}
                    onChange={onShowChange}
                >
                    <option value=''>Please select a dataset to display on the map</option>
                    {datasetMetadata.map((dsm) => {
                        return (
                            <option 
                                key={dsm.name}
                                value={dsm.name}
                            >{dsm.name}</option>
                        );
                    })}
                </select>
            </div>
            <div>
                <button type='button' onClick={actionHandlers.fetchAllDatasets}>Refresh data</button>
                <button type='button' onClick={actionHandlers.runAnalysis}>Analyse</button>
            </div>
            <div style={{background: 'green'}}>
                <span>Low</span>
            </div>
            <div style={{background: 'red'}}>
                <span>High</span>
            </div>
        </form>
    );
}

export default ControlPanel;