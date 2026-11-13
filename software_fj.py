import abc #Librería obligatoria para implementar Abstracción (Clases y métodos abstractos)
import logging  # Librería para el sistema de audiotoria y archivos
from datetime import datetime  # Módulo para capturar la fecha y hora exacta del sistema
from typing import List


logging.basicConfig(
    filename='sistema_software_fj.log',  # Nombre del archivo donde se guardará la bitácora
    level=logging.INFO,           # Nivel mínimo de reportes a capturar
    format='%(asctime)s - %(levelname)s - %(message)s',  # Estructura del log: Fecha - importancia - Mensaje
    encoding='utf-8'  # Soporte para caracteres en español (tildes y la letra Ñ)
)

def registrar_log(mensaje: str, es_error: bool = False):
    print(mensaje)
    if es_error:
        logging.error(mensaje) 
    else:
        logging.info(mensaje)

class SoftwareFJException(Exception): #Clase madre para todas las excepciones del programa
    pass

class DatoInvalidoException(SoftwareFJException): #Se activa cuando entran datos que no cumples con las reglas
    pass

class ServicioNoDisponibleException(SoftwareFJException): #Se activa cuando solicitan un servicio inactivo o en mantenimiento
    pass

class ReservaInvalidaException(SoftwareFJException): #Se activa cuando una transaccion de reserva falla en las reglas de limites o calculos
    pass

#------------------------------------------------------------------------
# CLASE BASE DEL SISTEMA
#------------------------------------------------------------------------

class EntidadBase(abc.ABC):
    def __init__(self, id_entidad: str):  # No permite ID vacion o con espacios
        if not id_entidad or not id_entidad.strip():
            raise DatoInvalidoException("El ID de la entidad no puede estar vacío.")
        self._id_entidad = id_entidad.strip()
        self._fecha_registro = datetime.now()

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    @abc.abstractmethod
    def obtener_detalles(self) -> str:
        pass

#---------------------------------------------------------------------------------------------
# CLASE CLIENTE
#--------------------------------------------------------------------------------------
class Cliente(EntidadBase):
    def __init__(self, id_cliente: str, nombre: str, correo: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str):
            raise DatoInvalidoException("El nombre debe ser un texto.")

        valor = valor.strip()

        if len(valor) < 3:
            raise DatoInvalidoException(
                "El nombre debe tener al menos 3 caracteres."
            )

        if not all(
            caracter.isalpha() or caracter.isspace() or caracter in "-'"
            for caracter in valor
        ):
            raise DatoInvalidoException(
                "El nombre contiene caracteres no permitidos."
            )

        self._nombre = valor

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not isinstance(valor, str):
            raise DatoInvalidoException("El correo electrónico debe ser un texto.")

        valor = valor.strip()

        if (
            not valor
            or "@" not in valor
            or valor.count("@") != 1
            or "." not in valor.split("@")[1]
            or valor.startswith("@")
            or valor.endswith(".")
            or " " in valor
        ):
            raise DatoInvalidoException(
                f"El correo electrónico '{valor}' no tiene un formato válido."
            )

        self._correo = valor

    def obtener_detalles(self) -> str:
        return f"Cliente ID: {self.id_entidad} | Nombre: {self.nombre} | Correo: {self.correo}"

#----------------------------------------------------------------------------------
# POLIMORFISMO Y HERENCIA
#--------------------------------------------------------------------------------------
class Servicio(abc.ABC):
    def __init__(self, id_servicio: str, nombre_servicio: str, costo_base: float):

        if not isinstance(id_servicio, str) or not id_servicio.strip():
            raise DatoInvalidoException(
                "El ID del servicio debe ser un texto válido."
            )

        if not isinstance(nombre_servicio, str) or not nombre_servicio.strip():
            raise DatoInvalidoException(
                "El nombre del servicio debe ser un texto válido."
            )

        if (
            not isinstance(costo_base, (int, float))
            or isinstance(costo_base, bool)
            or costo_base < 0
        ):
            raise DatoInvalidoException(
                "El costo base debe ser un número positivo o cero."
            )

        self._id_servicio = id_servicio.strip()
        self._nombre_servicio = nombre_servicio.strip()
        self._costo_base = costo_base
        self._disponible = True

    @property
    def id_servicio(self) -> str:
        return self._id_servicio

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        if not isinstance(estado, bool):
            raise DatoInvalidoException(
                "El estado de disponibilidad debe ser verdadero o falso."
            )
        self._disponible = estado

    def validar_descuento(self, descuento: float):
        if (
            not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or descuento < 0
            or descuento > 1
        ):
            raise DatoInvalidoException(
                "El descuento debe estar entre 0 y 1 (0% a 100%)."
            )
        
    @abc.abstractmethod
    def calcular_costo(
        self,
        horas: int,
        descuento: float = 0.0,
        impuesto: float = 0.0
    ) -> float:
        pass

    @abc.abstractmethod
    def describir_servicio(self) -> str:
        pass

    def validar_parametros(self, horas: int):
        if (
            not isinstance(horas, int)
            or isinstance(horas, bool)
            or horas <= 0
        ):
            raise DatoInvalidoException(
                "La duración del servicio debe ser un número entero mayor a 0 horas."
            )
        
#----------------------------------------------------------------------------------
# Reserva de salas
#----------------------------------------------------------------------------------
class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, capacidad_personas: int, costo_base: float = 50.0):
        super().__init__(id_servicio, "Reserva de Sala", costo_base)
        if (
            not isinstance(capacidad_personas, int)
            or isinstance(capacidad_personas, bool)
            or capacidad_personas <= 0
        ):
            raise DatoInvalidoException(
                "La capacidad de la sala debe ser un número entero mayor a cero."
            )
        self.capacidad_personas = capacidad_personas

    def validar_parametros(self, horas: int):
        super().validar_parametros(horas) # Valida que las horas sean mayores a cero
        if horas > 12: # No se permite rentar la sala mas de medio dia seguido
            raise DatoInvalidoException("No se puede reservar una sala por más de 12 horas continuas.")

    def calcular_costo(
        self,
        horas: int,
        descuento: float = 0.0,
        impuesto: float = 0.0
    ) -> float:
        self.validar_parametros(horas)
        self.validar_descuento(descuento)

        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or impuesto < 0
            or impuesto > 1
        ):
            raise DatoInvalidoException(
                "El impuesto debe estar entre 0 y 1 (0% a 100%)."
            )
        
        costo_total = (self._costo_base * horas) + (self.capacidad_personas * 2)
        costo_con_descuento = costo_total * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)

        return round(costo_final, 2)

    def describir_servicio(self) -> str:
        return f"Sala (ID: {self.id_servicio}) - Capacidad: {self.capacidad_personas} personas."

#----------------------------------------------------------------------------
# Alquiler de equipo tecnologico
#----------------------------------------------------------------------------
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, tipo_equipo: str, costo_base: float):
        super().__init__(id_servicio, f"Alquiler de {tipo_equipo}", costo_base)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise DatoInvalidoException(
                "El tipo de equipo debe ser un texto válido."
            )

        self.tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, horas: int):
        super().validar_parametros(horas)
        if horas < 2:
            raise DatoInvalidoException("El tiempo mínimo de alquiler de equipos es de 2 horas.")

    def calcular_costo(
        self,
        horas: int,
        descuento: float = 0.0,
        impuesto: float = 0.0
    ) -> float:
        self.validar_parametros(horas)
        self.validar_descuento(descuento)

        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or impuesto < 0
            or impuesto > 1
        ):
            raise DatoInvalidoException(
                "El impuesto debe estar entre 0 y 1 (0% a 100%)."
            )

        costo_total = (self._costo_base * horas) * 1.05
        costo_con_descuento = costo_total * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)

        return round(costo_final, 2)

    def describir_servicio(self) -> str:
        return f"Equipo (ID: {self.id_servicio}) - Tipo: {self.tipo_equipo}."

#---------------------------------------------------------------------------
#Asersoria eprofesional
#---------------------------------------------------------------------------
class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, consultor: str, costo_base: float = 120.0):
        super().__init__(id_servicio, "Asesoría Especializada", costo_base)

        if not isinstance(consultor, str) or not consultor.strip():
            raise DatoInvalidoException(
                "El nombre del consultor debe ser un texto válido."
            )

        self.consultor = consultor.strip()

    def validar_parametros(self, horas: int):
        super().validar_parametros(horas)
        if horas > 4:
            raise DatoInvalidoException("Las asesorías no pueden exceder las 4 horas continuas.")

    def calcular_costo(
        self,
        horas: int,
        descuento: float = 0.0,
        impuesto: float = 0.0
    ) -> float:
        self.validar_parametros(horas)
        self.validar_descuento(descuento)

        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or impuesto < 0
            or impuesto > 1
        ):
            raise DatoInvalidoException(
                "El impuesto debe estar entre 0 y 1 (0% a 100%)."
            )
        
        costo_total = self._costo_base * horas
        costo_con_descuento = costo_total * (1 - descuento)
        costo_final = costo_con_descuento * (1 + impuesto)

        return round(costo_final, 2)

    def describir_servicio(self) -> str:
        return f"Asesoría (ID: {self.id_servicio}) - Consultor: {self.consultor}."

#-----------------------------------------------------------------------
# Control
#-----------------------------------------------------------------------
class Reserva:
    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        horas: int,
        descuento: float = 0.0,
        impuesto: float = 0.0
    ):
        if not isinstance(id_reserva, str) or not id_reserva.strip():
            raise DatoInvalidoException(
                "El identificador de la reserva debe ser un texto válido."
            )

        if not isinstance(cliente, Cliente):
            raise DatoInvalidoException(
                "La reserva debe estar asociada a un cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise DatoInvalidoException(
                "La reserva debe estar asociada a un servicio válido."
            )

        self.id_reserva = id_reserva.strip()
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.descuento = descuento
        self.impuesto = impuesto
        self.estado = "PENDIENTE"
        self.costo_final = 0.0

    def procesar_confirmacion(self):
        registrar_log(f"\n--- Iniciando Procesamiento de la Reserva {self.id_reserva} ---")
        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleException(f"El servicio '{self.servicio.id_servicio}' se encuentra inactivo.")
            self.costo_final = self.servicio.calcular_costo(
                self.horas,
                self.descuento,
                self.impuesto
            )
        except (ServicioNoDisponibleException, DatoInvalidoException) as error_origen:
            self.estado = "FALLIDA"
            mensaje_error = f"No se pudo confirmar la reserva {self.id_reserva}."
            registrar_log(f"[ERROR CONTROLADO]: {mensaje_error} -> Motivo: {error_origen}", es_error=True)
            raise ReservaInvalidaException(mensaje_error) from error_origen
        else:
            self.estado = "CONFIRMADA"
            registrar_log(f"[ÉXITO]: Reserva {self.id_reserva} aprobada de manera exitosa.")
            registrar_log(f"         {self.cliente.obtener_detalles()}")
            registrar_log(f"         {self.servicio.describir_servicio()}")
            registrar_log(f"         Costo total liquidado: ${self.costo_final}")
        finally:
            registrar_log(f"--- Fin de la Transacción de la Reserva {self.id_reserva} ---")
            
    def cancelar(self, motivo: str = "Sin especificar"):
        try:
            if self.estado != "CONFIRMADA":
                raise ReservaInvalidaException(
                    f"No se puede cancelar la reserva {self.id_reserva} "
                    f"porque su estado es {self.estado}."
                )
            if not isinstance(motivo, str) or not motivo.strip():
                raise ReservaInvalidaException(
                    "Debe proporcionar un motivo de cancelación válido."
                )

            motivo = motivo.strip()

            self.estado = "CANCELADA"
            registrar_log(
                f"[CANCELACIÓN]: Reserva {self.id_reserva} cancelada. "
                f"Motivo: {motivo}"
            )

        except ReservaInvalidaException as error:
            registrar_log(
                f"[ERROR CONTROLADO]: {error}",
                es_error=True
            )
            raise

#----------------------------------------------------------------
#Operaciones requeridas
#----------------------------------------------------------------

def ejecutar_simulador():
    registrar_log("=================================================================")
    registrar_log("     INICIANDO SIMULACIÓN INTEGRAL - SOFTWARE FJ                 ")
    registrar_log("=================================================================\n")
    
    lista_clientes: List[Cliente] = []
    lista_servicios: List[Servicio] = []
    lista_reservas: List[Reserva] = []

    # Op 1
    registrar_log("[Op 1] Intentando registrar un Cliente Válido...")
    try:
        c1 = Cliente("C01", "Carlos Mendoza", "carlos@email.com")
        lista_clientes.append(c1)
        registrar_log(f"   ÉXITO -> {c1.obtener_detalles()}")
    except SoftwareFJException as e:
        registrar_log(f"   ERROR INESPERADO -> {e}", es_error=True)

    # Op 2
    registrar_log("\n[Op 2] Intentando registrar Cliente Inválido (Nombre de 2 letras)...")
    try:
        c_error1 = Cliente("C02", "Al", "al@email.com")
        lista_clientes.append(c_error1)
    except DatoInvalidoException as e:
        registrar_log(f"   [Excepción Controlada Esperada]: {e}", es_error=True)

    # Op 3
    registrar_log("\n[Op 3] Intentando registrar Cliente Inválido (Correo sin @ ni .)...")
    try:
        c_error2 = Cliente("C03", "Maria Gomez", "mariagomez.com")
        lista_clientes.append(c_error2)
    except DatoInvalidoException as e:
        registrar_log(f"   [Excepción Controlada Esperada]: {e}", es_error=True)

    # Op 4
    registrar_log("\n[Op 4] Intentando crear un Servicio de Sala Válido...")
    try:
        s1 = ReservaSala("S_SALA_01", capacidad_personas=10, costo_base=60.0)
        lista_servicios.append(s1)

        registrar_log(f"   ÉXITO -> {s1.describir_servicio()}")
    except SoftwareFJException as e:
        registrar_log(f"   ERROR INESPERADO -> {e}", es_error=True)

    # Op 5
    registrar_log("\n[Op 5] Intentando crear Servicio con Costo Base Negativo...")
    try:
        s_error = AlquilerEquipo("S_EQ_ERR", "Servidor", costo_base=-50.0)
        lista_servicios.append(s_error)
    except DatoInvalidoException as e:
        registrar_log(f"   [Excepción Controlada Esperada]: {e}", es_error=True)

    # Op 6
    registrar_log("\n[Op 6] Creando Servicios adicionales válidos en el catálogo...")
    try:
        s2 = AlquilerEquipo("S_EQ_02", "Videobeam 4K", costo_base=25.0)
        s3 = AsesoriaEspecializada("S_ASE_03", "Ing. Diana Torres", costo_base=150.0)
        lista_servicios.append(s2)
        lista_servicios.append(s3)
        registrar_log(f"   ÉXITO -> {s2.describir_servicio()}")
        registrar_log(f"   ÉXITO -> {s3.describir_servicio()}")
    except SoftwareFJException as e:
        registrar_log(f"   ERROR INESPERADO -> {e}", es_error=True)

    # Op 7
    registrar_log("\n[Op 7] Solicitando Reserva Válida para Sala (5 horas, 10% desc)...")
    try:
        reserva1 = Reserva("R01", c1, s1, horas=5, descuento=0.10)
        lista_reservas.append(reserva1)
        reserva1.procesar_confirmacion()
    except ReservaInvalidaException:
        pass

    # Op 8
    registrar_log("\n[Op 8] Solicitando Reserva Inválida (Excede límite de 12 horas en Sala)...")
    try:
        reserva2 = Reserva("R02", c1, s1, horas=24)
        lista_reservas.append(reserva2)
        reserva2.procesar_confirmacion()
    except ReservaInvalidaException:
        pass

    # Op 9
    registrar_log("\n[Op 9] Solicitando Reserva de un equipo puesto Fuera de Servicio...")
    try:
        s2.disponible = False
        reserva3 = Reserva("R03", c1, s2, horas=4)
        lista_reservas.append(reserva3)
        reserva3.procesar_confirmacion()
    except ReservaInvalidaException:
        pass

    # Op 10
    registrar_log("\n[Op 10] Solicitando Reserva Válida para Asesoría Técnica (3 horas)...")
    try:
        reserva4 = Reserva(
            "R04",
            c1,
            s3,
            horas=3,
            descuento=0.10,
            impuesto=0.19
        )
        lista_reservas.append(reserva4)
        reserva4.procesar_confirmacion()
    except ReservaInvalidaException:
        pass

    # Op 11: Cancelación de reserva confirmada
    registrar_log("\n[Op 11] Cancelando una reserva confirmada...")
    try:
        reserva1.cancelar("Solicitud del cliente")
    except ReservaInvalidaException:
        pass

    # Op 12: Intento de cancelar una reserva fallida
    registrar_log("\n[Op 12] Intentando cancelar una reserva fallida...")
    try:
        reserva2.cancelar("Prueba de cancelación inválida")
    except ReservaInvalidaException:
        pass

    registrar_log("\n=================================================================")
    registrar_log("  SIMULACIÓN FINALIZADA - PROGRAMA SE MANTUVO ACTIVO Y ESTABLE   ")
    registrar_log("=================================================================")


if __name__ == "__main__":
    ejecutar_simulador()
