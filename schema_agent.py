import json
import os
from sqlalchemy import create_engine, inspect

class SchemaAgent:
    def __init__(self, db_url):
        # Creamos el motor de conexión
        self.engine = create_engine(db_url)
        # El inspector es la herramienta que "lee" la estructura de la DB
        self.inspector = inspect(self.engine)

    def generate_metadata_json(self):
        metadata = {
            "database_name": "Demo_Project_IA",
            "engine": self.engine.name,
            "tables": []
        }

        # 1. Obtenemos todas las tablas
        tables = self.inspector.get_table_names()

        for table_name in tables:
            table_info = {
                "table_name": table_name,
                "description": self._get_table_description(table_name), # Simulado
                "columns": []
            }

            # 2. Obtenemos columnas y llaves primarias
            columns = self.inspector.get_columns(table_name)
            pk_columns = self.inspector.get_pk_constraint(table_name)['constrained_columns']
            
            # 3. Obtenemos llaves foráneas (Relaciones)
            fk_info = self.inspector.get_foreign_keys(table_name)

            for col in columns:
                col_name = col['name']
                
                # Buscamos si esta columna es una llave foránea
                references = None
                for fk in fk_info:
                    if col_name in fk['constrained_columns']:
                        # Guardamos a qué tabla y columna apunta
                        idx = fk['constrained_columns'].index(col_name)
                        references = f"{fk['referred_table']}.{fk['referred_columns'][idx]}"

                column_data = {
                    "name": col_name,
                    "type": str(col['type']),
                    "is_pk": col_name in pk_columns,
                    "is_fk": references is not None,
                    "references": references,
                    "description": self._get_column_description(table_name, col_name),
                    "is_pii": self._check_if_pii(col_name) # Lógica de privacidad
                }
                table_info["columns"].append(column_data)

            metadata["tables"].append(table_info)

        return metadata

    

    def _get_table_description(self, table_name):
        descriptions = {
            "clientes": "Maestro de usuarios y clientes finales.",
            "productos": "Catálogo de productos disponibles para la venta.",
            "ventas": "Registro histórico de transacciones comerciales."
        }
        return descriptions.get(table_name, "Sin descripción disponible.")

    def _get_column_description(self, table_name, col_name):
        # Esto ayuda al LLM a no alucinar mira las columnas que existen
        return f"Campo {col_name} de la tabla {table_name}"

    def _check_if_pii(self, col_name):
        # Lógica simple de seguridad: si el nombre sugiere datos personales
        sensitive_keywords = ['email', 'telefono', 'direccion', 'password', 'nombre']
        return any(key in col_name.lower() for key in sensitive_keywords)

    def save_to_file(self, output_path):
        data = self.generate_metadata_json()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f" Metadata guardada en: {output_path}")

if __name__ == "__main__":
    # Conexión a nuestra base de datos local
    db_path = "sqlite:///data/database.db"
    agent = SchemaAgent(db_path)
    agent.save_to_file("config/schema_metadata.json")