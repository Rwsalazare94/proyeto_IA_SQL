import os
import json
from google import genai
from dotenv import load_dotenv

# --- Lógica de Rutas Inteligente ---
# Obtenemos la ruta de la carpeta donde está ESTE script (src/)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Subimos un nivel para llegar a la raíz del proyecto (proyecto_IA_SQL/)
root_dir = os.path.dirname(script_dir)

# 1. Cargamos el .env desde la raíz
load_dotenv(os.path.join(root_dir, '.env'))
api_key = os.getenv("GOOGLE_API_KEY")

class SQLOrchestrator:
    def __init__(self, metadata_path):
        # Usamos la ruta absoluta para el JSON
        full_metadata_path = os.path.join(root_dir, metadata_path)
        
        if not api_key:
            raise ValueError("No se encontró la API KEY en el archivo .env")
            
        self.client = genai.Client(api_key=api_key)
        
        with open(full_metadata_path, 'r', encoding='utf-8') as f:
            self.metadata = json.dumps(json.load(f), indent=2)

    def generate_sql(self, user_question):
        # Este es el ID más estable y con mejor cuota gratuita
        model_id = 'gemini-2.5-flash-lite' 
        
        prompt = f"""
        Eres un Experto en SQL. Genera SOLO el código SQL para esta pregunta:
        Pregunta: {user_question}
        Esquema: {self.metadata}
        """

        response = self.client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        return response.text.strip()

if __name__ == "__main__":
    # La ruta ahora es relativa a la raíz del proyecto
    orchestrator = SQLOrchestrator("config/schema_metadata.json")
    
    pregunta = "¿Cuántos productos tenemos?"
    sql = orchestrator.generate_sql(pregunta)
    
    print("\n✅ GEMINI RESPONDIÓ:")
    print("-" * 40)
    print(sql)
    print("-" * 40)