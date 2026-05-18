from flask import Flask, request, jsonify
from groq import Groq
import json
import os
from dotenv import load_dotenv

# 1. Cargar las variables del archivo .env oculto
load_dotenv() 

app = Flask(__name__)

# 2. Conectar con Groq leyendo la clave de forma segura
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/analizar', methods=['POST'])
def analizar_tarea():
    datos = request.json
    titulo = datos.get('titulo_tarea', 'Sin título')
    mensaje = datos.get('mensaje', 'Sin mensaje')

    print(f"🏋️‍♀️ Nueva tarea del Kanban recibida: {titulo}")

    prompt = f"""
    Actúa como un analista experto. 
    Analiza esta actualización de una tarea:
    - Título: {titulo}
    - Descripción: {mensaje}

    CRÍTICO: Debes responder ÚNICA Y EXCLUSIVAMENTE con un objeto JSON válido.
    Estructura exacta:
    {{
        "resumen_rendimiento": "Tu consejo o análisis de máximo 30 palabras.",
        "status": "success"
    }}
    """

    try:
        print("⚡ Consultando a Groq...")
        
        # Llamada a Groq con el modelo actualizado
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"} 
        )
        
        texto_ia = chat_completion.choices[0].message.content
        resultado_json = json.loads(texto_ia)
        
        print("✅ Análisis de Groq enviado a Dataverse")
        return jsonify(resultado_json)

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"resumen_rendimiento": "Error de conexión con la IA", "status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)