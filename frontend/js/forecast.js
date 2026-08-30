let chartInstance = null;

async function loadProductsForSelect() {
    try {
        const products = await getProducts();
        const select = document.getElementById('productSelect');
        for (const p of products) {
            const option = document.createElement('option');
            option.value = p.id;
            option.textContent = p.name;
            select.appendChild(option);
        }
    } catch (e) {
        console.error("Failed to load products for select:", e);
    }
}

async function loadProductForecast() {
    const productId = document.getElementById('productSelect').value;
    const container = document.getElementById('forecastContainer');
    const errorContainer = document.getElementById('errorContainer');
    
    container.style.display = 'none';
    errorContainer.style.display = 'none';
    
    if (!productId) return;
    
    try {
        const f = await getForecast(productId, 30);
        
        container.style.display = 'block';
        
        // Update summary cards
        document.getElementById('predictedDemand').textContent = f.predicted_demand;
        if (f.recommendation) {
            document.getElementById('recommendationStatus').textContent = f.recommendation.status;
            document.getElementById('suggestedOrder').textContent = f.recommendation.recommended_order;
        } else {
            document.getElementById('recommendationStatus').textContent = 'N/A';
            document.getElementById('suggestedOrder').textContent = 'N/A';
        }
        
        // Render chart
        if (f.daily_forecast) {
            const labels = f.daily_forecast.map(d => d.date);
            const data = f.daily_forecast.map(d => d.demand);
            
            if (chartInstance) {
                chartInstance.destroy();
            }
            
            const ctx = document.getElementById('productForecastChart').getContext('2d');
            chartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Forecast Demand',
                        data: data,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
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
    } catch (e) {
        console.error("Forecast error:", e);
        errorContainer.textContent = "Could not load forecast: " + e.message;
        errorContainer.style.display = 'block';
    }
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/index.html';
}

loadProductsForSelect();
