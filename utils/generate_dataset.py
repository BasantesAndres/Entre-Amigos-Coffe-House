import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def generate_synthetic_sales_dataset(output_path="data/sales_history.csv", days=90, seed=42):
    np.random.seed(seed)

    end_date = datetime.today().date()
    start_date = end_date - timedelta(days=days - 1)

    rows = []
    current_date = start_date

    for i in range(days):
        day_of_week = current_date.weekday()  # 0 lunes, 6 domingo
        is_weekend = 1 if day_of_week >= 5 else 0

        # comportamiento simulado
        menu_items = np.random.randint(4, 9)
        promo = np.random.choice([0, 1], p=[0.75, 0.25])

        base_orders = 8 + (4 if is_weekend else 0) + (2 if promo else 0)
        orders_count = max(1, int(np.random.normal(base_orders, 2)))

        avg_ticket = np.random.normal(8.5, 1.5)
        if is_weekend:
            avg_ticket += 1.2
        if promo:
            avg_ticket += 0.8

        total_sales = max(20, round(orders_count * avg_ticket + np.random.normal(0, 5), 2))

        rows.append({
            "date": current_date.isoformat(),
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "menu_items": menu_items,
            "promo": promo,
            "orders_count": orders_count,
            "total_sales": total_sales
        })

        current_date += timedelta(days=1)

    df = pd.DataFrame(rows)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    df = generate_synthetic_sales_dataset()
    print("Dataset generado correctamente.")
    print(df.head())