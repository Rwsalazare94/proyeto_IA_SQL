import sqlite3
import os

def create_database():
    # Aseguramos que se cree en la carpeta 'data'
    if not os.path.exists('data'):
        os.makedirs('data')
    
    db_path = os.path.join('data', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Crear tablas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            precio REAL,
            stock INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            ciudad TEXT
        )
    ''')

    # 2. Insertar datos de prueba
    productos = [
        (1, 'Laptop Gaming', 1200.50, 10),
        (2, 'Mouse Inalámbrico', 25.00, 50),
        (3, 'Monitor 4K', 350.00, 15),
        (4, 'Teclado Mecánico', 80.00, 20),
        (5, 'Auriculares Pro', 150.00, 30)
    ]

    clientes = [
        (1, 'Juan Pérez', 'Madrid'),
        (2, 'Maria García', 'Barcelona'),
        (3, 'Carlos López', 'Valencia')
    ]

    cursor.executemany('INSERT OR REPLACE INTO productos VALUES (?,?,?,?)', productos)
    cursor.executemany('INSERT OR REPLACE INTO clientes VALUES (?,?,?)', clientes)

    conn.commit()
    conn.close()
    print("✅ Base de datos creada y poblada con datos de éxito.")

if __name__ == "__main__":
    create_database()