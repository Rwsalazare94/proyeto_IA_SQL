import sqlite3
import pandas as pd
import os
import re
from query_agent import SQLOrchestrator

def limpiar_sql(texto_sql):
    """Elimina las etiquetas ```sql y espacios extra para que SQLite no falle"""
    limpio = re.sub(r'```sql|```', '', texto_sql)
    return limpio.strip()

def ejecutar_consulta_ia():
    # 1. Definir rutas absolutas
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "data", "database.db")
    
    # 2. Iniciar el orquestador de IA
    # Nota: Asegúrate de que el JSON esté en la carpeta config
    orchestrator = SQLOrchestrator("config/schema_metadata.json")
    
    print("\n---  AGENTE DE DATOS ACTIVO ---")
    pregunta = input("¿Qué información necesitas de la base de datos?: ")
    
    try:
        # 3. Generar el SQL con Gemini
        sql_generado = orchestrator.generate_sql(pregunta)
        sql_limpio = limpiar_sql(sql_generado)
        
        print(f"\n SQL que voy a ejecutar: \n{sql_limpio}")
        
        # 4. Conectar a SQLite y ejecutar con Pandas
        conn = sqlite3.connect(db_path)
        # Pandas convierte automáticamente el resultado en una tabla (DataFrame)
        df = pd.read_sql_query(sql_limpio, conn)
        conn.close()
        
        # 5. Mostrar resultados
        if df.empty:
            print("\n La consulta se ejecutó pero no encontró datos.")
        else:
            print("\n RESULTADOS:")
            print("=" * 50)
            print(df.to_string(index=False)) # Imprime la tabla sin el índice de filas
            print("=" * 50)
            
    except Exception as e:
        print(f"\n Ups, algo salió mal: {e}")

if __name__ == "__main__":
    ejecutar_consulta_ia()