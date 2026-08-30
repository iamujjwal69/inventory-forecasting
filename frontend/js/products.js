async function loadProducts() {
    try {
        const products = await getProducts();
        const tbody = document.querySelector('#productsTable tbody');
        tbody.innerHTML = '';
        
        for (const p of products) {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>${p.category || '-'}</td>
                <td>$${p.price.toFixed(2)}</td>
                <td>${p.current_stock}</td>
                <td>${p.reorder_level}</td>
            `;
            tbody.appendChild(tr);
        }
    } catch (e) {
        console.error("Failed to load products:", e);
    }
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/index.html';
}

loadProducts();
