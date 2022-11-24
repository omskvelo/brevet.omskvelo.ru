const distance = JSON.parse(document.getElementById('chart_distance').textContent)
const milestones = JSON.parse(document.getElementById('chart_milestones').textContent)
const canvas = document.getElementById('chart-stats-personal')
const canvasContainer = document.getElementById('container-stats-personal')

canvasContainer.setAttribute("style",`height: ${distance.length * 50 + 50}px;`)

const mobile = window.screen.width <= 600
const datalabels_display_milestones = !mobile


Chart.register(ChartDataLabels);

const chart = new Chart(canvas, {
  type: 'bar',
  data: {
    labels: distance.map(row => row.y),
    datasets: [
      {
        data: distance,
        borderColor: "#1d365290",
        borderWidth: 0,
        backgroundColor: "#36a2eb55",
        datalabels: {
          display: true,
          color: "#1d3652",
          anchor: 'start',
          align: 'right',
        }
      },
      {
        data: milestones,
        fillColor: "#1d3652",
        datalabels: {
          display: datalabels_display_milestones,
          color: "#1d3652",
          anchor: 'start',
          align: 'right'
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
        grace: "30%"
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