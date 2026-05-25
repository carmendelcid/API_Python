import os
import base64
from flask import Flask, request, jsonify
from github import Github
from dotenv import load_dotenv

# 1. Cargamos el archivo .env para leer las llaves secretas
load_dotenv()

app = Flask(__name__)

# 2. Conectamos con GitHub usando tu NUEVO token del .env
TOKEN_KANBAN = os.getenv("GITHUB_TOKEN_KANBAN")
g = Github(TOKEN_KANBAN)

@app.route('/api/autofix', methods=['POST'])
def autofix():
    try:
        # 3. Recibir los datos que nos envía Power Automate
        datos = request.get_json()
        
        repo_full_name = datos.get("repositorio")     # Ej: "TuUsuario/Empresa-Simulada-Tickets"
        path_archivo = datos.get("archivo")           # Ej: "config.json"
        codigo_corregido = datos.get("codigo_solucion") # El código arreglado por el LLM
        ticket_id = datos.get("ticket_id", "Desconocido")

        # Validación de seguridad por si falta algún dato
        if not repo_full_name or not path_archivo or not codigo_corregido:
            return jsonify({"error": "Faltan datos obligatorios (repositorio, archivo o codigo_solucion)"}), 400

        # 4. Apuntar al repositorio de GitHub
        repo = g.get_repo(repo_full_name)

        # 5. Buscar el archivo original en GitHub para obtener su SHA (su huella digital)
        try:
            archivo_existente = repo.get_contents(path_archivo)
            sha_original = archivo_existente.sha
        except Exception:
            return jsonify({"error": f"No se encontró el archivo '{path_archivo}' en el repositorio"}), 404

        # 6. HACER EL COMMIT: El agente escribe el cambio directamente en GitHub
        mensaje_commit = f"fix(ai-agent): resolución automática del ticket #{ticket_id}"
        
        repo.update_file(
            path=path_archivo,
            message=mensaje_commit,
            content=codigo_corregido,
            sha=sha_original
        )

        # Si todo sale bien, respondemos con un éxito
        return jsonify({
            "status": "success",
            "message": f"¡Archivo '{path_archivo}' corregido y guardado en GitHub con éxito!"
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error crítico en el Agente de GitHub: {str(e)}"}), 500

if __name__ == '__main__':
    # Arrancamos el servidor en el puerto 5000
    app.run(port=5000, debug=True)