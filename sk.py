import os
import secrets

# Generar una clave secreta segura
secret_key = secrets.token_hex(16)
print(secret_key)
