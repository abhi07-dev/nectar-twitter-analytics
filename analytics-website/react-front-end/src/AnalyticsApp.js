import React, { Component } from 'react';
import SplitterLayout from 'react-splitter-layout';
import { sprintf } from 'sprintf-js';

import SuburbHeatMap from './SuburbHeatMap';
import ControlPanel from './ControlPanel';
import RegressionPlot from './RegressionPlot';
import datasetMetadata from '../data/datasetMetadata';
import {extractCoordinates, suburbRegression} from './analysisFunctions';

class AnalyticsApp extends Component {
    constructor(props) {
        super(props);
        this.geoJsonUrl = 'https://data.gov.au/geoserver/vic-suburb-locality-boundaries-psma-administrative-boundaries/wfs?request=GetFeature&typeName=ckan_af33dd8c_0534_4e18_9245_fc64440f742e&outputFormat=json';
        this.state = {
            analysisInfo: {
                points: null,
                result: null,
                predictorName: '',
                responseName: '',
                complete: false
            },
            suburbPolygons: [],
            allDatasets: {},
            predictor: '',
            response: '',
            datasetToShow: '',
        }
        
        this.fetchDatasetByName = this.fetchDatasetByName.bind(this);
        this.fetchAllDatasets = this.fetchAllDatasets.bind(this);
        this.fetchAndParseSuburbPolygons = this.fetchAndParseSuburbPolygons.bind(this);
        this.handlePredictorChange = this.handlePredictorChange.bind(this);
        this.handleResponseChange = this.handleResponseChange.bind(this);
        this.handleShowChange = this.handleShowChange.bind(this);
        this.runAnalysis = this.runAnalysis.bind(this);
        this.augmentSuburbPolygons = this.augmentSuburbPolygons.bind(this);

        this.actionHandlers = {
            fetchDatasetByName: this.fetchDatasetByName,
            fetchAllDatasets: this.fetchAllDatasets,
            handlePredictorChange: this.handlePredictorChange,
            handleResponseChange: this.handleResponseChange,
            handleShowChange: this.handleShowChange,
            runAnalysis: this.runAnalysis
        };
    }

    runAnalysis() {
        if (this.state.predictor && this.state.response) {
            let predictorSet = this.state.allDatasets[this.state.predictor];
            let responseSet = this.state.allDatasets[this.state.response];
            let points = extractCoordinates(
                predictorSet,
                responseSet
            );
            let result = suburbRegression(
                predictorSet,
                responseSet
            );
            this.setState({
               analysisInfo: {
                   points: points,
                   result: result,
                   predictorName: this.state.predictor,
                   responseName: this.state.response,
                   complete: true
               }
            });
        } else {
            console.log('select params');
        }
    }

    handleShowChange(newShow) {
        this.setState({
            datasetToShow: newShow
        });
    }

    handlePredictorChange(newPredictor) {
        this.setState({
            predictor: newPredictor
        });
    }

    handleResponseChange(newResponse) {
        this.setState({
            response: newResponse
        });
    }

    fetchDatasetByName(dsName) {
        let dsm = datasetMetadata.find((d) => d.name == dsName);
        if (dsm) {
            return fetch('/' + dsm.url).then((response) => {
                return response.json();
            }).then((jsonResponse) => {
                this.setState({
                    allDatasets: {
                        ...this.state.allDatasets,
                        [dsm.name]: jsonResponse.rows
                    }
                });
                return jsonResponse.rows;
            });
        }
    }

    fetchAllDatasets() {
        let ads = {};
        let promises = [];
        datasetMetadata.forEach((dsm) => {
            promises.push(fetch('/' + dsm.url).then((response) => {
                return response.json();
            }).then((jsonResponse) => {
                ads[dsm.name] = jsonResponse.rows;
            }));
        });

        return Promise.all(promises).then(() => {
            console.log(ads);
            this.setState({
                allDatasets: ads
            });
        });
    }

    fetchAndParseSuburbPolygons() {
        return fetch(this.geoJsonUrl).then((res) => {
            return res.json();
        }).then((suburbData) => {
            let suburbPolygons = suburbData.features.map((suburb) => {
                let polygons = suburb.geometry.coordinates[0].map((polygon) => {
                    let paths = polygon.map((point) => {
                        return ({
                            lat: point[1],
                            lng: point[0]
                        });
                    });
                    return paths;
                });
                let suburbName = suburb.properties.vic_loca_2.toLowerCase();
                return ({
                    suburbName: suburbName,
                    suburbScore: 0,
                    polygons: polygons
                });
            });
            this.setState({
                suburbPolygons: suburbPolygons
            });
        });
    }

    augmentSuburbPolygons() {
        let dsname = this.state.datasetToShow;
        let ds = this.state.allDatasets[dsname];
        if (ds) {
            return this.state.suburbPolygons.map((sp) => {
                let foundSuburb = ds.find((s) => {
                    return (s.key == sp.suburbName);
                });
                
                if (foundSuburb) {
                    return ({
                        ...sp,
                        suburbScore: foundSuburb.value,
                    });
                }
            }).filter((suburb) => suburb); // filter out undefined
        } else {
            return null;
        }
    }

    componentDidMount() {
        this.fetchAllDatasets();
        this.fetchAndParseSuburbPolygons().then(() => {
        });
    }

    render() {
        let augmentedSuburbPolygons = this.augmentSuburbPolygons();
        let analysisInfo = this.state.analysisInfo;
        return (
            <SplitterLayout
                percentage={true}
                secondaryInitialSize={50}
            >
                <div>
                    <ControlPanel
                        predictor={this.state.predictor}
                        response={this.state.response}
                        datasetToShow={this.state.datasetToShow}
                        actionHandlers={this.actionHandlers}
                    />
                    {analysisInfo.complete && 
                    <RegressionPlot analysisInfo={analysisInfo}/>}
                </div>
                <div>
                    {augmentedSuburbPolygons && <SuburbHeatMap
                        datasetName={this.state.datasetToShow}
                        suburbPolygons={augmentedSuburbPolygons}
                        googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,visualization,drawing,places"
                        loadingElement={<div style={{ height: `100%` }} />}
                        containerElement={<div style={{ height: `100vh` }}/>}
                        mapElement={<div style={{ height: `100%` }} />}
                    />}
                </div>
            </SplitterLayout>
        );
    }
}

export default AnalyticsApp;