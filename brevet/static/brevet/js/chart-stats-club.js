function make_chart(){
  const canvas = document.getElementById('chart-stats-club')
  const chart_distance = JSON.parse(document.getElementById('chart_distance').textContent)
  const chart_colors = JSON.parse(document.getElementById('chart_colors').textContent)

  Chart.register(ChartDataLabels)
  
  let new_chart = new Chart(canvas, {
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
      maintainAspectRatio: true,
      responsive: true,
      animations: false,
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
  return new_chart
}

let chart = make_chart()

const redraw_path = /^\/database\/hx\/stats\/club\/(?:\d{4})|(?:total)$/

function redraw(event){
  if (redraw_path.test(event.detail.pathInfo.requestPath)){
    chart.destroy()
    chart = make_chart()
  }
}

document.addEventListener('htmx:afterSwap', redraw)