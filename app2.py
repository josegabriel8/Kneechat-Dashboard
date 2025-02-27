import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos (ajusta según tu archivo)
df = pd.read_excel("bd_c_gpt.xlsx")

# Diccionario de mapeo para categorias1 (códigos del 1 al 10)
DudasFrecuentes = {
    1: "Info general",          
    2: "Preparación para la cirugía",           
    3: "Cirugía/Anestesia",     
    4: "Proceso de recuperación",          
    5: "Manejo dolor",          
    6: "Complicaciones",        
    7: "Cuidados postop",       
    8: "Expectativas",          
    9: "Recursos Adicionales",              
    10: "Logística y tiempos de espera"             
}

# Crear una nueva columna con los labels cortos para categorias1
df['DudasFrecuentes'] = df['categorias1'].map(DudasFrecuentes)

# Diccionario de mapeo para categorias2 (códigos del 1 al 6)
map_cat2 = {
    1: "Dolor/Complicaciones",  
    2: "Deseo de operarse",         
    3: "Miedo/preocupación/Ansiedad",        
    4: "Confianza y positividad",             
    5: "Rutina diaria",               
    6: "Otros"                  
}

# Crear una nueva columna con los labels cortos para categorias2
df['Tiporeflexión'] = df['categorias2'].map(map_cat2)

# Configuración de la página
st.set_page_config(page_title="Dashboard de Análisis de Texto", layout="wide")

# Título principal
st.title("📊 Dashboard de Análisis de Comentarios y Preguntas")


st.header("Información del estudio")
st.write("""
**Este tablero presenta la información recopilada en el estudio:**
**'Empleo de canales de comunicación digitales para la evaluación y detección de necesidades de información en pacientes pendientes de intervención de Artroplastia Total de Rodilla.'**

- Los datos fueron recolectados a través de **41 entrevistas telefónicas** realizadas a pacientes con diagnóstico de **gonartrosis de rodilla** y con un procedimiento pendiente codificado como **sustitución total de rodilla**.
""")

st.header("Análisis de intervenciones/frases recogidas por pacientes en las entrevistas")
st.write("""
- La información presentada corresponde exclusivamente a las intervenciones realizadas por los pacientes durante las entrevistas.
- Tras el **preprocesamiento de los textos** y la segmentación de las intervenciones en **unidades de análisis (frases)**, se aplicaron técnicas de **Procesamiento de Lenguaje Natural (PLN)** para clasificar las frases en tres grandes grupos:

  1️⃣ **Duda/Pregunta:** Frases en las que el paciente expresa una necesidad de información.  
  2️⃣ **Comentario/Reflexión:** Frases dirigidas al entrevistador (doctor) que contienen información relevante sobre sus circunstancias, sentimientos, preocupaciones, etc.  
  3️⃣ **Interacciones no relevantes:** Saludaciones, despedidas, afirmaciones genéricas u otros comentarios sin valor para el estudio.  

""")


total_pacientes = 41

# Identificar pacientes únicos por tipo
comentario_ids = df[df["Tipo"] == "Comentario/reflexión"]["num_entrevista"].unique()
duda_ids = df[df["Tipo"] == "Duda/pregunta"]["num_entrevista"].unique()
union_ids = set(comentario_ids) | set(duda_ids)

# Contar pacientes por cada grupo
comentarios_count = len(comentario_ids)
dudas_count = len(duda_ids)
sin_registro = total_pacientes - len(union_ids)

# Preparar DataFrame para el gráfico
data = {
    "Tipo": ["Comentario/reflexión", "Duda/pregunta", "Sin interacción"],
    "Entrevistas": [comentarios_count, dudas_count, sin_registro]
}
df_plot = pd.DataFrame(data)
df_plot["Porcentaje"] = df_plot["Entrevistas"] / total_pacientes * 100

# Configurar estilo sin grid
sns.set_style("white")

# Gráfico 1: Frecuencia de entrevistas
fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(
    x="Tipo",
    y="Entrevistas",
    data=df_plot,
    order=["Comentario/reflexión", "Duda/pregunta", "Sin interacción"],
    color="#cf5c36",  # Color modificado a cf5c36
    ax=ax
)

# Agregar borde a cada barra
for patch in ax.patches:
    patch.set_edgecolor("black")
    patch.set_linewidth(1.5)

ax.set_title("Frecuencia de entrevistas por tipo de información recogida", fontsize=12)
ax.set_ylabel("Número de entrevistas", fontsize=10)
ylim_max = df_plot["Entrevistas"].max() + 5  
ax.set_ylim(0, ylim_max)

# Anotar porcentaje en cada barra
for index, row in df_plot.iterrows():
    y_value = row["Entrevistas"] + 0.5
    if index == 0 and y_value > ylim_max - 1:
        y_value = row["Entrevistas"] - 0.5
        va = "top"
    else:
        va = "bottom"
    ax.text(index, y_value, f'{row["Porcentaje"]:.1f}%', ha='center', va=va, fontsize=14)

plt.tight_layout()
st.pyplot(fig)

# ---- Gráficos 2 y 3: Frecuencia por categoría con filtro y lado a lado ----
st.subheader("--------------------------------------------------------")
st.header("Frases y pacientes por categoría")

st.write("📌 **En una segunda fase, la clasificación se profundizó aún más utilizando inteligencia artificial.**")
# Clasificación de comentarios/reflexiones
st.subheader("📌 Clasificación de comentarios/reflexiones")

st.write("""
Para las frases en las que los pacientes expresaban reflexiones o comentarios, se establecieron las siguientes categorías:

✅ **Dolor/Complicaciones:** Relacionadas con dolor, sufrimiento o complicaciones físicas derivadas de la rodilla.  
✅ **Deseo de operarse:** Expresan urgencia por la cirugía o críticas sobre la espera prolongada.  
✅ **Miedo/Preocupación/Ansiedad:** Reflejan angustia, miedo o inquietudes respecto a la cirugía o el postoperatorio.  
✅ **Confianza y Positividad:** Demuestran seguridad y optimismo respecto al procedimiento y el equipo médico.  
✅ **Rutina diaria:** Describen de manera neutral la vida cotidiana del paciente.  
✅ **Otros:** Frases que no encajan en las categorías anteriores.  
""")

# Clasificación de dudas/preguntas
st.subheader("📌 Clasificación de dudas/preguntas")
st.write("""
Las frases que reflejaban **necesidad de información** fueron categorizadas con base en la guía de **Preguntas Frecuentes sobre Prótesis Total de Rodilla**, que abarca los siguientes temas:

1️⃣ **Información general sobre la artroplastia de rodilla:** Explica qué es el procedimiento, su necesidad y comparaciones con otras intervenciones.  
2️⃣ **Preparación para la cirugía:** Consejos sobre cómo prepararse física y mentalmente, incluyendo cambios en el estilo de vida y adaptaciones en el hogar.  
3️⃣ **Cirugía y anestesia:** Información sobre el preoperatorio, tipo de anestesia, procedimiento quirúrgico y recuperación inicial.  
4️⃣ **Proceso de recuperación:** Expectativas sobre el postoperatorio en hospital y en casa, incluyendo fisioterapia y rehabilitación.  
5️⃣ **Manejo del dolor:** Estrategias para aliviar el dolor postoperatorio y detalles sobre medicamentos y efectos secundarios.  
6️⃣ **Complicaciones y riesgos:** Posibles complicaciones, señales de alerta y cómo identificarlas.  
7️⃣ **Cuidados postoperatorios:** Recomendaciones sobre higiene, vendajes, actividad física y recuperación en casa.  
8️⃣ **Expectativas a largo plazo:** Durabilidad de la prótesis, nivel de funcionalidad esperado y consejos para el cuidado de la rodilla operada.  
9️⃣ **Recursos adicionales:** Información sobre fuentes confiables para quienes buscan más orientación o apoyo.  

📌 **Categoría adicional:**  
🕒 **Logística y tiempos de espera:** Debido a la cantidad de preguntas sobre este tema, se agregó una categoría específica para abordar consultas sobre tiempos de espera, costos, trámites administrativos y pruebas preoperatorias.  
""")





# Botón de filtro para seleccionar qué columnas mostrar
tipo_seleccionado = st.multiselect(
    "Selecciona qué frecuencia mostrar:",
    ["Frases", "Pacientes"],
    default=["Frases", "Pacientes"]
)

# Gráfico 1: Dudas/Preguntas
st.markdown("### Dudas/Preguntas")
df_dudas = df.groupby("DudasFrecuentes").agg(
    Frases=("DudasFrecuentes", "count"),
    Pacientes=("num_entrevista", "nunique")
).reset_index().sort_values(by="Frases", ascending=False)

df_dudas_melted = df_dudas.melt(id_vars="DudasFrecuentes", var_name="Tipo", value_name="Frecuencia")
df_dudas_melted = df_dudas_melted[df_dudas_melted["Tipo"].isin(tipo_seleccionado)]

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=df_dudas_melted,
    x="DudasFrecuentes",
    y="Frecuencia",
    hue="Tipo",
    palette={"Frases": "#cf5c36", "Pacientes": "#93B7BE"},
    ax=ax2
)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha="right")
ax2.set_xlabel("Categoría de Dudas")
ax2.set_ylabel("Frecuencia")
ax2.legend(title="Tipo")
for container in ax2.containers:
    ax2.bar_label(container, fmt='%d', label_type='edge', fontsize=12)
plt.tight_layout()
st.pyplot(fig2)

# Separación visual
st.markdown("---")  

# Gráfico 2: Reflexiones/Comentarios
st.markdown("### Reflexiones/Comentarios")
df_reflexion = df.groupby("Tiporeflexión").agg(
    Frases=("Tiporeflexión", "count"),
    Pacientes=("num_entrevista", "nunique")
).reset_index().sort_values(by="Frases", ascending=False)

df_reflexion_melted = df_reflexion.melt(id_vars="Tiporeflexión", var_name="Tipo", value_name="Frecuencia")
df_reflexion_melted = df_reflexion_melted[df_reflexion_melted["Tipo"].isin(tipo_seleccionado)]

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=df_reflexion_melted,
    x="Tiporeflexión",
    y="Frecuencia",
    hue="Tipo",
    palette={"Frases": "#cf5c36", "Pacientes": "#93B7BE"},
    ax=ax3
)
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha="right")
ax3.set_xlabel("Categoría de Reflexión")
ax3.set_ylabel("Frecuencia")
ax3.legend(title="Tipo")
for container in ax3.containers:
    ax3.bar_label(container, fmt='%d', label_type='edge', fontsize=12)
plt.tight_layout()
st.pyplot(fig3)


st.subheader("--------------------------------------------------------")
st.header("Muestra de frases")

# ---- Ejemplos de preguntas/dudas por categoría ----
st.subheader("🎯 Ejemplos de preguntas/dudas por categoría")
# Se elimina el NaN del selectbox
categoria_dudas = st.selectbox(
    "Selecciona una categoría de dudas:",
    df["DudasFrecuentes"].dropna().unique()
)
# Se crea un DataFrame con las columnas 'num_entrevista' y 'frase'
df_dudas_table = df[df["DudasFrecuentes"] == categoria_dudas][["num_entrevista", "frase"]]
# Se establece 'num_entrevista' como índice para reemplazar el índice predeterminado
df_dudas_table = df_dudas_table.set_index("num_entrevista")
st.dataframe(df_dudas_table, use_container_width=True)

# ---- Ejemplos de reflexiones/comentarios por categoría ----
st.subheader("🎯 Ejemplos de reflexiones/comentarios por categoría")
# Se elimina el NaN del selectbox
categoria_reflexion = st.selectbox(
    "Selecciona una categoría comentario:",
    df["Tiporeflexión"].dropna().unique()
)
# Se crea un DataFrame con las columnas 'num_entrevista' y 'frase'
df_reflexion_table = df[df["Tiporeflexión"] == categoria_reflexion][["num_entrevista", "frase"]]
# Se establece 'num_entrevista' como índice para reemplazar el índice predeterminado
df_reflexion_table = df_reflexion_table.set_index("num_entrevista")
st.dataframe(df_reflexion_table, use_container_width=True)