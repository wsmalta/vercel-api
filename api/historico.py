import yfinance as yf
from datetime import datetime
import json

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"erro": "Método não permitido"}),
            "headers": {"Content-Type": "application/json"}
        }

    try:
        data = request.json
    except Exception:
        return {
            "statusCode": 400,
            "body": json.dumps({"erro": "JSON inválido"}),
            "headers": {"Content-Type": "application/json"}
        }

    tickers = data.get("tickers", [])
    start_date = data.get("inicio", "")
    end_date = data.get("fim", datetime.now().strftime("%Y-%m-%d"))

    if not tickers or not start_date:
        return {
            "statusCode": 400,
            "body": json.dumps({"erro": "Campos 'tickers' e 'inicio' são obrigatórios."}),
            "headers": {"Content-Type": "application/json"}
        }

    try:
        result = {}
        for ticker in tickers:
            df = yf.download(ticker, start=start_date, end=end_date)
            df.reset_index(inplace=True)
            # Transformar datas em string para JSON serializável
            records = []
            for row in df.itertuples():
                records.append({
                    "Date": row.Date.strftime("%Y
