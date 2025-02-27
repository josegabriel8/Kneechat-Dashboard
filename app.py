import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ---------------------------
# Cargar dataset principal y mapeos
# ---------------------------
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
df['Tiporeflexión'] = df['categorias2'].map(map_cat2)

# ---------------------------
# Configuración de la página y encabezados
# ---------------------------
st.set_page_config(page_title="Dashboard de Análisis de Texto", layout="wide")
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

# ---------------------------
# Aumentar tamaño de fuente general mediante CSS
# ---------------------------
st.markdown(
    """
    <style>
    p, div[class^="css"] {
        font-size: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# 1. Indicadores (Cards)
# ---------------------------
entrevistas_count = 41
frases_relevantes = df.shape[0]

st.markdown("### Indicadores Generales")

col_card1, col_card2, col_card3, col_card4 = st.columns(4)
col_card1.metric("Entrevistas realizadas", entrevistas_count,  border=True)
col_card2.metric("Número total de frases de pacientes", 623, border=True)
col_card3.metric("Frases relevantes", frases_relevantes, border=True)
col_card4.metric("Preguntas o dudas", 54, border=True)

# ---------------------------
# 2. Primer gráfico interactivo y tabla de frases
# ---------------------------
# Preparar datos para el gráfico 1
total_pacientes = 41  # valor fijo según estudio
comentario_ids = df[df["Tipo"] == "Comentario/reflexión"]["num_entrevista"].unique()
duda_ids = df[df["Tipo"] == "Duda/pregunta"]["num_entrevista"].unique()
union_ids = set(comentario_ids) | set(duda_ids)

comentarios_count = len(comentario_ids)
dudas_count = len(duda_ids)
sin_registro = total_pacientes - len(union_ids)

data = {
    "Tipo": ["Comentario/reflexión", "Duda/pregunta", "Sin interacción relevante"],
    "Entrevistas": [comentarios_count, dudas_count, sin_registro]
}
df_plot = pd.DataFrame(data)
df_plot["Porcentaje"] = df_plot["Entrevistas"] / total_pacientes * 100

# Agregar los valores fijos para el tooltip
fixed_total_frases = {
    "Comentario/reflexión": 227,
    "Duda/pregunta": 54,
    "Sin interacción relevante": 347
}
df_plot["TotalFrases"] = df_plot["Tipo"].map(fixed_total_frases)

# Crear gráfico interactivo con Plotly Express
fig1 = px.bar(
    df_plot,
    x="Tipo",
    y="Entrevistas",
    text=df_plot["Porcentaje"].apply(lambda x: f"{x:.1f}%"),
    hover_data={"TotalFrases": True, "Entrevistas": True},
    color_discrete_sequence=["#34a3d3"] 
)
fig1.update_layout(
    xaxis_title="",
    title_text="Frecuencia de entrevistas por tipo de información recogida"
)
fig1.update_traces(textposition='outside')

# Cargar dataset de frases irrelevantes (frasesfull.xlsx)
df_frases = pd.read_excel("frasesfull.xlsx")

st.markdown('<h3 style="text-align: center;">Categorización General y Ejemplos de Frases</h3>', unsafe_allow_html=True)
col_chart, col_table = st.columns(2)
with col_chart:
    st.plotly_chart(fig1, use_container_width=True)
with col_table:
    selected_tipo_frase = st.selectbox("Selecciona el tipo de frase", df_frases["tipo"].unique())
    filtered_frases = df_frases[df_frases["tipo"] == selected_tipo_frase].reset_index(drop=True)
    st.dataframe(filtered_frases[["frase"]].reset_index(drop=True), use_container_width=True)

# ---------------------------
# 3. Reorganización de Gráficos 2 y 3 con sus Tablas
# ---------------------------
st.markdown("## Análisis Detallado por Categorías")


st.subheader("--------------------------------------------------------")
st.header("Frases y pacientes por categoría")

st.write("📌 **En una segunda fase, la clasificación se profundizó aún más utilizando inteligencia artificial.**")
st.subheader("📌 Clasificación de dudas/preguntas")
st.write("""
Las frases que reflejaban **necesidad de información (54 en total)** fueron categorizadas con base en la guía de **Preguntas Frecuentes sobre Prótesis Total de Rodilla**, que abarca los siguientes temas:

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

# 3.1 Dudas/Preguntas: gráfico y tabla de ejemplos
st.markdown("### Dudas/Preguntas")
col_dudas_chart, col_dudas_table = st.columns(2)

with col_dudas_chart:
    tipo_seleccionado_dudas = st.multiselect(
       "Selecciona qué frecuencia mostrar (Dudas):",
       ["Frases", "Pacientes"],
       default=["Frases", "Pacientes"]
    )
    df_dudas = df.groupby("DudasFrecuentes").agg(
        Frases=("DudasFrecuentes", "count"),
        Pacientes=("num_entrevista", "nunique")
    ).reset_index().sort_values(by="Frases", ascending=False)
    df_dudas_melted = df_dudas.melt(id_vars="DudasFrecuentes", var_name="Tipo", value_name="Frecuencia")
    df_dudas_melted = df_dudas_melted[df_dudas_melted["Tipo"].isin(tipo_seleccionado_dudas)]
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=df_dudas_melted,
        x="DudasFrecuentes",
        y="Frecuencia",
        hue="Tipo",
        palette={"Frases": "#34a3d3", "Pacientes": "#b7b7bd"}, 
        ax=ax2
    )
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha="right")
    ax2.set_ylabel("Frecuencia")
    ax2.set_xlabel("")
    ax2.legend(title="Tipo")
    for container in ax2.containers:
        ax2.bar_label(container, fmt='%d', label_type='edge', fontsize=10)
    plt.tight_layout()
    st.pyplot(fig2)

with col_dudas_table:
    categoria_dudas = st.selectbox(
        "Selecciona una categoría de dudas:",
        df["DudasFrecuentes"].dropna().unique()
    )
    df_dudas_table = df[df["DudasFrecuentes"] == categoria_dudas][["num_entrevista", "frase"]]
    df_dudas_table = df_dudas_table.set_index("num_entrevista")
    st.dataframe(df_dudas_table, use_container_width=True)


# 3.2 Reflexiones/Comentarios: gráfico y tabla de ejemplos
st.markdown("### Reflexiones/Comentarios")

st.subheader("📌 Clasificación de comentarios/reflexiones")

st.write("""
Para las frases en las que los pacientes expresaban reflexiones o comentarios, que fueron **225**, se establecieron las siguientes categorías:

✅ **Dolor/Complicaciones:** Relacionadas con dolor, sufrimiento o complicaciones físicas derivadas de la rodilla.  
✅ **Deseo de operarse:** Expresan urgencia por la cirugía o críticas sobre la espera prolongada.  
✅ **Miedo/Preocupación/Ansiedad:** Reflejan angustia, miedo o inquietudes respecto a la cirugía o el postoperatorio.  
✅ **Confianza y Positividad:** Demuestran seguridad y optimismo respecto al procedimiento y el equipo médico.  
✅ **Rutina diaria:** Describen de manera neutral la vida cotidiana del paciente.  
✅ **Otros:** Frases que no encajan en las categorías anteriores.  
""")



col_reflexion_chart, col_reflexion_table = st.columns(2)

with col_reflexion_chart:
    tipo_seleccionado_reflexion = st.multiselect(
       "Selecciona qué frecuencia mostrar (Reflexiones):",
       ["Frases", "Pacientes"],
       default=["Frases", "Pacientes"]
    )
    df_reflexion = df.groupby("Tiporeflexión").agg(
        Frases=("Tiporeflexión", "count"),
        Pacientes=("num_entrevista", "nunique")
    ).reset_index().sort_values(by="Frases", ascending=False)
    df_reflexion_melted = df_reflexion.melt(id_vars="Tiporeflexión", var_name="Tipo", value_name="Frecuencia")
    df_reflexion_melted = df_reflexion_melted[df_reflexion_melted["Tipo"].isin(tipo_seleccionado_reflexion)]
    
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=df_reflexion_melted,
        x="Tiporeflexión",
        y="Frecuencia",
        hue="Tipo",
        palette={"Frases": "#34a3d3", "Pacientes": "#b7b7bd"}, 
        ax=ax3
    )
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha="right")
    ax3.set_ylabel("Frecuencia")
    ax3.set_xlabel("")
    ax3.legend(title="Tipo")
    for container in ax3.containers:
        ax3.bar_label(container, fmt='%d', label_type='edge', fontsize=10)
    plt.tight_layout()
    st.pyplot(fig3)
    
with col_reflexion_table:
    categoria_reflexion = st.selectbox(
        "Selecciona una categoría de comentario:",
        df["Tiporeflexión"].dropna().unique()
    )
    df_reflexion_table = df[df["Tiporeflexión"] == categoria_reflexion][["num_entrevista", "frase"]]
    df_reflexion_table = df_reflexion_table.set_index("num_entrevista")
    st.dataframe(df_reflexion_table, use_container_width=True)
