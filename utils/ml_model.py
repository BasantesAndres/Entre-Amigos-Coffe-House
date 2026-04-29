import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


MODEL_PATH = "models/mlp_sales_model.pkl"
DATA_PATH = "data/sales_history.csv"


def load_dataset(path=DATA_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el dataset en {path}")
    df = pd.read_csv(path)
    return df


def prepare_features(df: pd.DataFrame):
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # lags
    df["lag_1"] = df["total_sales"].shift(1)
    df["lag_2"] = df["total_sales"].shift(2)
    df["lag_3"] = df["total_sales"].shift(3)
    df["rolling_mean_3"] = df["total_sales"].rolling(3).mean().shift(1)

    df = df.dropna().reset_index(drop=True)

    feature_cols = [
        "day_of_week",
        "is_weekend",
        "menu_items",
        "promo",
        "orders_count",
        "lag_1",
        "lag_2",
        "lag_3",
        "rolling_mean_3"
    ]

    X = df[feature_cols]
    y = df["total_sales"]

    return df, X, y, feature_cols


def train_mlp_model():
    df = load_dataset()
    prepared_df, X, y, feature_cols = prepare_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = MLPRegressor(
        hidden_layer_sizes=(64, 32),
        activation="relu",
        solver="adam",
        max_iter=1000,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    os.makedirs("models", exist_ok=True)
    joblib.dump({
        "model": model,
        "feature_cols": feature_cols
    }, MODEL_PATH)

    return {
        "model": model,
        "feature_cols": feature_cols,
        "df_prepared": prepared_df,
        "X_test": X_test,
        "y_test": y_test,
        "y_pred": y_pred,
        "mae": mae,
        "rmse": rmse
    }


def load_trained_model():
    if not os.path.exists(MODEL_PATH):
        return None
    return joblib.load(MODEL_PATH)


def forecast_next_days(days=7):
    saved = load_trained_model()
    if saved is None:
        raise FileNotFoundError("No existe un modelo entrenado todavía.")

    model = saved["model"]

    df = load_dataset()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    history = df.copy()
    predictions = []

    for _ in range(days):
        last_date = history["date"].iloc[-1]
        next_date = last_date + pd.Timedelta(days=1)

        day_of_week = next_date.weekday()
        is_weekend = 1 if day_of_week >= 5 else 0

        # asumimos valores operativos esperados
        menu_items = int(round(history["menu_items"].tail(7).mean()))
        promo = 1 if np.random.rand() < 0.25 else 0
        orders_count = int(round(history["orders_count"].tail(7).mean()))

        lag_1 = history["total_sales"].iloc[-1]
        lag_2 = history["total_sales"].iloc[-2]
        lag_3 = history["total_sales"].iloc[-3]
        rolling_mean_3 = history["total_sales"].tail(3).mean()

        X_new = pd.DataFrame([{
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "menu_items": menu_items,
            "promo": promo,
            "orders_count": orders_count,
            "lag_1": lag_1,
            "lag_2": lag_2,
            "lag_3": lag_3,
            "rolling_mean_3": rolling_mean_3
        }])

        pred = float(model.predict(X_new)[0])
        pred = round(max(pred, 0), 2)

        predictions.append({
            "date": next_date.date().isoformat(),
            "predicted_sales": pred
        })

        new_row = {
            "date": next_date,
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "menu_items": menu_items,
            "promo": promo,
            "orders_count": orders_count,
            "total_sales": pred
        }
        history = pd.concat([history, pd.DataFrame([new_row])], ignore_index=True)

    return pd.DataFrame(predictions)