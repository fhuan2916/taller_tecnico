from flask_appbuilder import BaseView,ModelView, expose#, GroupByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder
from app.models import OrdenServicio
from app import db
from collections import Counter
from google import genai

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
        # ordenes = db.session.query(OrdenServicio).all()
        # total_ordenes = len(ordenes)
        
        # estados_lista = [o.estado for o in ordenes if o.estado]
        # fallas_lista = [o.falla_reportada for o in ordenes if o.falla_reportada]
        
        # conteo_estados = Counter(estados_lista)
        # conteo_fallas = Counter(fallas_lista)
        # ordenes_activas = conteo_estados.get("En Proceso", 0) + conteo_estados.get("Recibido", 0)
        # tiempo_estimado_entrega = ordenes_activas * 1.5  # Asumiendo 1.5 horas de media por servicio
        
        # # Pronóstico 2: Tasa de efectividad de reparaciones futuras
        # terminadas = conteo_estados.get("Terminado", 0) + conteo_estados.get("Entregado", 0)
        # tasa_efectividad = (terminadas / total_ordenes * 100) if total_ordenes > 0 else 100
        
        # # Pronóstico 3: Proyección de Crecimiento de Órdenes para el siguiente mes (+15% tendencia)
        # proyeccion_ordenes_mes_siguiente = round(total_ordenes * 1.15)

        # # Gráfica 2: Pronósticos sobre Tipos de Fallas
        # # Pronóstico 4: Demanda estimada de repuestos críticos (basado en la falla más común)
        # falla_mas_comun = conteo_fallas.most_common(1)[0][0] if fallas_lista else "Ninguna"
        
        # # Pronóstico 5: Estimación de ingresos promedio requeridos por mantenimiento de software vs hardware
        # # Pronóstico 6: Tiempo promedio de diagnóstico según complejidad de la falla prevalente

        # return self.render_template(
        #     "graficos.html",
        #     estados_labels=list(conteo_estados.keys()),
        #     estados_valores=list(conteo_estados.values()),
        #     fallas_labels=list(conteo_fallas.keys()),
        #     fallas_valores=list(conteo_fallas.values()),
        #     # Enviamos las variables predictivas al HTML
        #     tiempo_entrega=round(tiempo_estimado_entrega, 1),
        #     tasa_efectividad=round(tasa_efectividad, 1),
        #     proyeccion_total=proyeccion_ordenes_mes_siguiente,
        #     falla_comun=falla_mas_comun
        # )
        ordenes = db.session.query(OrdenServicio).all()
        
        estados_lista = [o.estado for o in ordenes if o.estado]
        fallas_lista = [o.falla_reportada for o in ordenes if o.falla_reportada]
        
        conteo_estados = Counter(estados_lista)
        conteo_fallas = Counter(fallas_lista)
        
        # =========================================================
        # 🤖 INTEGRACIÓN CON GEMINI IA
        # =========================================================
        # RECOMENDACIÓN: Reemplaza "TU_API_KEY_AQUÍ" por tu clave de Google AI Studio
        try:
            client = genai.Client(api_key="")
            
            # Construimos un prompt contextualizado con los datos reales de tu taller
            prompt = f"""
            Actúa como un experto en Auditoría de Sistemas y Business Intelligence para un taller de soporte técnico computacional.
            Analiza los siguientes datos actuales del negocio:
            - Total de órdenes en el sistema: {len(ordenes)}
            - Distribución por estados: {dict(conteo_estados)}
            - Fallas recurrentes reportadas por los clientes: {dict(conteo_fallas)}
            
            Genera un informe breve de pronóstico operativo y estratégico en exactamente 3 puntos concisos (máximo 2 líneas por punto). Enfatiza proyecciones de inventario, cuellos de botella y carga técnica futura. Evita usar formatos Markdown complejos como asteriscos en exceso.
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            reporte_ia = response.text
        except Exception as e:
            # Resguardo en caso de que falle la conexión o falte la API Key
            reporte_ia = "Módulo IA temporalmente en mantenimiento. Verifique la API Key de Google Cloud."

        return self.render_template(
            "graficos.html",
            estados_labels=list(conteo_estados.keys()),
            estados_valores=list(conteo_estados.values()),
            fallas_labels=list(conteo_fallas.keys()),
            fallas_valores=list(conteo_fallas.values()),
            # Enviamos el informe generado por la IA a la interfaz
            reporte_ia=reporte_ia
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