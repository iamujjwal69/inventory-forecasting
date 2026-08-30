async function loadDashboard() {
    try {
        const products = await getProducts();
        let totalStock = 0, lowStock = 0, totalSales = 0;
        products.forEach(p => {
            totalStock += p.current_stock;
            if (p.current_stock < p.reorder_level) lowStock++;
        });
        
        try {
            const sales = await getSales();
            const thirtyDaysAgo = new Date();
            thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
            sales.forEach(s => {
                if (new Date(s.sale_date) >= thirtyDaysAgo) {
                    totalSales += (s.quantity * s.unit_price);
                }
            });
            document.getElementById('totalSales').textContent = '$' + totalSales.toFixed(2);
        } catch (e) {
            console.warn("Could not fetch sales:", e);
            document.getElementById('totalSales').textContent = 'Error';
        }

        document.getElementById('totalProducts').textContent = products.length;
        document.getElementById('totalStock').textContent = totalStock;
        document.getElementById('lowStock').textContent = lowStock;

        // Populate product dropdown
        const select = document.getElementById('dashboardProductSelect');
        products.forEach(p => {
            const option = document.createElement('option');
            option.value = p.id;
            option.textContent = p.name;
            select.appendChild(option);
        });
        
        if (products.length > 0) {
            await updateDashboardChart();
        }
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

let dashboardChartInstance = null;

async function updateDashboardChart() {
    const select = document.getElementById('dashboardProductSelect');
    const productId = select.value;
    const productName = select.options[select.selectedIndex].text;
    
    if (!productId) return;
    
    try {
        const f = await getForecast(productId, 7);
        if (f && f.daily_forecast) {
            const labels = f.daily_forecast.map(d => d.date);
            const data = f.daily_forecast.map(d => d.demand);
            
            if (dashboardChartInstance) {
                dashboardChartInstance.destroy();
            }
            
            dashboardChartInstance = new Chart(document.getElementById('forecastChart'), {
                type: 'line',
                data: { labels, datasets: [{ label: `Forecast Demand for ${productName}`, data }] }
            });
        }
    } catch (err) {
        console.warn("Forecast for chart not available:", err.message);
    }
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/index.html';
}

loadDashboard();
