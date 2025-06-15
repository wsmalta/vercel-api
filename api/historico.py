from flask import Request, jsonify
import yfinance as yf
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
        result = {}
        for ticker in tickers:
            df = yf.download(ticker, start=start_date, end=end_date)
            df.reset_index(inplace=True)
            result[ticker] = df[["Date", "Close"]].to_dict(orient="records")
        return jsonify(result)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
