import streamlit as st
import os
from joblib import dump, load
import numpy as np
import tensorflow as tf
from keras.models import load_model
import pandas as pd

# Caminho para o arquivo do modelo
model_path = "new_model.keras"

try:
    ann1 = tf.keras.models.load_model(model_path)
    print("Modelo carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    st.error(f"Erro ao carregar o modelo: {e}")
    st.stop()

# Resto do seu código Streamlit
st.title('Modelo de classificação de práticas tributárias')
with st.form(key="include_dadosempresas"):
    input_Ativo_Def = st.number_input(label="Insira o valor do ativo total do ano anterior")
    input_Ativo_At = st.number_input(label="Insira o valor do ativo total do ano atual")
    input_EBIT = st.number_input(label="Insira o valor do EBIT da empresa")
    input_IRCS_Def = st.number_input(label="Insira o valor da despesa com IR e CSLL da empresa do ano anterior")
    input_IRCS = st.number_input(label="Insira o valor da despesa com IR e CSLL da empresa do ano atual")
    input_LAIR_Def = st.number_input(label="Insira o valor do LAIR da empresa do ano anterior")
    input_LAIR = st.number_input(label="Insira o valor do LAIR da empresa do ano atual")
    input_IMOB = st.number_input(label="Insira o valor do ativo imobilizado da empresa")
    input_DIV = st.number_input(label="Insira o valor da dívida de longo prazo")
    input_Setor = st.selectbox("Selecione o setor da empresa", ["Bens industriais", "Comunicações", "Consumo cíclico", "Consumo não cíclico",
                                                                 "Materiais básicos", "Petróleo, gás e biocombustíveis", "Saúde",
                                                                 "Tecnologia da informação", "Utilidade pública"])
    input_button_submit = st.form_submit_button("Classificar")

# Inicialização das variáveis
ROA = 0
PPE = 0
END = 0
ETRDIF = 0
ETRDIFDEF = 0
ind = 0
comun = 0
consc = 0
consnc = 0
matb = 0
pet = 0
saud = 0
ti = 0
util = 0

if input_button_submit:
    # Cálculo das métricas
    roa = [input_EBIT / input_Ativo_Def]
    ppe = [np.log((input_IMOB / input_Ativo_Def))]
    end = [input_DIV / input_Ativo_Def]
    etrdif = [(((input_LAIR * 0.34) - input_IRCS) / abs(input_LAIR))]
    etrdifdef = [(((input_LAIR_Def * 0.34) - input_IRCS_Def) / abs(input_LAIR_Def))]

    # Definição do setor
    if input_Setor == "Bens industriais":
        ind = 1.0
    elif input_Setor == "Comunicações":
        comun = 1.0
    elif input_Setor == "Consumo cíclico":
        consc = 1.0
    elif input_Setor == "Consumo não cíclico":
        consnc = 1.0
    elif input_Setor == "Materiais básicos":
        matb = 1.0
    elif input_Setor == "Petróleo, gás e biocombustíveis":
        pet = 0.0
    elif input_Setor == "Saúde":
        saud = 1.0
    elif input_Setor == "Tecnologia da informação":
        ti = 1.0
    elif input_Setor == "Utilidade pública":
        util = 1.0
    else:
        ind = comun = consc = consnc = matb = pet = saud = ti = util = 0.0

    # Criação do DataFrame para teste
    x_test = pd.DataFrame({"ROA": roa, "ETRDIF": etrdif, "ETRDIFDEF": etrdifdef, "END": end, "PPE": ppe,
                             "comun": comun, "consc": consc, "consnc": consnc, "pet": pet, "saud": saud,
                             "ind": ind, "ti": ti, "matb": matb, "UTIL": util}, index=[0])

    # Predição do modelo
    y_pred = ann1.predict(x_test)
    y_pred_arg = np.argmax(y_pred, axis=1)

    # Exibição do resultado
    if y_pred_arg == 1:
        st.write("Práticas tributárias muito conservadoras")
    elif y_pred_arg == 2:
        st.write("Práticas tributárias conservadoras")
    elif y_pred_arg == 3:
        st.write("Práticas tributárias agressivas")
    else:
        st.write("Práticas tributárias muito agressivas")

text = st.text('''Possibilidades de classificação, considerando o nível ótimo de práticas tributárias
pela perspectiva do desempenho corporativo:
    
    
    Práticas tributárias muito conservadoras;
    Práticas tributárias conservadoras;
    Práticas tributárias agressivas e
    Práticas tributárias muito agressivas.''')
