# from flask_appbuilder import ModelView
# from flask_appbuilder.models.sqla.interface import SQLAInterface
# from .models import Cliente, Equipo, OrdenServicio, RepuestoDetalle, ServicioPrestado, Cobro
# from app import appbuilder

# class ClienteView(ModelView):
#     datamodel = SQLAInterface(Cliente)
#     list_columns = ['nombre', 'telefono', 'correo']

# class EquipoView(ModelView):
#     datamodel = SQLAInterface(Equipo)
#     list_columns = ['tipo', 'marca', 'modelo', 'cliente.nombre']

# class OrdenServicioView(ModelView):
#     datamodel = SQLAInterface(OrdenServicio)
#     list_columns = ['id', 'fecha_ingreso', 'equipo.cliente.nombre', 'estado']

# class RepuestoDetalleView(ModelView):
#     datamodel = SQLAInterface(RepuestoDetalle)

# class ServicioPrestadoView(ModelView):
#     datamodel = SQLAInterface(ServicioPrestado)

# class CobroView(ModelView):
#     datamodel = SQLAInterface(Cobro)
#     list_columns = ['orden_id', 'monto_total', 'estado_pago', 'metodo_pago']

# # Registro en el menú de la aplicación
# appbuilder.add_view(ClienteView, "Clientes", icon="fa-users", category="Gestion")
# appbuilder.add_view(EquipoView, "Equipos", icon="fa-laptop", category="Gestion")
# appbuilder.add_view(OrdenServicioView, "Órdenes de Trabajo", icon="fa-wrench", category="Taller")
# appbuilder.add_view(CobroView, "Control de Cobros", icon="fa-money", category="Finanzas")

from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

# 1. Importaciones limpias de tus modelos locales
from .models import Cliente, Equipo, OrdenServicio, RepuestoDetalle, ServicioPrestado, Cobro

# 2. Definición de las Vistas (Sin llamar a appbuilder todavía)
class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)
    list_columns = ['nombre', 'telefono', 'correo']

class EquipoView(ModelView):
    datamodel = SQLAInterface(Equipo)
    list_columns = ['tipo', 'marca', 'modelo', 'cliente.nombre']

class OrdenServicioView(ModelView):
    datamodel = SQLAInterface(OrdenServicio)
    list_columns = ['id', 'fecha_ingreso', 'equipo.cliente.nombre', 'estado']

class RepuestoDetalleView(ModelView):
    datamodel = SQLAInterface(RepuestoDetalle)

class ServicioPrestadoView(ModelView):
    datamodel = SQLAInterface(ServicioPrestado)

class CobroView(ModelView):
    datamodel = SQLAInterface(Cobro)
    list_columns = ['orden_id', 'monto_total', 'estado_pago', 'metodo_pago']


# =========================================================
# 3. ROMPER EL BUCLE: Importamos y registramos al FINAL ABSOLUTO
# =========================================================
from app import appbuilder

# Registramos las vistas SIN categorizar por ahora, directo a la raíz del menú
appbuilder.add_view(ClienteView, "Clientes", icon="fa-users")
appbuilder.add_view(EquipoView, "Equipos", icon="fa-laptop")
appbuilder.add_view(OrdenServicioView, "Órdenes de Trabajo", icon="fa-wrench")
appbuilder.add_view(CobroView, "Control de Cobros", icon="fa-money")