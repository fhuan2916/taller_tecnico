from flask_appbuilder import BaseView,ModelView, expose#, GroupByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from app.models import OrdenServicio
from app import db
from collections import Counter


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
# ======================================================== # <-- ¡Esta línea debe estar ARRIBA de todos los add_view!


############################################################################
# Vista para el Gráfico Estadístico de Órdenes
# Vista para el Gráfico Estadístico de Órdenes
# Vista para el Gráfico Estadístico de Órdenes
# Vista para el Gráfico Estadístico de Órdenes
# Vista para el Gráfico Estadístico de Órdenes
# class OrdenServicioChartView(GroupByChartView):
#     datamodel = SQLAInterface(OrdenServicio)
#     chart_title = "Panel de Inteligencia de Negocios - Taller Técnico"
#     chart_type = "bar"
    
#     # 1. Mapeamos las etiquetas usando columnas de texto directo de tu modelo
#     label_columns = {
#         "estado": "Estado de la Órden",
#         "falla_reportada": "Tipos de Falla Comunes"
#     }
    
#     # 2. Agrupamos solo por campos que guarden texto directo
#     group_by_columns = ["estado", "falla_reportada"]
    
#     # 3. Ajustamos las definiciones de las series para estas dos variables
#     definitions = [
#         {
#             "group": "estado",
#             "series": [(aggregate_count, "estado")]
#         },
#         {
#             "group": "falla_reportada",
#             "series": [(aggregate_count, "falla_reportada")]
#         }
#     ]
    
#     # Colores llamativos que contrastan perfecto con el fondo oscuro
#     chart_colors = ["#3498db", "#1abc9c", "#2ecc71", "#e74c3c", "#f1c40f"]  

############################################################################


class PanelGraficosView(BaseView):
    route_base = "/panel_graficos"
    
    # ¡ESTA ES LA PROPIEDAD CORRECTA! 
    # Le dice a FAB qué método cargar por defecto cuando se hace clic en el menú
    default_view = "ver_graficos"

    @expose("/ver/")
    def ver_graficos(self):
        # ... (Todo tu código interno de consultas se queda exactamente igual) ...
        ordenes = db.session.query(OrdenServicio).all()
        estados_lista = [o.estado for o in ordenes if o.estado]
        fallas_lista = [o.falla_reportada for o in ordenes if o.falla_reportada]
        
        conteo_estados = Counter(estados_lista)
        conteo_fallas = Counter(fallas_lista)
        
        return self.render_template(
            "graficos.html",
            estados_labels=list(conteo_estados.keys()),
            estados_valores=list(conteo_estados.values()),
            fallas_labels=list(conteo_fallas.keys()),
            fallas_valores=list(conteo_fallas.values())
        )

# =========================================================
# REGISTRO AL FINAL DEL ARCHIVO (Sección 3)
# =========================================================
# Dejamos el add_view limpio, sin el argumento 'endpoint' que causaba el error
appbuilder.add_view(
    PanelGraficosView, 
    "Gráfico de Órdenes", 
    icon="fa-chart-pie", 
    category="Taller"
)
# Registramos tus vistas principales
appbuilder.add_view(ClienteView, "Clientes", icon="fa-users")
appbuilder.add_view(EquipoView, "Equipos", icon="fa-laptop")
appbuilder.add_view(OrdenServicioView, "Órdenes de Trabajo", icon="fa-wrench")
appbuilder.add_view(CobroView, "Control de Cobros", icon="fa-money")

# Registramos el nuevo gráfico estadístico usando el appbuilder ya importado
#appbuilder.add_view(OrdenServicioChartView, "Gráfico de Órdenes", icon="fa-chart-bar", category="Taller")