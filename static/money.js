function fetchUserData() {
    fetch('/prices/${symbol}?limit=${limit}')
      .then(response => response.json())
      .then(data => {
        // Call a function to create the chart with the user data
        createUserMoneyChart(data);
      })
      .catch(error => console.error('Error fetching user data:', error));
  }

  function createUserMoneyChart(userData) {
    // Extract time and money arrays from the userData object
    const timeArray = userData.map(user => user.timestamp);
    const moneyArray = userData.map(user => user.money);
  
    // Prepare the chart data
    const chartData = timeArray.map((timestamp, index) => [timestamp * 1000, moneyArray[index]]);
  
    // Sort the chart data by timestamp in ascending order
    chartData.sort((a, b) => a[0] - b[0]);
  
    // Create the chart
    Highcharts.chart('stockChart', {
      title: {
        text: 'User Money Over Time'
      },
      xAxis: {
        type: 'datetime',
        labels: {
          formatter: function() {
            return Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.value);
          }
        }
      },
      yAxis: {
        title: {
          text: 'Money'
        }
      },
      series: [{
        name: 'User Money',
        data: chartData
      }]
    });
  }