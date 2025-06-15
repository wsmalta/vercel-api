from flask import Request, jsonify
import yfinance as yf
import pandas as pd
from datetime import datetime

def handler(request: Request):
    if request.method != "POST":
        return jsonify({"erro": "Método não permitido"}), 405

    data = request.get_json()
    tickers = data.get("tickers", [])
    start_date = data.get("inicio", "")
    end_date = data.get("fim", datetime.now().strftime("%Y-%m-%d"))

    if not tickers or not start_date:
        return jsonify({"erro": "Campos 'tickers' e 'inicio' são obrigatórios."}), 400

    try:
        df_all = pd.DataFrame()
        for ticker in tickers:
            df = yf.download(ticker, start=start_date, end=end_date)
            if not df.empty:
                df["Normalized"] = df["Close"] / df["Close"].iloc[0]
                df_all[ticker] = df["Normalized"]
        df_all.reset_index(inplace=True)
        return jsonify(df_all.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
