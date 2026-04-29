import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


PRODUCTS = [
    {"product_name": "Sanduche de pollo", "category": "Sanduches", "base_demand": 12},
    {"product_name": "Sanduche mixto", "category": "Sanduches", "base_demand": 10},
    {"product_name": "Sanduche de jamón", "category": "Sanduches", "base_demand": 8},
    {"product_name": "Sanduche de atún", "category": "Sanduches", "base_demand": 6},
    {"product_name": "Sanduche vegetariano", "category": "Sanduches", "base_demand": 5},
    {"product_name": "Cheesecake", "category": "Postres", "base_demand": 7},
    {"product_name": "Brownie", "category": "Postres", "base_demand": 9},
    {"product_name": "Tarta de chocolate", "category": "Postres", "base_demand": 8},
    {"product_name": "Tres leches", "category": "Postres", "base_demand": 6},
    {"product_name": "Galleta rellena", "category": "Postres", "base_demand": 11},
]


def generate_synthetic_product_sales_dataset(
    output_path="data/product_sales_history.csv",
    days=90,
    seed=42
):
    np.random.seed(seed)

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=days - 1)

    rows = []

    for i in range(days):
        current_date = start_date + timedelta(days=i)
        day_of_week = current_date.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        promo = np.random.choice([0, 1], p=[0.75, 0.25])

        for product in PRODUCTS:
            base = product["base_demand"]

            category_boost = 0
            if product["category"] == "Sanduches":
                category_boost += 2 if day_of_week in [0, 1, 2, 3, 4] else -1
            else:
                category_boost += 2 if is_weekend else 0

            promo_boost = np.random.randint(1, 4) if promo else 0
            noise = np.random.normal(0, 2)

            units_sold = max(
                0,
                int(round(base + category_boost + promo_boost + noise))
            )

            price = {
                "Sanduche de pollo": 3.50,
                "Sanduche mixto": 3.25,
                "Sanduche de jamón": 3.00,
                "Sanduche de atún": 3.75,
                "Sanduche vegetariano": 3.20,
                "Cheesecake": 2.80,
                "Brownie": 2.20,
                "Tarta de chocolate": 3.00,
                "Tres leches": 2.75,
                "Galleta rellena": 1.80,
            }[product["product_name"]]

            rows.append({
                "date": current_date.isoformat(),
                "product_name": product["product_name"],
                "category": product["category"],
                "day_of_week": day_of_week,
                "is_weekend": is_weekend,
                "promo": promo,
                "price": price,
                "units_sold": units_sold
            })

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    df = generate_synthetic_product_sales_dataset()
    print("Dataset generado correctamente.")
    print(df.head())