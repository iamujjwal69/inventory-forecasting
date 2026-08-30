def get_recommendation(current_stock, predicted_demand, reorder_level, safety_stock_ratio=0.1):
    safety_stock = int(predicted_demand * safety_stock_ratio)
    recommended_order = max(0, predicted_demand + safety_stock - current_stock)
    if current_stock <= 0:
        status = "OUT_OF_STOCK"
    elif current_stock < reorder_level:
        status = "REORDER_REQUIRED"
    elif current_stock < predicted_demand:
        status = "LOW_STOCK"
    elif current_stock > predicted_demand * 1.5:
        status = "OVERSTOCKED"
    else:
        status = "IN_STOCK"
    return {
        "current_stock": current_stock,
        "predicted_demand": predicted_demand,
        "safety_stock": safety_stock,
        "recommended_order": recommended_order,
        "status": status
    }
