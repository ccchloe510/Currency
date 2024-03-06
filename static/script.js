// script.js
var ctx = document.getElementById('myChart').getContext('2d');

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'GBP 折线图',
            data: [],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'minute'
                },
                distribution: 'linear',
                ticks: {
                    source: 'auto',
                    autoSkip: true,
                    maxTicksLimit: 10
                }
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: false
                }
            }]
        }
    }
});

function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });

    // Check if the data array is longer than a specific length
    if (chart.data.labels.length > 5) {
        chart.data.labels.shift(); // Remove the oldest label
        chart.data.datasets.forEach((dataset) => {
            dataset.data.shift(); // Remove the oldest data point
        });
    }

    chart.update();
}


function updateChart() {
    fetch('/get_realtime_data')
        .then(response => response.json())
        .then(data => {
            var label = data.time;
            var rate = data.rate;
            addData(myChart, label, rate);
        });
}

updateChart();
setInterval(updateChart, 5000);
