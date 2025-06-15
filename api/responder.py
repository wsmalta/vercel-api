import json
import os
import google.generativeai as genai

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY não definido")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"erro": "Método não permitido"}),
            "headers": {"Content-Type": "application/json"}
        }

    try:
        body = request.get_json()
        pergunta = body.get("pergunta", "").strip()

        if not pergunta:
            return {
                "statusCode": 400,
                "body": json.dumps({"erro": "Pergunta não fornecida"}),
                "headers": {"Content-Type": "application/json"}
            }

        resposta = model.generate_content(pergunta)

        return {
            "statusCode": 200,
            "body": json.dumps({"resposta": resposta.text}),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"erro": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }


