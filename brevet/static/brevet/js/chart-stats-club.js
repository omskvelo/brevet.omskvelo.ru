const chart_distance = JSON.parse(document.getElementById('chart_distance').textContent)
const chart_colors = JSON.parse(document.getElementById('chart_colors').textContent)
const canvas = document.getElementById('chart-stats-club')
const canvasContainer = document.getElementById('container-stats-club')

canvasContainer.setAttribute("style",`height: ${chart_distance.length * 30 + 50}px;`)

Chart.register(ChartDataLabels);

const chart = new Chart(canvas, {
  type: 'bar',
  data: {
    labels: chart_distance.map(row => row.y),
    datasets: [
      {
        data: chart_distance,
        backgroundColor: chart_colors,
        datalabels: {
          display: true,
          color: "#1d3652",
        }
      },
    ]
  },
  options: {
    indexAxis: 'y',
    plugins: {
      legend: {
        display: false
      },
    },
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
      }
    },
    maintainAspectRatio: false,
    responsive: true,
  },
  scales: {
    x: {
      type: 'linear',
    },
    y: {
      type: 'linear',
    }
  }
})