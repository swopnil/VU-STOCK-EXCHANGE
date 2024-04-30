document.addEventListener('DOMContentLoaded', function() {
    var stockChart;
    var defaultSymbol = 'AAPL'; // Default stock symbol
    let selectedSymbol = defaultSymbol; // Store the currently selected symbol
    let previousSymbol = defaultSymbol; // Store the previously selected symbol
    let timeoutId = null; // Store the timeout ID
    // let selectedRange = 0;

    function updateGraph(symbol,selectedRange) {
        if (symbol !== previousSymbol) {
            // Destroy the existing chart
            if (stockChart) {
                stockChart.destroy();
                stockChart = null;
            }
            previousSymbol = symbol; // Update the previously selected symbol
        }
        var limit = 1000;
        if (selectedRange === 1) { // 1 day
            limit = 24; // Fetch the last 24 data points for 1 day
        } else if (selectedRange === 2) { // 1 week
            limit = 168; // Fetch the last 168 data points for 1 week
        } else if (selectedRange === 3) { // 1 month
            limit = 720; // Fetch the last 720 data points for 1 month
        } else if (selectedRange === 4) { // 1 year
            limit = 1000; // Fetch the last 1000 data points for 1 year
        }
        fetch(`/prices/${symbol}?limit=${limit}`)
        .then(response => response.json())
            .then(data => {
                console.log("Fetched data:", data);

                // Call createChart with the received data and range
                createChart(data, symbol, selectedRange);

                // Schedule the next update after a delay (e.g., 5 seconds)
                if (timeoutId) {
                    clearTimeout(timeoutId); // Clear the existing timeout
                }
                timeoutId = setTimeout(() => updateGraph(selectedSymbol, selectedRange), 5000); // Set a new timeout
            })
            .catch(error => console.error('Error fetching data:', error));
    }
    Highcharts.theme = {
        colors: ["#008000", "#AA4643", "#89A54E", "#80699B", "#3D96AE", "#DB843D", "#92A8CD", "#A47D7C", "#B5CA92"],
        chart: {
           
            backgroundColor: 'transparent', // Set background color to transparent
        borderWidth: 0, // Remove border
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'line',
            plotBackgroundColor: null ,
            style: {
                fontFamily: "'Unica One', sans-serif" // Set font family
            },
            plotBorderColor: '#008000' // Set plot border color to green
        },
        title: {
            style: {
                color: '#ffffff' // Set title text color to white
            }
        },
         legend: {
        enabled: false // Remove the legend
    },
    credits: {
        enabled: false // Remove the credits
    },

        subtitle: {
            style: {
                color: '#ffffff' // Set subtitle text color to white
            }
        },
        xAxis: {
            gridLineColor: '#008000',
            labels: {
                style: {
                    color: '#ffffff' // Set x-axis labels color to white
                }
            },
            lineColor: 'none', // Set x-axis line color to green
            minorGridLineColor: '#505053',
            tickColor: '#707073',
            title: {
                style: {
                    color: '#ffffff' // Set x-axis title color to white
                }
            }
        },
        yAxis: {
            gridLineColor: 'none',
            labels: {
                style: {
                    color: 'none' // Set y-axis labels color to white
                }
            },
            lineColor: '#008000', // Set y-axis line color to green
            minorGridLineColor: 'none',
            tickColor: '#707073',
            tickWidth: 1,
            title: {
                style: {
                    color: '#ffffff' // Set y-axis title color to white
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.85)',
            style: {
                color: '#ffffff' // Set tooltip text color to white
            }
        },
        plotOptions: {
            series: {
                dataLabels: {
                    color: '#ffffff' // Set data label color to white
                },
                marker: {
                    lineColor: '#ffffff' // Set marker line color to white
                }
            },
            boxplot: {
                fillColor: '#505053' // Set boxplot fill color
            },
            candlestick: {
                lineColor: 'white' // Set candlestick line color
            },
            errorbar: {
                color: 'white' // Set error bar color
            }
        },
        legend: {
            itemStyle: {
                color: '#ffffff' // Set legend item color to white
            },
            itemHoverStyle: {
                color: '#ffffff' // Set legend item hover color to white
            },
            itemHiddenStyle: {
                color: '#606063' // Set legend item hidden color
            }
        },
        credits: {
           
                enabled: false // Disable the credits
            
        
        },
        labels: {
            style: {
                color: '#ffffff' // Set labels color to white
            }
        },
        drilldown: {
            activeAxisLabelStyle: {
                color: '#ffffff' // Set drilldown active axis label color to white
            },
            activeDataLabelStyle: {
                color: '#ffffff' // Set drilldown active data label color to white
            }
        },
        navigation: {
            buttonOptions: {
                symbolStroke: '#ffffff',
                theme: {
                    fill: '#505053'
                }
            }
        },
        // Additional colors and styles
    };
   

    // Apply the theme
    Highcharts.setOptions(Highcharts.theme);
    
    
    
    // Apply the theme
  
    

    function createChart(data, symbol, selectedRange) {
        // Extract time and price arrays from the data object
        var timeArray = data.time;
        var priceArray = data.price;
    
        // Use the defaultSymbol to set the title of the chart
        var companyName = data.stocks[symbol].company_name;
    
        var chartData = []; // Initialize chartData as an empty array
    
        // Loop through time and price arrays to create chart data for new data points
        for (var i = 0; i < timeArray.length; i++) {
            var timestamp = timeArray[i];
            var formattedTime = Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', timestamp * 1000); // Convert to milliseconds
            var timeAgo = '';
    
            var seconds = Math.round((new Date() - timestamp * 1000) / 1000);
            if (seconds < 60) {
                timeAgo = seconds + ' seconds ago';
            } else if (seconds < 3600) {
                timeAgo = Math.round(seconds / 60) + ' minutes ago';
            } else if (seconds < 86400) {
                timeAgo = Math.round(seconds / 3600) + ' hours ago';
            } else {
                // timeAgo = Math.round(seconds / 86400) + ' days ago';
                timeAgo = formattedTime;
            }
    
            chartData.push([timestamp, parseFloat(priceArray[i])]);
        }
        console.log("Fetched time:", timeAgo);
    
        // Sort the chart data by timestamp in ascending order
        chartData.sort((a, b) => a[0] - b[0]);
        chartData.reverse()
    
        var rangeSelector = {
            buttons: [{
                type: 'day',
                count: 1,
                text: '1d',
            }, {
                type: 'week',
                count: 1,
                text: '1w',
            }, {
                type: 'month',
                count: 1,
                text: '1m',
            }, {
                type: 'year',
                count: 1,
                text: '1y',
            }, {
                type: 'all',
                text: 'All',
            }]
        };
    
        // If the stockChart instance doesn't exist, create a new one
        if (!stockChart) {
            stockChart = Highcharts.stockChart('stockChart', {
                rangeSelector: rangeSelector,
                title: {
                    text: `${companyName} Stock Price`
                },
                xAxis: {
                    labels: {
                        formatter: function() {
                            return timeAgo;
                        }
                    }
                },
                series: [{
                    name: 'Price',
                    data: chartData,
                    tooltip: {
                        valueDecimals: 2
                    }
                }]
            });
    
            // Add click event to range selector buttons
            stockChart.rangeSelector.buttons.forEach(function(button, index) {
                button.element.addEventListener('click', function() {
                    var selectedRange = index + 1; // Range starts from 1 for 1d, 2 for 1w, and so on
                    updateGraph(symbol,selectedRange);
                });
            });
        } else {
            // If the stockChart instance already exists, update the series data

            stockChart.series[0].setData(chartData);
        }
    }
    

    // Event listener for dropdown change
    document.getElementById('stockSelect').addEventListener('change', function() {
        selectedSymbol = this.value; // Update the selected symbol when the dropdown changes
        updateGraph(selectedSymbol); // Update the graph with data for the selected stock
    });

    // Prevent default form submission for buy and sell forms
    document.querySelectorAll('.buy-form, .sell-form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
        });
    });
    
});