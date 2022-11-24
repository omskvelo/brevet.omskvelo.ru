const distance = JSON.parse(document.getElementById('chart_distance').textContent)
const milestones = JSON.parse(document.getElementById('chart_milestones').textContent)
const canvas = document.getElementById('chart-stats-personal')


const chart = new Chart(canvas, {
    data:{
        labels: distance.map(row => row.x),
        datasets:[
          {
            type: 'bar',
            data: distance.map(row => row.y),
            fillColor: "#1d3652",
          }
        ]
      },
    options:{
        plugins: {
            legend: {
              display: false
            }
        },
        maintainAspectRatio: false
    },
    responsive: true,
    scales: {
      x: {
        stacked: true
      },
      y: {
        stacked: true,
      }
    }
})