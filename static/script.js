document.addEventListener('DOMContentLoaded', function() {
    var stockChart;
    var defaultSymbol = 'AAPL'; // Default stock symbol
    let selectedSymbol = defaultSymbol; // Store the currently selected symbol
    let previousSymbol = defaultSymbol; // Store the previously selected symbol
    let selectedRange = 0; // Store the currently selected range
    let timeoutId = null; // Store the timeout ID

    function updateGraph(symbol) {
        if (symbol !== previousSymbol) {
            // Destroy the existing chart
            if (stockChart) {
                stockChart.destroy();
                stockChart = null;
            }
            previousSymbol = symbol; // Update the previously selected symbol
        }

        fetch(`/prices/${symbol}?limit=10`) // Fetch only the last 10 data points for the selected symbol
            .then(response => response.json())
            .then(data => {
                console.log("Fetched data:", data);

                // Call createChart with the received data and range
                createChart(data, symbol, selectedRange);

                // Schedule the next update after a delay (e.g., 5 seconds)
                if (timeoutId) {
                    clearTimeout(timeoutId); // Clear the existing timeout
                }
                timeoutId = setTimeout(() => updateGraph(selectedSymbol), 5000); // Set a new timeout
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    function createChart(data, symbol, range) {
        // Extract time and price arrays from the data object
        var timeArray = data.time;
        var priceArray = data.price;

        // Use the defaultSymbol to set the title of the chart
        var companyName = data.stocks[defaultSymbol].company_name;

        var chartData = []; // Initialize chartData as an empty array

        // Loop through time and price arrays to create chart data for new data points
        for (var i = 0; i < timeArray.length; i++) {
            chartData.push([timeArray[i], parseFloat(priceArray[i])]);
        }

        // Sort the chart data by timestamp in ascending order
        chartData.sort((a, b) => a[0] - b[0]);

        var rangeSelector = {
            selected: 1,
            buttons: [{
                type: 'day',
                count: 1,
                text: '1d'
            }, {
                type: 'week',
                count: 1,
                text: '1w'
            }, {
                type: 'month',
                count: 1,
                text: '1m'
            }, {
                type: 'year',
                count: 1,
                text: '1y'
            }, {
                type: 'all',
                text: 'All'
            }]
        };

        if (range) {
            rangeSelector.selected = range; // Set the selected range
        }

        // If the stockChart instance doesn't exist, create a new one
        if (!stockChart) {
            stockChart = Highcharts.stockChart('stockChart', {
                rangeSelector: rangeSelector,
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
    document.getElementById('stockSelect').addEventListener('change', function() {
        selectedSymbol = this.value; // Update the selected symbol when the dropdown changes
        updateGraph(selectedSymbol); // Update the graph with data for the selected stock
    });

    // Event listener for range selector change
    document.getElementById('rangeSelector').addEventListener('change', function() {
        selectedRange = this.value; // Update the selected range when the range selector changes
        updateGraph(selectedSymbol); // Update the graph with data for the selected stock and range
    });

    // Prevent default form submission for buy and sell forms
    document.querySelectorAll('.buy-form, .sell-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
        });
    });
});