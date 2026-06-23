from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Text
from sqlalchemy.orm import relationship
import datetime

# 1. Tabla Clientes
class Cliente(Model):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    telefono = Column(String(20), nullable=False)
    correo = Column(String(100), nullable=True)

    def __repr__(self):
        return self.nombre if self.nombre else f"Cliente {self.id}"

# 2. Tabla Equipos
class Equipo(Model):
    __tablename__ = 'equipos'
    id = Column(Integer, primary_key=True)
    tipo = Column(String(50), nullable=False) # Laptop, PC, etc.
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=True)
    serie = Column(String(100), nullable=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    cliente = relationship("Cliente")

    def __repr__(self):
        return f"{self.marca} {self.modelo}" if self.marca else f"Equipo {self.id}"

# 3. Tabla Ordenes de Servicio
class OrdenServicio(Model):
    __tablename__ = 'ordenes_servicio'
    id = Column(Integer, primary_key=True)
    fecha_ingreso = Column(Date, default=datetime.date.today, nullable=False)
    falla_reportada = Column(Text, nullable=False)
    diagnostico = Column(Text, nullable=True)
    estado = Column(String(50), default="Recibido") # Recibido, En Reparacion, Listo, Entregado
    
    equipo_id = Column(Integer, ForeignKey('equipos.id'), nullable=False)
    equipo = relationship("Equipo")

    def __repr__(self):
        return f"Orden #{self.id}"

# 4. Tabla Detalle de Repuestos
class RepuestoDetalle(Model):
    __tablename__ = 'repuestos_detalle'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(150), nullable=False)
    costo_repuesto = Column(Float, default=0.0, nullable=False)
    
    orden_id = Column(Integer, ForeignKey('ordenes_servicio.id'), nullable=False)
    orden = relationship("OrdenServicio")

# 5. Tabla Servicios Prestados (Mano de Obra)
class ServicioPrestado(Model):
    __tablename__ = 'servicios_prestados'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(150), nullable=False) # Ej: Limpieza Química
    costo_mano_obra = Column(Float, default=0.0, nullable=False)
    
    orden_id = Column(Integer, ForeignKey('ordenes_servicio.id'), nullable=False)
    orden = relationship("OrdenServicio")

# 6. Tabla Cobros / Facturas (Prioridad del negocio)
class Cobro(Model):
    __tablename__ = 'cobros'
    id = Column(Integer, primary_key=True)
    monto_total = Column(Float, default=0.0, nullable=False)
    metodo_pago = Column(String(50), default="Efectivo") # Efectivo, QR, Transferencia
    estado_pago = Column(String(50), default="Pendiente") # Pendiente, Pagado, Anticipo
    fecha_pago = Column(Date, nullable=True)
    
    orden_id = Column(Integer, ForeignKey('ordenes_servicio.id'), nullable=False)
    orden = relationship("OrdenServicio")