import os
from dotenv import load_dotenv

print(f" Directorio actual: {os.getcwd()}")
print(f" ¿Existe el archivo .env aquí?: {os.path.exists('.env')}")

load_dotenv()
key = os.getenv("GOOGLE_API_KEY")

if key:
    print(f" ¡ÉXITO! Llave encontrada: {key[:10]}...")
else:
    print("ERROR: La llave sigue sin aparecer.")
    print("Contenido de la carpeta actual:", os.listdir('.'))