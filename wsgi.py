import sys
import site
import os

# Añade el sitio-packages del entorno virtual al path
site.addsitedir('/proyectos/sgti/venv/lib/python3.8/site-packages')

# Añade la carpeta del proyecto al path
sys.path.insert(0, "/proyectos/sgti")

from app import app as application
