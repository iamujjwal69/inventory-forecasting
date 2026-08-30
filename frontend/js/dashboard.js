async function loadDashboard() {
    try {
        const products = await getProducts();
        // Calculate stats
        let totalStock = 0, lowStock = 0, totalSales = 0;
        products.forEach(p => {
            totalStock += p.current_stock;
            if (p.current_stock < p.reorder_level) lowStock++;
            // For sales, we'd need another API; we'll mock for now.
        });
        document.getElementById('totalProducts').textContent = products.length;
        document.getElementById('totalStock').textContent = totalStock;
        document.getElementById('lowStock').textContent = lowStock;
        document.getElementById('totalSales').textContent = 'N/A';

        // Load first product forecast for chart
        if (products.length) {
            try {
                const f = await getForecast(products[0].id, 7);
                if (f && f.daily_forecast) {
                    const labels = f.daily_forecast.map(d => d.date);
                    const data = f.daily_forecast.map(d => d.demand);
                    new Chart(document.getElementById('forecastChart'), {
                        type: 'line',
                        data: { labels, datasets: [{ label: 'Forecast Demand', data }] }
                    });
                }
            } catch (err) {
                console.warn("Forecast for chart not available:", err.message);
            }
        }
        // Load sales trend (mock)
        // ...
        // Populate recommendation table
        const tbody = document.querySelector('#recomTable tbody');
        tbody.innerHTML = '';
        for (const p of products) {
            let f = null;
            try {
                f = await getForecast(p.id, 7);
            } catch (err) {
                console.warn(`Forecast not available for product ${p.id}:`, err.message);
            }
            const recom = f ? f.recommendation : { recommended_order: 0, status: 'N/A' };
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${p.name}</td><td>${p.current_stock}</td>
                <td>${f ? f.predicted_demand : '-'}</td>
                <td>${recom.recommended_order}</td>
                <td>${recom.status}</td>`;
            tbody.appendChild(tr);
        }
    } catch (e) {
        console.error(e);
    }
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/index.html';
}

loadDashboard();
