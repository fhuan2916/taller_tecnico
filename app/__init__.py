# from flask import Flask
# from flask_appbuilder import AppBuilder, SQLA

# app = Flask(__name__)
# app.config.from_object("config")

# # 1. Inicializamos la base de datos primero
# db = SQLA(app)

# # 2. Inicializamos el generador de interfaces
# appbuilder = AppBuilder(app, db.session)

# # 3. AL FINAL ABSOLUTO importamos los modelos y vistas
# from . import models, views

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA

app = Flask(__name__)
app.config.from_object("config")

db = SQLA(app)
appbuilder = AppBuilder(app, db.session)

# IMPORTANTE: Solo importa models aquí para romper el bucle con views
from . import models