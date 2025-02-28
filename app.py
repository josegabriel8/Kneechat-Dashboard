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

# Definir estilo para todas las cards con un color uniforme
card_style_general = """
    <div style="padding: 10px; border-radius: 10px; background-color: #b7b7bd; text-align: center; color: white;">
        <h4 style="margin: 0;">{title}</h4>
        <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{value}</p>
    </div>
"""

# Mostrar los cards con el mismo color azul
col_card1.markdown(card_style_general.format(title="Entrevistas realizadas", value=entrevistas_count), unsafe_allow_html=True)
col_card2.markdown(card_style_general.format(title="Número total de frases de pacientes", value=623), unsafe_allow_html=True)
col_card3.markdown(card_style_general.format(title="Frases relevantes", value=frases_relevantes), unsafe_allow_html=True)
col_card4.markdown(card_style_general.format(title="Preguntas o dudas", value=54), unsafe_allow_html=True)


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

st.subheader("--------------------------------------------------------")


st.markdown("## Análisis Detallado por Categorías")


st.header("Frases y pacientes por categoría")

st.write("**En una segunda fase, la clasificación se profundizó aún más utilizando inteligencia artificial.**")
st.subheader("❓ Clasificación de dudas/preguntas")
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

st.subheader("--------------------------------------------------------")
st.subheader("--------------------------------------------------------")

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



###########################################


st.subheader("--------------------------------------------------------")
st.subheader("--------------------------------------------------------")

def clasificar_sentimiento(sent):
    if sent < -0.6:
        return 'Muy negativo'
    elif sent < -0.3:
        return 'Negativo'
    elif sent > 0.6:
        return 'Muy positivo'
    elif sent > 0.3:
        return 'Positivo'
    else:
        return 'Neutral'

# Crear la columna 'Sentimiento'
df['Sentimiento'] = df['sent_robertuito'].apply(clasificar_sentimiento)


import plotly.express as px
import pandas as pd

# Filtrar solo el tipo "Comentario/reflexión"
df_comentarioreflexion = df[df["Tipo"] == "Comentario/reflexión"].copy()
df_comentarioreflexion['num_entrevista'] = df_comentarioreflexion['num_entrevista'].astype(str)

# Agrupar por 'num_entrevista' y calcular la media, SEM y cantidad de frases
df_grouped = df_comentarioreflexion.groupby('num_entrevista', as_index=False).agg({
    'sent_robertuito': ['mean', 'sem', 'count']
})
df_grouped.columns = ['num_entrevista', 'mean_robertuito', 'sem_robertuito', 'count_frases']

# Clasificar sentimiento (se asume que la función clasificar_sentimiento está definida)
df_grouped['Sentimiento'] = df_grouped['mean_robertuito'].apply(clasificar_sentimiento)

# Calcular el intervalo de confianza (IC ~95%)
df_grouped['ci_robertuito'] = 1.96 * df_grouped['sem_robertuito']

# Mapeo de colores para cada categoría de sentimiento
color_dict = {
    "Muy negativo": "darkred",
    "Negativo": "lightcoral",
    "Neutral": "gray",
    "Positivo": "lightgreen",
    "Muy positivo": "darkgreen"
}

df_grouped['point_size'] = 12
# Crear gráfico interactivo con Plotly Express
fig_sentimiento = px.scatter(
    df_grouped,
    x=df_grouped.index,
    y="mean_robertuito",
    color="Sentimiento",
    color_discrete_map=color_dict,
    error_y="ci_robertuito",
    labels={
        "num_entrevista": "Número de Entrevista",
        "mean_robertuito": "Puntuación de Sentimiento"
    },
    title="Comparación de Sentimientos Promedio por Entrevista (IC ~95%)",
    size= "point_size",
    hover_data={
        "count_frases": True,
        "mean_robertuito": ':.2f',
        "num_entrevista": False  # ya se muestra en el eje x
    }
)

fig_sentimiento.update_layout(
    title_x=0.4  # Centra el título horizontalmente

)
# Agregar líneas horizontales de referencia
fig_sentimiento.add_hline(y=0.3, line_dash="dash", line_color="green", opacity=0.3)
fig_sentimiento.add_hline(y=0, line_dash="dash", line_color="grey", opacity=0.3)
fig_sentimiento.add_hline(y=-0.3, line_dash="dash", line_color="red", opacity=0.3)

# Actualizar hovertemplate para incluir información detallada
fig_sentimiento.update_traces(
    hovertemplate=(
        "<b>Entrevista: %{customdata[1]}</b><br>" +
        "Puntuación: %{y:.2f}<br>" +
        "Cantidad de frases: %{customdata[0]}<extra></extra>"
    ),
    customdata=df_grouped[['count_frases', 'num_entrevista']].values,

    
)

# Sección "Análisis de Sentimiento"
st.markdown("## Análisis de Sentimiento")

st.write("El análisis de sentimiento es una técnica de procesamiento del lenguaje natural que permite identificar y evaluar las emociones expresadas en un texto. En este caso, se aplica a los comentarios y reflexiones obtenidos en las entrevistas para determinar si el tono general es positivo, negativo o neutral.")

st.write("La puntuación de sentimiento se representa en una escala de -1 a 1, donde los valores negativos indican sentimientos negativos, los valores positivos reflejan sentimientos positivos y los valores cercanos a 0 representan un tono neutral. Esta puntuación se obtiene mediante modelos de análisis de texto y permite identificar patrones emocionales en los datos recopilados.")

st.write("*Para esta parte del Análisis se usaron solo las frases categorizadas como Comentario/reflexión ya que eran las que expresaban algún sentimiento o emoción*")


st.markdown("### Datos Generales")

col_card5, col_card6, col_card7, col_card8 = st.columns(4)


card_style = """
    <div style="padding: 10px; border-radius: 10px; background-color: {bg_color}; text-align: center; color: white;">
        <h4 style="margin: 0;">{title}</h4>
        <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{value}</p>
    </div>
"""

# Mostrar los cards con colores personalizados
col_card5.markdown(card_style.format(title="Promedio General de Sentimiento", value="-0.22", bg_color="#FF4B4B"), unsafe_allow_html=True)
col_card6.markdown(card_style.format(title="Entrevistas Negativas (Promedio)", value="12", bg_color="#D9534F"), unsafe_allow_html=True)
col_card7.markdown(card_style.format(title="Entrevistas Positivas (Promedio)", value="3", bg_color="#5CB85C"), unsafe_allow_html=True)
col_card8.markdown(card_style.format(title="Entrevistas Neutras", value="18", bg_color="#5BC0DE"), unsafe_allow_html=True)


st.plotly_chart(fig_sentimiento, use_container_width=True)


################################

import plotly.express as px
sentiment_order = ["Muy negativo", "Negativo", "Neutral", "Positivo", "Muy positivo"]

# Contar cantidad de frases por categoría de sentimiento
sentiment_counts = df_comentarioreflexion["Sentimiento"].value_counts().reindex(sentiment_order, fill_value=0)
sentiment_percent = (sentiment_counts / sentiment_counts.sum()) * 100  # Convertir a porcentaje

# Crear DataFrame para visualización
df_percent = pd.DataFrame({
    "Sentimiento": sentiment_order,
    "Porcentaje": sentiment_percent.values,
    "Cantidad de frases": sentiment_counts.values
})

# Crear gráfico de barras con Plotly
fig_sentimiento_bar = px.bar(
    df_percent,
    x="Sentimiento",
    y="Porcentaje",
    text="Porcentaje",
    color="Sentimiento",
    color_discrete_map=color_dict,
    labels={"Porcentaje": "Porcentaje (%)"},
    title="Porcentaje de Frases por Categoría de Sentimiento",
    hover_data={"Cantidad de frases": True}
)

fig_sentimiento_bar.update_layout(
    title_x=0.4  # Centra el título horizontalmente

)

# Ajustar formato de etiquetas sobre las barras
fig_sentimiento_bar.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>Porcentaje: %{y:.1f}%<br>Cantidad de frases: %{customdata[0]}<extra></extra>",
    customdata=df_percent[["Cantidad de frases"]].values
)

# Sección "Distribución de Sentimiento"
st.markdown("## Distribución de Sentimiento")
st.plotly_chart(fig_sentimiento_bar, use_container_width=True)


#categoria_sentimiento = st.selectbox(
#        "Selecciona una categoría de sentimiento:",
#        df_comentarioreflexion["Sentimiento"].dropna().unique()
#    )
df__table = df_comentarioreflexion[["frase","sent_robertuito","Tiporeflexión", "Sentimiento"]]


st.dataframe(df__table, use_container_width=True)