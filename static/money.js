function fetchUserData() {
  fetch('/money')
    .then(response => response.json())
    .then(data => {
      // Call a function to create the chart with the user data
      createUserMoneyChart(data);
    })
    .catch(error => console.error('Error fetching user data:', error));
}

function createUserMoneyChart(data) {
  // Extract username, money, and timestamp from the data object
  const { username, money, timestamp } = data;

  // Prepare the chart data
  const chartData = [[Date.parse(timestamp), money]];

  // Create the chart
  Highcharts.chart('chartContainer', {
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