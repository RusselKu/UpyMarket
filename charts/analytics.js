const canvas = document.getElementById('telemetryChart');

if (canvas && window.Chart) {
  new window.Chart(canvas, {
    type: 'bar',
    data: {
      labels: ['Academic', 'Leisure', 'Laptop with GPU'],
      datasets: [
        {
          label: 'Sample Clicks',
          data: [12, 8, 5],
          backgroundColor: ['#2563eb', '#7c3aed', '#10b981']
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
