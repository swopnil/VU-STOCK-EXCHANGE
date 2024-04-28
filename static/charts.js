Highcharts.stockChart('container', {
    rangeSelector: {
        selected: 1
    },

    title: {
        text: 'Stock Price'
    },

    series: [{
        name: 'AAPL',
        data: [
            [1619433600000, 135.00],
            [1619520000000, 138.00],
            [1619606400000, 133.00],
            // Add more data points as needed
        ],
        tooltip: {
            valueDecimals: 2
        }
    }]
});
