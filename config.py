import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Configuración obligatoria de Flask
SECRET_KEY = "una_clave_secreta_muy_segura_para_el_examen"

# Conexión a la Base de Datos usando SQLAlchemy
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuraciones de Flask-AppBuilder
APP_NAME = "Taller Técnico Oruro"
APP_THEME = "cyborg.css"  # Tema visual por defecto

# Habilitar la gestión de usuarios y roles nativa
AUTH_TYPE = 1  # Autenticación basada en Base de Datos (Login/Logout)

# 1. Definir el idioma por defecto de la aplicación
BABEL_DEFAULT_LOCALE = "es"

# 2. Habilitar los idiomas que el sistema va a soportar (puedes dejar solo español o ambos)
LANGUAGES = {
    "es": {"flag": "bo", "name": "Español"},
    "en": {"flag": "us", "name": "English"},
}