from flask import Request, jsonify
import google.generativeai as genai
import os

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY não definido")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

def handler(request: Request):
    if request.method != "POST":
        return jsonify({"erro": "Método não permitido"}), 405

    data = request.get_json()
    pergunta = data.get("pergunta", "")

    if not pergunta:
        return jsonify({"erro": "Pergunta não fornecida"}), 400

    try:
        resposta = model.generate_content(pergunta)
        return jsonify({"resposta": resposta.text})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

