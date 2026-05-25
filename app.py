from flask import Flask, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv
from github import Github

# 1. Configuración inicial
load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
TOKEN_KANBAN = os.environ.get("GITHUB_TOKEN_KANBAN")
g = Github(TOKEN_KANBAN)

# 2. Función para analizar tarea
@app.route('/analizar', methods=['POST'])
def analizar_tarea():
    datos = request.json
    titulo = datos.get('titulo_tarea', 'Sin título')
    mensaje = datos.get('mensaje', 'Sin mensaje')

    print(f"🏋️‍♀️ Nueva tarea del Kanban recibida: {titulo}")

    prompt = f"""
    Eres un desarrollador experto. Arregla el código basándote en este problema:
    - Título: {titulo}
    - Descripción: {mensaje}
    
    Devuelve ÚNICAMENTE el código corregido. Sin explicaciones, sin saludos, sin markdown y sin comillas. Solo el texto del código puro.
    """

    try:
        print("⚡ Consultando a Groq...")
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant"
        )
        
        texto_ia = chat_completion.choices[0].message.content.strip()
        print("✅ Código corregido generado y listo para enviar a Dataverse")
        
        return jsonify({
            "resumen_rendimiento": texto_ia,
            "status": "success"
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"resumen_rendimiento": "Error de conexión con la IA", "status": "error"}), 500

# 3. Función para subir a GitHub
@app.route('/api/autofix', methods=['POST'])
def autofix():
    try:
        datos = request.get_json()
        repo_full_name = datos.get("repositorio", "").replace("https://github.com/", "")
        path_archivo = datos.get("archivo")
        codigo_corregido = datos.get("codigo_solucion")
        ticket_id = datos.get("ticket_id", "Desconocido")

        if not repo_full_name or not path_archivo or not codigo_corregido:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        repo = g.get_repo(repo_full_name)
        archivo_existente = repo.get_contents(path_archivo)
        
        mensaje_commit = f"fix(ai-agent): resolución automática del ticket #{ticket_id}"
        
        resultado_git = repo.update_file(
            path=path_archivo,
            message=mensaje_commit,
            content=codigo_corregido,
            sha=archivo_existente.sha
        )

        return jsonify({
            "status": "success",
            "message": "Archivo corregido en GitHub con éxito.",
            "commit_url": resultado_git['commit'].html_url
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error en el Agente de GitHub: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)