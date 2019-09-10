const express = require('express');
const path = require('path');
const http = require('http');
const request = require('request');
const sprintf = require('sprintf-js').sprintf;

const app = express();

let portNumber = process.argv[2] || 3000;
let dbIp = process.argv[3] || 'localhost';
let dbPort = process.argv[4] || 5984;
let dbName = 'twitter';

app.use("/dist", express.static(path.join(
    __dirname, '../react-front-end', '/dist')));

app.get('/recent_tweets', (req, res) => {
    let limit = req.query.limit || 5;
    let designDoc = 'analytics_test';
    let viewName = 'tweets_by_date';
    let url = sprintf('http://%s:%s/%s/_design/%s/_view/%s?limit=%d&descending=true', 
        dbIp,
        dbPort,
        dbName, 
        designDoc, 
        viewName, 
        limit);
    request.get(url, function (err, dbRes, body) {
        console.log(body);
        res.send(body);
    });
})

app.get('/suburb_sentiment', (req, res) => {
    let designDoc = 'analytics_test';
    let viewName = 'suburb_sentiment';
    let url = sprintf('http://%s:%s/%s/_design/%s/_view/%s?group=true', 
        dbIp,
        dbPort,
        dbName, 
        designDoc, 
        viewName);
    request.get(url, function (err, dbRes, body) {
        res.send(body);
    });
})

app.get('/suburb_median_age', (req, res) => {
    let designDoc = 'analytics';
    let viewName = 'suburb_median_age';
    let url = sprintf('http://%s:%s/%s/_design/%s/_view/%s', 
        dbIp,
        dbPort,
        'aurin', 
        designDoc, 
        viewName);
    request.get(url, function (err, dbRes, body) {
        res.send(body);
    });
})

app.get('/suburb_employment_rate', (req, res) => {
    let designDoc = 'analytics';
    let viewName = 'suburb_employment_rate';
    let url = sprintf('http://%s:%s/%s/_design/%s/_view/%s', 
        dbIp,
        dbPort,
        'aurin', 
        designDoc, 
        viewName);
    request.get(url, function (err, dbRes, body) {
        res.send(body);
    });
})

app.get('/suburb_median_household_income', (req, res) => {
    let designDoc = 'analytics';
    let viewName = 'suburb_median_household_income';
    let url = sprintf('http://%s:%s/%s/_design/%s/_view/%s', 
        dbIp,
        dbPort,
        'aurin', 
        designDoc, 
        viewName);
    request.get(url, function (err, dbRes, body) {
        res.send(body);
    });
})

app.get('/suburb_avg_government_benefits', (req, res) => {
    let designDoc = 'analytics';
    let viewName = 'suburb_avg_government_benefits';
    let url = sprintf('http://%s:%s/%s/_design/%s/_view/%s', 
        dbIp,
        dbPort,
        'aurin', 
        designDoc, 
        viewName);
    request.get(url, function (err, dbRes, body) {
        res.send(body);
    });
})

app.get('/suburb_restaurants_bars_count', (req, res) => {
    let designDoc = 'analytics';
    let viewName = 'count';
    let url = sprintf('http://%s:%s/%s/_design/%s/_view/%s?group=true', 
        dbIp,
        dbPort,
        'restaurantsbars', 
        designDoc, 
        viewName);
    request.get(url, function (err, dbRes, body) {
        res.send(body);
    });
})

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../html', 'index.html'));
});

app.listen(portNumber, () => console.log('Listening on ' + portNumber));