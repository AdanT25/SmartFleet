# requirements.txt debe incluir: pgmpy, networkx, matplotlib
from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def build_smartfleet_model():
    # 1. Estructura del DAG: Temperatura, Kilometraje y Presión -> Falla
    model = BayesianNetwork([
        ('Temperatura', 'Falla'),
        ('Kilometraje', 'Falla'),
        ('Presion', 'Falla')
    ])

    # 2. CPDs (0 = Estado Positivo/Normal, 1 = Estado Negativo/Alerta)
    # Temperatura: 0=Normal, 1=Alta 
    cpd_temp = TabularCPD(variable='Temperatura', variable_card=2, values=[[0.7], [0.3]])
    
    # Kilometraje: 0=Bajo, 1=Alto
    cpd_km = TabularCPD(variable='Kilometraje', variable_card=2, values=[[0.6], [0.4]])
    
    # Presión: 0=Normal, 1=Baja
    cpd_pres = TabularCPD(variable='Presion', variable_card=2, values=[[0.85], [0.15]])

    # Falla: 0=No, 1=Sí
    # Orden de evidencia: Temperatura, Kilometraje, Presion
    # Hay 2^3 = 8 combinaciones posibles.
    cpd_falla = TabularCPD(
        variable='Falla', 
        variable_card=2, 
        values=[
            # Temp=0(Norm), Temp=0, Temp=0, Temp=0, Temp=1(Alta), Temp=1, Temp=1, Temp=1
            # Km=0(Bajo), Km=0,   Km=1,   Km=1,   Km=0,         Km=0,   Km=1,   Km=1
            # Pr=0(Norm), Pr=1,   Pr=0,   Pr=1,   Pr=0,         Pr=1,   Pr=0,   Pr=1
            [0.98, 0.40, 0.85, 0.30, 0.70, 0.20, 0.50, 0.05], # Falla = No
            [0.02, 0.60, 0.15, 0.70, 0.30, 0.80, 0.50, 0.95]  # Falla = Sí
        ],
        evidence=['Temperatura', 'Kilometraje', 'Presion'],
        evidence_card=[2, 2, 2]
    )

    model.add_cpds(cpd_temp, cpd_km, cpd_pres, cpd_falla)
    assert model.check_model(), "Error en la validación de las CPDs"
    return model

# 3. Construir el modelo y motor de inferencia
modelo_smartfleet = build_smartfleet_model()
infer = VariableElimination(modelo_smartfleet)

# 4. Ejecutar Consultas Requeridas
print("Consulta 1: P(Falla | Temperatura=Alta, Kilometraje=Alto)")
res_1 = infer.query(variables=['Falla'], evidence={'Temperatura': 1, 'Kilometraje': 1})
print(res_1)

print("\nConsulta 2: P(Falla | Presión=Baja)")
res_2 = infer.query(variables=['Falla'], evidence={'Presion': 1})
print(res_2)