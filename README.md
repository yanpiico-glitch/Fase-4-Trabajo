# Fase-4-Trabajo
Desarrollo de la actividad correspondiente de la actividad de la fase 4 repositorio

import abc
import logging
from datetime import datetime
from typing import List


logging.basicConfig(
    filename='sistema_software_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def registrar_log(mensaje: str, es_error: bool = False):
    print(mensaje)
    if es_error:
        logging.error(mensaje)
    else:
        logging.info(mensaje)

class SoftwareFJException(Exception):
    pass

class DatoInvalidoException(SoftwareFJException):
    pass

class ServicioNoDisponibleException(SoftwareFJException):
    pass

class ReservaInvalidaException(SoftwareFJException):
    pass


class EntidadBase(abc.ABC):
    def __init__(self, id_entidad: str):
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
        if not valor or len(valor.strip()) < 3:
            raise DatoInvalidoException("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if "@" not in valor or "." not in valor:
            raise DatoInvalidoException(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self._correo = valor.strip()

    def obtener_detalles(self) -> str:
        return f"Cliente ID: {self.id_entidad} | Nombre: {self.nombre} | Correo: {self.correo}"


class Servicio(abc.ABC):
    def __init__(self, id_servicio: str, nombre_servicio: str, costo_base: float):
        if costo_base < 0:
            raise DatoInvalidoException("El costo base no puede ser negativo.")
        self._id_servicio = id_servicio
        self._nombre_servicio = nombre_servicio
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
        self._disponible = estado

    @abc.abstractmethod
    def calcular_costo(self, horas: int, descuento: float = 0.0) -> float:
        pass

    @abc.abstractmethod
    def describir_servicio(self) -> str:
        pass

    @abc.abstractmethod
    def validar_parametros(self, horas: int):
        if horas <= 0:
            raise DatoInvalidoException("La duración del servicio debe ser mayor a 0 horas.")


class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, capacidad_personas: int, costo_base: float = 50.0):
        super().__init__(id_servicio, "Reserva de Sala", costo_base)
        if capacidad_personas <= 0:
            raise DatoInvalidoException("La capacidad de la sala debe ser mayor a cero.")
        self.capacidad_personas = capacidad_personas

    def validar_parametros(self, horas: int):
        super().validar_parametros(horas)
        if horas > 12:
            raise DatoInvalidoException("No se puede reservar una sala por más de 12 horas continuas.")

    def calcular_costo(self, horas: int, descuento: float = 0.0) -> float:
        self.validar_parametros(horas)
        costo_total = (self._costo_base * horas) + (self.capacidad_personas * 2)
        return round(costo_total * (1 - descuento), 2)

    def describir_servicio(self) -> str:
        return f"Sala (ID: {self.id_servicio}) - Capacidad: {self.capacidad_personas} personas."


class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, tipo_equipo: str, costo_base: float):
        super().__init__(id_servicio, f"Alquiler de {tipo_equipo}", costo_base)
        self.tipo_equipo = tipo_equipo

    def validar_parametros(self, horas: int):
        super().validar_parametros(horas)
        if horas < 2:
            raise DatoInvalidoException("El tiempo mínimo de alquiler de equipos es de 2 horas.")

    def calcular_costo(self, horas: int, descuento: float = 0.0) -> float:
        self.validar_parametros(horas)
        costo_total = (self._costo_base * horas) * 1.05
        return round(costo_total * (1 - descuento), 2)

    def describir_servicio(self) -> str:
        return f"Equipo (ID: {self.id_servicio}) - Tipo: {self.tipo_equipo}."


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, consultor: str, costo_base: float = 120.0):
        super().__init__(id_servicio, "Asesoría Especializada", costo_base)
        self.consultor = consultor

    def validar_parametros(self, horas: int):
        super().validar_parametros(horas)
        if horas > 4:
            raise DatoInvalidoException("Las asesorías no pueden exceder las 4 horas continuas.")

    def calcular_costo(self, horas: int, descuento: float = 0.0) -> float:
        self.validar_parametros(horas)
        costo_total = self._costo_base * horas
        return round(costo_total * (1 - descuento), 2)

    def describir_servicio(self) -> str:
        return f"Asesoría (ID: {self.id_servicio}) - Consultor: {self.consultor}."


class Reserva:
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: int, descuento: float = 0.0):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.descuento = descuento
        self.estado = "PENDIENTE"
        self.costo_final = 0.0

    def procesar_confirmacion(self):
        registrar_log(f"\n--- Iniciando Procesamiento de la Reserva {self.id_reserva} ---")
        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleException(f"El servicio '{self.servicio.id_servicio}' se encuentra inactivo.")
            self.costo_final = self.servicio.calcular_costo(self.horas, self.descuento)
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



def ejecutar_simulador():
    registrar_log("=================================================================")
    registrar_log("     INICIANDO SIMULACIÓN INTEGRAL - SOFTWARE FJ                 ")
    registrar_log("=================================================================\n")
    
    lista_clientes: List[Cliente] = []
    lista_servicios: List[Servicio] = []

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
        reserva1.procesar_confirmacion()
    except ReservaInvalidaException:
        pass

    # Op 8
    registrar_log("\n[Op 8] Solicitando Reserva Inválida (Excede límite de 12 horas en Sala)...")
    try:
        reserva2 = Reserva("R02", c1, s1, horas=24)
        reserva2.procesar_confirmacion()
    except ReservaInvalidaException:
        pass

    # Op 9
    registrar_log("\n[Op 9] Solicitando Reserva de un equipo puesto Fuera de Servicio...")
    try:
        s2.disponible = False
        reserva3 = Reserva("R03", c1, s2, horas=4)
        reserva3.procesar_confirmacion()
    except ReservaInvalidaException:
        pass

    # Op 10
    registrar_log("\n[Op 10] Solicitando Reserva Válida para Asesoría Técnica (3 horas)...")
    try:
        reserva4 = Reserva("R04", c1, s3, horas=3)
        reserva4.procesar_confirmacion()
    except ReservaInvalidaException:
        pass

    registrar_log("\n=================================================================")
    registrar_log("  SIMULACIÓN FINALIZADA - PROGRAMA SE MANTUVO ACTIVO Y ESTABLE   ")
    registrar_log("=================================================================")


if __name__ == "__main__":
    ejecutar_simulador()
