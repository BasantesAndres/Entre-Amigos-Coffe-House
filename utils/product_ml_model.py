import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


DATA_PATH = "data/product_sales_history.csv"
MODEL_PATH = "models/product_mlp_model.pkl"


def load_product_dataset(path=DATA_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el dataset en {path}")
    return pd.read_csv(path)


def prepare_product_features(df: pd.DataFrame):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["product_name", "date"]).reset_index(drop=True)

    df["category_code"] = df["category"].astype("category").cat.codes
    df["product_code"] = df["product_name"].astype("category").cat.codes

    df["lag_1"] = df.groupby("product_name")["units_sold"].shift(1)
    df["lag_2"] = df.groupby("product_name")["units_sold"].shift(2)
    df["lag_3"] = df.groupby("product_name")["units_sold"].shift(3)
    df["rolling_mean_3"] = (
        df.groupby("product_name")["units_sold"]
        .rolling(3)
        .mean()
        .shift(1)
        .reset_index(level=0, drop=True)
    )

    df = df.dropna().reset_index(drop=True)

    feature_cols = [
        "day_of_week",
        "is_weekend",
        "promo",
        "price",
        "category_code",
        "product_code",
        "lag_1",
        "lag_2",
        "lag_3",
        "rolling_mean_3"
    ]

    X = df[feature_cols]
    y = df["units_sold"]

    product_mapping = (
        df[["product_name", "product_code", "category", "category_code", "price"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return df, X, y, feature_cols, product_mapping


def train_product_mlp_model():
    df = load_product_dataset()
    prepared_df, X, y, feature_cols, product_mapping = prepare_product_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = MLPRegressor(
        hidden_layer_sizes=(64, 32),
        activation="relu",
        solver="adam",
        max_iter=1200,
        random_state=42
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    os.makedirs("models", exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "feature_cols": feature_cols,
            "product_mapping": product_mapping
        },
        MODEL_PATH
    )

    return {
        "model": model,
        "feature_cols": feature_cols,
        "product_mapping": product_mapping,
        "df_prepared": prepared_df,
        "X_test": X_test,
        "y_test": y_test,
        "y_pred": y_pred,
        "mae": mae,
        "rmse": rmse
    }


def load_trained_product_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def forecast_product_next_days(product_name: str, days=7):
    saved = load_trained_product_model()
    if saved is None:
        raise FileNotFoundError("No existe un modelo entrenado.")

    model = saved["model"]
    product_mapping = saved["product_mapping"]

    df = load_product_dataset()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["product_name", "date"]).reset_index(drop=True)

    if product_name not in df["product_name"].unique():
        raise ValueError(f"Producto no encontrado: {product_name}")

    product_history = df[df["product_name"] == product_name].copy().reset_index(drop=True)
    mapping_row = product_mapping[product_mapping["product_name"] == product_name].iloc[0]

    predictions = []

    for _ in range(days):
        last_date = product_history["date"].iloc[-1]
        next_date = last_date + pd.Timedelta(days=1)

        day_of_week = next_date.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0
        promo = 0
        price = float(mapping_row["price"])
        category_code = int(mapping_row["category_code"])
        product_code = int(mapping_row["product_code"])

        lag_1 = product_history["units_sold"].iloc[-1]
        lag_2 = product_history["units_sold"].iloc[-2]
        lag_3 = product_history["units_sold"].iloc[-3]
        rolling_mean_3 = product_history["units_sold"].tail(3).mean()

        X_new = pd.DataFrame([{
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "promo": promo,
            "price": price,
            "category_code": category_code,
            "product_code": product_code,
            "lag_1": lag_1,
            "lag_2": lag_2,
            "lag_3": lag_3,
            "rolling_mean_3": rolling_mean_3
        }])

        pred = float(model.predict(X_new)[0])
        pred = max(0, round(pred, 2))

        predictions.append({
            "date": next_date.date().isoformat(),
            "product_name": product_name,
            "predicted_units": pred
        })

        new_row = pd.DataFrame([{
            "date": next_date,
            "product_name": product_name,
            "category": mapping_row["category"],
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "promo": promo,
            "price": price,
            "units_sold": pred
        }])

        product_history = pd.concat([product_history, new_row], ignore_index=True)

    return pd.DataFrame(predictions)


def forecast_all_products_next_days(days=7):
    df = load_product_dataset()
    product_names = sorted(df["product_name"].unique())

    all_predictions = []
    for product_name in product_names:
        pred_df = forecast_product_next_days(product_name, days=days)
        total_units = pred_df["predicted_units"].sum()
        tomorrow_units = pred_df.iloc[0]["predicted_units"]

        all_predictions.append({
            "product_name": product_name,
            "tomorrow_prediction": round(float(tomorrow_units), 2),
            "next_days_total": round(float(total_units), 2)
        })

    return pd.DataFrame(all_predictions).sort_values(
        "next_days_total", ascending=False
    ).reset_index(drop=True)