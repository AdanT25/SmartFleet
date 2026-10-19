# Proyecto Integrador - Proyecto 2 (Red Bayesiana)

## Descripción
Este módulo implementa una Red Bayesiana para el **diagnóstico de fallas mecánicas** en el contexto del proyecto **SmartFleet**. Permite evaluar dinámicamente el riesgo de que un camión sufra una avería utilizando datos en tiempo real de los sensores del motor y el desgaste histórico del vehículo.

## Video Demo
Puedes ver la demostración del funcionamiento del proyecto y las consultas de inferencia en el siguiente enlace:
👉 [Video Demo - SmartFleet (YouTube)](https://youtu.be/__J_qH7IzTU)

## Estructura de la Red
**Variables:**
* `Temperatura`: Temperatura del motor con estados {0: Normal, 1: Alta}.
* `Kilometraje`: Kilometraje acumulado con estados {0: Bajo, 1: Alto}.
* `Presión`: Presión del aceite con estados {0: Normal, 1: Baja}.
* `Falla`: Falla mecánica general con estados {0: No, 1: Sí}.

**Dependencias:**
La variable `Falla` es dependiente de manera directa de los tres indicadores (`Temperatura`, `Kilometraje`, `Presión`), ya que la combinación de desgaste, factores térmicos y lubricación dicta la integridad mecánica.
- **Diagrama:** `Temperatura -> Falla`, `Kilometraje -> Falla`, `Presión -> Falla`.

## CPDs
| Variable | Padres | Descripción |
| :--- | :--- | :--- |
| `Temperatura` | Ninguno | Probabilidad base asignada en 30% Alta. Las altas temperaturas sostenidas en las rutas del desierto de Mexicali incrementan significativamente la probabilidad a priori de calentamiento del motor en la flotilla. |
| `Kilometraje` | Ninguno | Probabilidad base de 40% Alto, asumiendo una flotilla de vehículos de carga con uso constante y recorridos largos. |
| `Presión` | Ninguno | Probabilidad base de 15% Baja. La pérdida de presión de aceite es un evento menos frecuente pero crítico. |
| `Falla` | Temp, Km, Pres | La probabilidad de falla salta al 95% si los tres factores son negativos (Temp Alta, Km Alto, Presión Baja), reflejando cómo un motor desgastado sometido a calor extremo y mala lubricación tiene un colapso inminente. Si solo la presión es baja, el riesgo sube al 60% por desgaste de metales internos, incluso con buena temperatura. |

## Consultas de Inferencia
1. **Consulta 1:** `P(Falla | Temperatura=1, Kilometraje=1)`
   **Resultado:** Falla: No = 0.4325 / Falla: Sí = 0.5675
   **Interpretación:** Un camión con alto kilometraje operando bajo altas temperaturas tiene un 56.75% de probabilidad de fallar. Esto indica que se requiere programación preventiva inmediata en el taller, ya que el riesgo de tirar el camión en ruta supera la probabilidad de operar normalmente.

2. **Consulta 2:** `P(Falla | Presión=1)`
   **Resultado:** Falla: No = 0.2940 / Falla: Sí = 0.7060
   **Interpretación:** La caída de presión de aceite eleva la probabilidad de falla mecánica general al 70.60%, sin importar la temperatura o el kilometraje. La regla de negocio de SmartFleet debe dictar apagar el motor inmediatamente.

## Instrucciones de Ejecución
1. Clonar el repositorio: `git clone [TU_URL_AQUI]`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar el script: `python script.py`

## Ejemplo de Salida
```text
Consulta 1: P(Falla | Temperatura=Alta, Kilometraje=Alto)
+----------+--------------+
| Falla    |   phi(Falla) |
+==========+==============+
| Falla(0) |       0.4325 |
+----------+--------------+
| Falla(1) |       0.5675 |
+----------+--------------+
