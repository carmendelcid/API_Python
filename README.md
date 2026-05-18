# 🧠 Kanban Board - Motor de IA (Python)

## 📖 Descripción
Este repositorio contiene el microservicio de Inteligencia Artificial del proyecto "Kanban Board". Es una API REST ligera desarrollada en **Python con Flask** que actúa como intermediaria entre Microsoft Dataverse (vía Power Automate) y el LLM.

## 🚀 Funcionalidad
Cuando un usuario finaliza una tarea en el Kanban, recibe la información (título y descripción) y:
1. Construye un prompt especializado para el rol de analista.
2. Se comunica con la API de **Groq** utilizando el modelo **LLaMA 3 (llama-3.1-8b-instant)**.
3. Exige y procesa una respuesta estrictamente en formato JSON.
4. Devuelve el análisis de rendimiento a Dataverse para ser guardado en el registro de la tarea.

## 🔒 Seguridad
Las credenciales de la API externa (Groq) se gestionan de forma segura mediante variables de entorno locales (`.env`), las cuales están excluidas del control de versiones.

## 🛠️ Instalación local
Para levantar el servidor en local:
```bash
pip install flask groq python-dotenv
python app.py
