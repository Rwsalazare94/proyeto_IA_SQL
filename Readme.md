#  AI SQL Agent: Text-to-SQL Generator

Este proyecto es un **Agente de IA Generativa** capaz de interactuar con bases de datos relacionales utilizando lenguaje natural. El sistema traduce preguntas humanas a consultas SQL precisas y devuelve los resultados de forma estructurada.

##  Características
- **Traducción Semántica:** Convierte lenguaje natural a SQL complejo (JOINs, agregaciones, filtros).
- **Mapeo de Metadatos:** Utiliza un archivo `schema_metadata.json` para dar contexto al modelo y evitar errores de nombres de columnas.
- **Visualización:** Integración con **Pandas** para mostrar los resultados en tablas limpias.
- **Seguridad:** Implementación de archivos `.gitignore` para proteger credenciales y variables de entorno.

##  Tech Stack
- **Lenguaje:** Python 3.11
- **Modelo de IA:** Google gemini-2.5-flash-lite
- **Base de Datos:** SQLite
- **Librerías Clave:** `google-genai`, `pandas`, `python-dotenv`

## 📁 Estructura del Proyecto
- `src/query_agent.py`: El "cerebro" que genera el SQL.
- `src/executor_agent.py`: Orquesta la entrada del usuario y la ejecución en la DB.
- `config/schema_metadata.json`: Definición del esquema de la base de datos.
- `setup_db.py`: Script para crear y poblar la base de datos de prueba.

## ⚙️ Instalación
1. Clona el repositorio.
2. Crea un archivo `.env` con tu `GEMINI_API_KEY`.
3. Ejecuta `python setup_db.py` para crear la base de datos.
4. Inicia el agente con `python src/executor_agent.py`.