import json
import yfinance as yf
import pandas as pd
from datetime import datetime

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"erro": "Método não permitido"}),
            "headers": {"Content-Type": "application/json"}
        }

    try:
        data = request.get_json()
        tickers = data.get("tickers", [])
        start_date = data.get("inicio", "")
        end_date = data.get("fim", datetime.now().strftime("%Y-%m-%d"))

        if not tickers or not start_date:
            return {
                "statusCode": 400,
                "body": json.dumps({"erro": "Campos 'tickers' e 'inicio' são obrigatórios."}),
                "headers": {"Content-Type": "application/json"}
            }

        df_all = pd.DataFrame()
        for ticker in tickers:
            df = yf.download(ticker, start=start_date, end=end_date)
            if not df.empty:
                df["Normalized"] = df["Close"] / df["Close"].iloc[0]
                df_all[ticker] = df["Normalized"]

        df_all.reset_index(inplace=True)
        result = df_all.to_dict(orient="records")

        return {
            "statusCode": 200,
            "body": json.dumps(result),
            "headers": {"Content-Type": "application/json"}
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"erro": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }


