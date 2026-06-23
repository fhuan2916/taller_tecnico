from app import app, appbuilder, db
from flask_appbuilder.security.sqla.models import User

with app.app_context():
    # Buscamos el rol de Administrador
    admin_role = appbuilder.sm.find_role(appbuilder.sm.auth_role_admin)
    
    # Crea tus credenciales aquí (Cámbialas si gustas)
    username = "admin"
    email = "admin@tallertecnico.com"
    password = "AdminPassword123"
    
    # Verificamos si ya existe para no duplicarlo
    if not appbuilder.sm.find_user(username=username):
        user = appbuilder.sm.add_user(
            username=username,
            first_name="Juan",
            last_name="Diego",
            email=email,
            role=admin_role,
            password=password
        )
        if user:
            print("=========================================")
            print("¡ADMINISTRADOR CREADO CON ÉXITO!")
            print(f"Usuario: {username}")
            print(f"Contraseña: {password}")
            print("=========================================")
        else:
            print("No se pudo crear el usuario.")
    else:
        print("El usuario admin ya existe.")