import httpx
import json

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print(f"\n{'='*50}\n{title}\n{'='*50}")

def run_tour():
    client = httpx.Client(base_url=BASE_URL)
    
    print_section("1. Testing Authentication (Register & Login)")
    # Register
    reg_res = client.post("/auth/register", json={
        "name": "Admin User",
        "email": "admin2@example.com",
        "password": "securepassword123"
    })
    print(f"Register Response ({reg_res.status_code}): {reg_res.text}")
    
    # Login
    login_res = client.post("/auth/login", json={
        "email": "admin2@example.com",
        "password": "securepassword123"
    })
    print(f"Login Response ({login_res.status_code}): {login_res.text}")
    token = login_res.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    print_section("2. Fetching Products (Inventory Data)")
    prod_res = client.get("/products", headers=headers)
    products = prod_res.json()
    print(f"Found {len(products)} products in the database.")
    if products:
        first_product = products[0]
        print(f"Sample Product: {json.dumps(first_product, indent=2)}")
        product_id = first_product["id"]
        
        print_section("3. Creating a Sale (Deducting Inventory)")
        sale_res = client.post("/sales/", headers=headers, json={
            "product_id": product_id,
            "sale_date": "2026-08-30",
            "quantity": 2,
            "unit_price": first_product["price"]
        })
        print(f"Sale Creation Response ({sale_res.status_code}): {sale_res.text}")
        
        print_section("4. AI Forecasting & Recommendations")
        print(f"Triggering forecast for Product ID {product_id} for the next 7 days...")
        forecast_res = client.get(f"/forecast/{product_id}?days=7", headers=headers)
        if forecast_res.status_code == 200:
            forecast_data = forecast_res.json()
            print(f"AI Recommendation: {json.dumps(forecast_data['recommendation'], indent=2)}")
            print(f"Total Predicted Demand (7 days): {forecast_data['predicted_demand']}")
            print(f"Daily Breakdown: {json.dumps(forecast_data['daily_forecast'][:3], indent=2)} ... (truncated)")
        else:
            print(f"Forecast Error: {forecast_res.text}")

if __name__ == "__main__":
    run_tour()
