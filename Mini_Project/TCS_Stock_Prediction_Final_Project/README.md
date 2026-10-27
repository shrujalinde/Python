# TCS Stock Price Analysis and Prediction — Ready-to-Run Mini Project

## What is included
- `main.py`: downloads real TCS stock data automatically, preprocesses it, creates visualizations, trains Linear Regression, evaluates it against a simple baseline, and saves outputs.
- `requirements.txt`: required Python packages.
- `Mini_Project_Report.docx`: project report with methodology, algorithm, metric explanations, references, and places to insert the actual results after running the program.
- `REFERENCES.md`: source links.

## Run it
1. Extract the ZIP.
2. Open the extracted folder in VS Code.
3. In the VS Code terminal, run:
   `python -m pip install -r requirements.txt`
4. Run:
   `python main.py`
5. Open the `outputs` folder. Use the actual numbers in `model_metrics.csv` to complete the results table in the report.

The program first tries Yahoo Finance (`TCS.NS`) using `yfinance`; if that fails, it tries the public GitHub CSV source. An internet connection is required to fetch the real-world data.

## Outputs created automatically
- `cleaned_tcs_stock.csv`
- `model_metrics.csv`
- `prediction_results.csv`
- `01_closing_price_trend.png`
- `02_trading_volume.png` (if volume is present)
- `03_correlation_heatmap.png` (if OHLC fields are available)
- `04_actual_vs_predicted.png`

## Important
Do not invent or copy model metrics from another project. Run the code and report the results it prints for your dataset. Stock prices are uncertain; this basic model is for education only and is not a financial forecasting service.
