from app import app, db, appbuilder

with app.app_context():
    # 1. Cargamos tus vistas al contexto
    from app import view
    
    # 2. Pasamos las variables internas del objeto que FAB necesita para mapear
    print("Sincronizando nuevos permisos en la base de datos...")
    appbuilder.sm.security_converge(appbuilder.baseviews, appbuilder.menu)
    print("¡Permisos actualizados con éxito!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)