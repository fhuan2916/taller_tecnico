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

class PanelGraficosView(BaseView):
    route_base = "/panel_graficos"
    
    # ¡ESTA ES LA PROPIEDAD CORRECTA! 
    # Le dice a FAB qué método cargar por defecto cuando se hace clic en el menú
    default_view = "ver_graficos"

    @expose("/ver/")
    def ver_graficos(self):
        ordenes = db.session.query(OrdenServicio).all()
        total_ordenes = len(ordenes)
        
        estados_lista = [o.estado for o in ordenes if o.estado]
        fallas_lista = [o.falla_reportada for o in ordenes if o.falla_reportada]
        
        conteo_estados = Counter(estados_lista)
        conteo_fallas = Counter(fallas_lista)
        
        # =========================================================
        # LÓGICA DE PRONÓSTICOS (Contexto: Taller Técnico)
        # =========================================================
        # Gráfica 1: Pronósticos sobre Estados de las Órdenes
        # Pronóstico 1: Cuello de botella estimado en base a órdenes "Recibidas" o "En Proceso"
        ordenes_activas = conteo_estados.get("En Proceso", 0) + conteo_estados.get("Recibido", 0)
        tiempo_estimado_entrega = ordenes_activas * 1.5  # Asumiendo 1.5 horas de media por servicio
        
        # Pronóstico 2: Tasa de efectividad de reparaciones futuras
        terminadas = conteo_estados.get("Terminado", 0) + conteo_estados.get("Entregado", 0)
        tasa_efectividad = (terminadas / total_ordenes * 100) if total_ordenes > 0 else 100
        
        # Pronóstico 3: Proyección de Crecimiento de Órdenes para el siguiente mes (+15% tendencia)
        proyeccion_ordenes_mes_siguiente = round(total_ordenes * 1.15)

        # Gráfica 2: Pronósticos sobre Tipos de Fallas
        # Pronóstico 4: Demanda estimada de repuestos críticos (basado en la falla más común)
        falla_mas_comun = conteo_fallas.most_common(1)[0][0] if fallas_lista else "Ninguna"
        
        # Pronóstico 5: Estimación de ingresos promedio requeridos por mantenimiento de software vs hardware
        # Pronóstico 6: Tiempo promedio de diagnóstico según complejidad de la falla prevalente

        return self.render_template(
            "graficos.html",
            estados_labels=list(conteo_estados.keys()),
            estados_valores=list(conteo_estados.values()),
            fallas_labels=list(conteo_fallas.keys()),
            fallas_valores=list(conteo_fallas.values()),
            # Enviamos las variables predictivas al HTML
            tiempo_entrega=round(tiempo_estimado_entrega, 1),
            tasa_efectividad=round(tasa_efectividad, 1),
            proyeccion_total=proyeccion_ordenes_mes_siguiente,
            falla_comun=falla_mas_comun
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