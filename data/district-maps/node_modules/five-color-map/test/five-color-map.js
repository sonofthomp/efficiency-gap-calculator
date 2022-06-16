var fs = require('fs'),
    fiveColorMap = require('../'),
    geojsonhint = require('geojsonhint');

var geojson = JSON.parse(fs.readFileSync('./test/data.json'));

var colorMap = fiveColorMap(geojson);

console.log(geojsonhint.hint(colorMap));
