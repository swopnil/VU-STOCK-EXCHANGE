// Get the canvas element
const totalBalanceCanvas = document.getElementById('totalBalanceChart');

// Create a new chart instance
const totalBalanceChart = new Chart(totalBalanceCanvas, {
    type: 'line',
    data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        datasets: [{
            label: 'Total Balance',
            data: [500000, 550000, 600000, 590351.97],
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});// Get the canvas element
const totalBalanceCanvas = document.getElementById('totalBalanceChart');

// Create a new chart instance
const totalBalanceChart = new Chart(totalBalanceCanvas, {
    type: 'line',
    data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        datasets: [{
            label: 'Total Balance',
            data: [500000, 550000, 600000, 590351.97],
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});