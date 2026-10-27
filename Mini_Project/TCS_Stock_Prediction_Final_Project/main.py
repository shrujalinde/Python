"""
TCS Stock Price Analysis and Prediction — Mini Project
Automatically downloads real historical TCS (TCS.NS) data using yfinance.
Run: python main.py
Outputs are saved in the outputs/ folder.
"""

from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = Path(__file__).resolve().parent
OUT = BASE_DIR / "outputs"
OUT.mkdir(exist_ok=True)

def load_data():
    """Fetch real historical data. If Yahoo Finance download fails, try the public CSV."""
    try:
        import yfinance as yf
        data = yf.download("TCS.NS", start="2018-01-01", auto_adjust=False,
                           progress=False, threads=False)
        if data is not None and not data.empty:
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            data = data.reset_index()
            # Use adjusted close if available for a consistent price series.
            if "Adj Close" in data.columns:
                data["Close"] = data["Adj Close"].fillna(data["Close"])
            return data, "Yahoo Finance (TCS.NS)"
    except Exception as exc:
        print("Yahoo Finance download failed:", exc)

    url = "https://raw.githubusercontent.com/abulbasar/data/master/tcs-stock.csv"
    try:
        data = pd.read_csv(url)
        rename = {
            "Date": "Date", "Close Price": "Close", "Open Price": "Open",
            "High Price": "High", "Low Price": "Low",
            "Total Traded Quantity": "Volume"
        }
        data = data.rename(columns=rename)
        required = {"Date", "Close"}
        if not required.issubset(data.columns):
            raise ValueError(f"CSV columns did not match expected fields: {list(data.columns)}")
        return data, "Public GitHub TCS historical CSV"
    except Exception as exc:
        raise RuntimeError(
            "Could not download the real dataset. Connect to the internet and try again. "
            "The program downloads data automatically; no manual CSV download is needed.\n"
            f"Details: {exc}"
        )

def main():
    raw, source = load_data()
    print(f"Dataset source: {source}")
    print("\nRaw preview:")
    print(raw.head())
    print(f"\nRaw rows and columns: {raw.shape}")

    # Normalize column names and parse dates/numeric fields.
    raw.columns = [str(c).strip() for c in raw.columns]
    date_col = next((c for c in raw.columns if c.lower() == "date"), None)
    close_col = next((c for c in raw.columns if c.lower() in ("close", "close price")), None)
    if date_col is None or close_col is None:
        raise ValueError(f"Required Date/Close columns not found. Columns: {list(raw.columns)}")

    df = raw.copy()
    # df[date_col] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
    df[date_col] = pd.to_datetime(
    df[date_col].astype(str).str.strip(),
    errors="coerce",
    format="mixed",
    dayfirst=True
)
    for c in df.columns:
        if c != date_col:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=[date_col, close_col])
    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates().sort_values(date_col).reset_index(drop=True)

    # Rename the core fields to standard names.
    df = df.rename(columns={date_col: "Date", close_col: "Close"})
    if "Volume" not in df.columns:
        volume_col = next((c for c in df.columns if "volume" in c.lower() or "traded quantity" in c.lower()), None)
        if volume_col:
            df = df.rename(columns={volume_col: "Volume"})
    if "Volume" in df.columns:
        df["Volume"] = df["Volume"].fillna(df["Volume"].median())

    print("\nPreprocessing summary")
    print("Rows after removing invalid dates/close and duplicates:", len(df))
    print("Duplicate rows identified before removal:", duplicate_count)
    print("Missing values after cleaning:\n", df.isnull().sum())

    df.to_csv(OUT / "cleaned_tcs_stock.csv", index=False)
    print("\nDescriptive statistics:\n", df[["Close"]].describe())

    # Visualization 1: closing-price trend
    plt.figure(figsize=(11, 5))
    plt.plot(df["Date"], df["Close"], linewidth=1.2)
    plt.title("TCS Historical Closing Price")
    plt.xlabel("Date"); plt.ylabel("Price (INR)")
    plt.grid(alpha=0.25); plt.tight_layout()
    plt.savefig(OUT / "01_closing_price_trend.png", dpi=220); plt.close()

    # Visualization 2: volume trend if available
    if "Volume" in df.columns:
        plt.figure(figsize=(11, 5))
        plt.plot(df["Date"], df["Volume"], linewidth=1)
        plt.title("TCS Trading Volume")
        plt.xlabel("Date"); plt.ylabel("Volume")
        plt.grid(alpha=0.25); plt.tight_layout()
        plt.savefig(OUT / "02_trading_volume.png", dpi=220); plt.close()

    # Visualization 3: correlation heatmap for available OHLC numeric columns
    ohlc = [c for c in ["Open", "High", "Low", "Close"] if c in df.columns]
    if len(ohlc) >= 2:
        plt.figure(figsize=(7, 5))
        sns.heatmap(df[ohlc].corr(), annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
        plt.title("Correlation Heatmap of Stock Prices")
        plt.tight_layout()
        plt.savefig(OUT / "03_correlation_heatmap.png", dpi=220); plt.close()

    # Feature engineering: use only information available up to current session.
    model_df = df[["Date", "Close"]].copy()
    model_df["Lag_1"] = model_df["Close"].shift(1)
    model_df["Lag_2"] = model_df["Close"].shift(2)
    model_df["Lag_3"] = model_df["Close"].shift(3)
    model_df["Moving_Average_5"] = model_df["Close"].shift(1).rolling(5).mean()
    model_df["Target_Next_Close"] = model_df["Close"].shift(-1)
    model_df = model_df.dropna().reset_index(drop=True)

    features = ["Lag_1", "Lag_2", "Lag_3", "Moving_Average_5"]
    X, y = model_df[features], model_df["Target_Next_Close"]
    split = int(len(model_df) * 0.8)
    if split < 20 or len(model_df) - split < 5:
        raise ValueError("Not enough valid observations to train and test the model.")

    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    test_dates = model_df["Date"].iloc[split:]

    model = LinearRegression()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    mse = mean_squared_error(y_test, pred)
    rmse = float(np.sqrt(mse))
    r2 = r2_score(y_test, pred)

    # Baseline: use the most recent close as the next-session prediction.
    baseline_pred = X_test["Lag_1"].to_numpy()
    baseline_mae = mean_absolute_error(y_test, baseline_pred)

    metrics = pd.DataFrame([
        {"Metric": "MAE", "Linear Regression": mae, "Last-close baseline": baseline_mae},
        {"Metric": "MSE", "Linear Regression": mse, "Last-close baseline": mean_squared_error(y_test, baseline_pred)},
        {"Metric": "RMSE", "Linear Regression": rmse, "Last-close baseline": np.sqrt(mean_squared_error(y_test, baseline_pred))},
        {"Metric": "R-squared", "Linear Regression": r2, "Last-close baseline": r2_score(y_test, baseline_pred)}
    ])
    metrics.to_csv(OUT / "model_metrics.csv", index=False)

    results = pd.DataFrame({
        "Date": test_dates.to_numpy(),
        "Actual_Next_Close": y_test.to_numpy(),
        "Predicted_Next_Close": pred,
        "Last_Close_Baseline": baseline_pred
    })
    results.to_csv(OUT / "prediction_results.csv", index=False)

    plt.figure(figsize=(11, 5))
    plt.plot(results["Date"], results["Actual_Next_Close"], label="Actual", linewidth=1.5)
    plt.plot(results["Date"], results["Predicted_Next_Close"], label="Linear Regression", linewidth=1.2)
    plt.plot(results["Date"], results["Last_Close_Baseline"], label="Last-close baseline", linewidth=1, alpha=0.8)
    plt.title("Actual vs Predicted Next-Session Closing Price")
    plt.xlabel("Date"); plt.ylabel("Price (INR)")
    plt.legend(); plt.grid(alpha=0.25); plt.xticks(rotation=35)
    plt.tight_layout()
    plt.savefig(OUT / "04_actual_vs_predicted.png", dpi=220); plt.close()

    latest = df.sort_values("Date").reset_index(drop=True)
    last_five = latest["Close"].tail(5)
    next_features = pd.DataFrame([{
        "Lag_1": latest["Close"].iloc[-1],
        "Lag_2": latest["Close"].iloc[-2],
        "Lag_3": latest["Close"].iloc[-3],
        "Moving_Average_5": last_five.mean()
    }])
    next_estimate = float(model.predict(next_features[features])[0])

    print("\n========== MODEL RESULTS ==========")
    print(f"Observations used for modeling: {len(model_df)}")
    print(f"Training rows: {len(X_train)} | Testing rows: {len(X_test)}")
    print(f"MAE: {mae:.4f}")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R-squared: {r2:.4f}")
    print(f"Last-close baseline MAE: {baseline_mae:.4f}")
    print(f"Latest date in dataset: {latest['Date'].iloc[-1].date()}")
    print(f"Estimated next trading-day close (educational estimate): INR {next_estimate:.2f}")
    print(f"\nAll generated files are in: {OUT}")
    print("Note: This is a learning project, not an investment recommendation.")

if __name__ == "__main__":
    main()
