# 🤖 Kanban Board - Agente de IA y Despliegue Autónomo (Python Backend)

## 📖 Descripción

Este repositorio aloja el microservicio de Inteligencia Artificial y automatización del proyecto "Kanban Board". Es una API REST ligera desarrollada en Python con Flask que actúa como el "cerebro desarrollador" del sistema, conectando de forma transversal Microsoft Dataverse (a través de Power Automate) con el LLM de Groq y la API de GitHub.

El servicio ha evolucionado de ser un asistente analítico a convertirse en un **Agente Autónomo de Corrección de Bugs (Bug-Fixing Agent)** que opera bajo un modelo de supervisión humana (*Human-in-the-Loop*).

## 🚀 Funcionalidades Principales

El backend expone dos endpoints críticos que gestionan el ciclo de vida de la resolución del código:

1. **`/analizar` (Análisis y Corrección Zero-Shot):**
   * Recibe el reporte del bug de la tarea del Kanban (título y descripción).
   * Procesa la información mediante la API de Groq utilizando el modelo **LLaMA 3.1 (llama-3.1-8b-instant)**.
   * Devuelve un JSON limpio empaquetado por Python que contiene *única y exclusivamente* el código reparado y funcional, listo para ser inyectado en Dataverse sin interferencias de formato.

2. **`/api/autofix` (Integración con Git y Despliegue Automático):**
   * Se activa inmediatamente cuando el usuario aprueba la solución arrastrando la tarjeta a "Finalizado".
   * Conecta con la **API de GitHub (PyGithub)** utilizando autenticación segura.
   * Localiza el repositorio y el archivo destino indicados dinámicamente desde la tarjeta de Dataverse.
   * Realiza un commit automatizado (`update_file`) aplicando el parche de código y devuelve la **URL pública del commit** para asegurar una trazabilidad total.

## 🔒 Seguridad y Buenas Prácticas (DevSecOps)

Siguiendo estándares profesionales de seguridad en el software, todas las credenciales sensibles están estrictamente aisladas del código fuente mediante un archivo local `.env` (ignorado en el control de versiones por el `.gitignore`):

* `GROQ_API_KEY`: Llave de acceso para la ejecución de inferencias en el LLM.
* `GITHUB_TOKEN_KANBAN`: Personal Access Token (PAT) con permisos restringidos para la gestión y actualización del código en el repositorio objetivo.

## 🛠️ Instalación y Despliegue Local

### Requisitos Previos
* Python 3.x instalado.
* Archivo `.env` configurado en la raíz con las claves correspondientes.

### Pasos para ejecutar:

```bash
# 1. Instalar las dependencias del microservicio (incluyendo PyGithub)
pip install flask groq python-dotenv PyGithub

# O de forma alternativa mediante el archivo de requerimientos:
pip install -r requirements.txt

# 2. Levantar el entorno de desarrollo local (Puerto 5000)
python app.py
