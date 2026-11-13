# APORTE INDIVIDUAL – FASE 4
## Sistema de gestión de reservas – Software FJ

---

## 1. Descripción del aporte

Este aporte individual desarrolla funcionalidades para el sistema Software FJ, enfocadas en la gestión de clientes, servicios y reservas, aplicando los principios de la programación orientada a objetos en Python.

## 2. Librerías utilizadas

Se utilizaron las siguientes librerías:

- **abc:** permite implementar abstracción mediante clases y métodos abstractos.
- **logging:** permite registrar eventos, operaciones y errores en un archivo de auditoría.
- **datetime:** permite obtener la fecha y hora del registro.
- **typing:** permite definir los tipos de datos utilizados en las listas mediante `List`.

## 3. Clases desarrolladas

- **EntidadBase:** clase abstracta que establece características generales de las entidades.
- **Cliente:** permite registrar clientes y validar sus nombres y correos electrónicos.
- **Servicio:** clase abstracta que define las características y operaciones generales de los servicios.
- **ReservaSala:** administra los servicios de reserva de salas y sus condiciones.
- **AlquilerEquipo:** gestiona el alquiler de equipos tecnológicos.
- **AsesoriaEspecializada:** administra los servicios de asesoría profesional.
- **Reserva:** controla la creación, confirmación y cancelación de reservas.

## 4. Conceptos de programación orientada a objetos aplicados

- **Abstracción:** mediante clases y métodos abstractos.
- **Herencia:** las clases especializadas heredan características de las clases principales.
- **Polimorfismo:** cada tipo de servicio implementa su propio cálculo de costos.
- **Encapsulamiento:** mediante atributos privados y propiedades para controlar el acceso y la modificación de datos.

## 5. Funcionalidades implementadas

- Registro y validación de clientes.
- Validación de información de los servicios.
- Control de disponibilidad de los servicios.
- Cálculo de costos según el tipo de servicio.
- Aplicación de descuentos e impuestos.
- Confirmación de reservas.
- Cancelación de reservas confirmadas.
- Control de estados: PENDIENTE, CONFIRMADA, FALLIDA y CANCELADA.
- Manejo de excepciones personalizadas.
- Registro de eventos y errores mediante logging.
- Administración de clientes, servicios y reservas mediante listas.

## 6. Manejo de excepciones y auditoría

Se implementaron excepciones personalizadas para controlar datos inválidos, servicios no disponibles y errores relacionados con las reservas.

También se utilizaron las estructuras `try`, `except`, `else` y `finally` para gestionar los errores y garantizar el registro de las operaciones realizadas.

## 7. Pruebas realizadas

Se ejecutaron 12 operaciones de prueba para verificar:

- Registro de clientes válidos e inválidos.
- Validación de correos electrónicos.
- Creación de servicios.
- Control de costos negativos.
- Confirmación de reservas.
- Validación de duración de los servicios.
- Control de disponibilidad.
- Aplicación de descuentos e impuestos.
- Cancelación de reservas.
- Manejo de errores.

Las pruebas permitieron comprobar el funcionamiento del sistema y la estabilidad de la ejecución.

## 8. Archivos generados

- `software_fj.py`: contiene el código fuente del aporte individual.
- `sistema_software_fj.log`: almacena los registros de auditoría generados durante la ejecución.

## 9. Integración del aporte

Este desarrollo se presenta como aporte individual para la Fase 4 del proyecto Software FJ. Está preparado para integrarse con los aportes de los demás integrantes, realizando los ajustes necesarios para unificar las clases y funcionalidades del sistema.

---
**Proyecto:** Software FJ  
**Actividad:** Fase 4 – Trabajo colaborativo
