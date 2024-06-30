document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            const visualizationsDiv = document.getElementById('visualizations');

            // Create a visualization for each collection
            for (let [collectionName, collectionData] of Object.entries(data)) {
                const canvasElement = document.createElement('canvas');
                canvasElement.id = `chart-${collectionName}`;
                visualizationsDiv.appendChild(canvasElement);

                // This is a simple bar chart example. You might want to create different types of charts based on your data.
                new Chart(canvasElement, {
                    type: 'bar',
                    data: {
                        labels: collectionData.map(item => item.label || item.name || item._id),
                        datasets: [{
                            label: collectionName,
                            data: collectionData.map(item => item.value || Math.random() * 100), // Replace with actual data field
                            backgroundColor: 'rgba(75, 192, 192, 0.6)'
                        }]
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
        })
        .catch(error => console.error('Error:', error));
});