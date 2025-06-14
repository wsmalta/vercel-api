from flask import Flask, request, jsonify
import google.generativeai as genai
import yfinance as yf
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Configuração da API do Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi definida.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

# Endpoint para resposta via Gemini
@app.route("/responder", methods=["POST"])
def responder():
    data = request.get_json()
    pergunta = data.get("pergunta", "")

    if not pergunta.strip():
        return jsonify({"erro": "Pergunta não fornecida."}), 400

    try:
        resposta = model.generate_content(pergunta)
        return jsonify({"resposta": resposta.text})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Endpoint para obter dados históricos de ações
@app.route("/historico", methods=["POST"])
def historico():
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

# Endpoint para dados normalizados (comparar variações relativas)
@app.route("/normalizado", methods=["POST"])
def normalizado():
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
        result = df_all.to_dict(orient="records")
        return jsonify(result)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Endpoint de status
@app.route("/", methods=["GET"])
def home():
    return "✅ API Gemini + Yahoo Finance ativa!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
