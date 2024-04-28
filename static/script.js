document.addEventListener('DOMContentLoaded', function() {
    var stockChart;
    var defaultSymbol = 'AAPL'; // Default stock symbol

      function updateGraph(symbol) {
        fetch(`/prices/${symbol}?limit=10`) // Fetch only the last 10 data points for the selected symbol
            .then(response => response.json())
            .then(data => {
                console.log("Fetched data:", data);
    
                // Call createChart with the received data
                createChart(data);
    
                // Schedule the next update after a delay (e.g., 5 seconds)
                setTimeout(() => updateGraph(symbol), 5000); // Adjust the delay as needed
            })
            .catch(error => console.error('Error fetching data:', error));
    }
    
    
    function createChart(data) {
    // Extract time and price arrays from the data object
    var timeArray = data.time;
    var priceArray = data.price;

    // Use the defaultSymbol to set the title of the chart
    var companyName = data.stocks[defaultSymbol].company_name;

    var chartData = stockChart ? stockChart.series[0].options.data : []; // Get existing chart data

    // Clear existing chart data
    chartData.length = 0;

    // Loop through time and price arrays to create chart data for new data points
    for (var i = 0; i < timeArray.length; i++) {
        chartData.push([timeArray[i], parseFloat(priceArray[i])]);
    }

    // Sort the chart data by timestamp in ascending order
    chartData.sort((a, b) => a[0] - b[0]);

    // If the stockChart instance doesn't exist, create a new one
    if (!stockChart) {
        stockChart = Highcharts.stockChart('stockChart', {
            rangeSelector: {
                selected: 1,
                buttons: [{
                    type: 'day',
                    count: 1,
                    text: '1d'
                }, {
                    type: 'week',
                    count: 7,
                    text: '1w'
                }, {
                    type: 'month',
                    count: 30,
                    text: '1m'
                }, {
                    type: 'year',
                    count: 365,
                    text: '1y'
                }, {
                    type: 'all',
                    text: 'All'
                }]
            },
            title: {
                text: `${companyName} Stock Price`
            },
            series: [{
                name: 'Price',
                data: chartData,
                tooltip: {
                    valueDecimals: 2
                }
            }]
        });
    } else {
        // If the stockChart instance already exists, update the series data
        stockChart.series[0].setData(chartData);
    }
}
    
    // Initial fetch and chart creation for the default symbol
    updateGraph(defaultSymbol);

    // Event listener for dropdown change
    // Event listener for dropdown change
document.getElementById('stockSelect').addEventListener('change', function() {
    var selectedSymbol = this.value;

    // Clear the existing chart before fetching new data
    if (stockChart) {
        stockChart.destroy();
        stockChart = null;
    }

    // Update the graph with data for the selected stock
    updateGraph(selectedSymbol);
});

    // Prevent default form submission for buy and sell forms
    document.querySelectorAll('.buy-form, .sell-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
        });
    });
});
