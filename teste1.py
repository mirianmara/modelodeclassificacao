import streamlit as st
import os
from joblib import dump, load
import numpy as np
import tensorflow as tf
from keras.models import model_from_json
import pandas as pd

st.title ('Modelo de classificação de práticas tributárias')
with st.form (key = "include_dadosempresas"):
    input_Ativo_Def = st.number_input (label = "Insira o valor do ativo total do ano anterior")
    input_Ativo_At = st.number_input(label = "Insira o valor do ativo total do ano atual")
    input_EBIT = st.number_input (label = "Insira o valor do EBIT da empresa")
    input_IRCS_Def = st.number_input (label = "Insira o valor da despesa com IR e CSLL da empresa do ano anterior")
    input_IRCS = st.number_input (label = "Insira o valor da despesa com IR e CSLL da empresa do ano atual")
    input_LAIR_Def = st.number_input (label = "Insira o valor do LAIR da empresa do ano anterior")
    input_LAIR = st.number_input (label = "Insira o valor do LAIR da empresa do ano atual")
    input_IMOB = st.number_input (label = "Insira o valor do ativo imobilizado da empresa")
    #input_VM = st.number_input (label = "Insira o valor de mercado da empresa do ano anterior")
    #input_PL = st.number_input (label = "Insira o valor do patrimônio líquido da empresa")
    input_DIV = st.number_input(label = "Insira o valor da dívida de longo prazo")
    input_Setor = st.selectbox ("Selecione o setor da empresa", ["Bens industriais", "Comunicações", "Consumo cíclico", "Consumo não cíclico",
"Materiais básicos", "Petróleo, gás e biocombustíveis", "Saúde","Tecnologia da informação", "Utilidade pública" ])
    input_button_submit = st.form_submit_button ("Classificar")
ROA = 0
#SIZE = 0
PPE = 0
END = 0
ETRDIF = 0
ETRDIFDEF = 0
#MB = 0
ind = 0
comun = 0
consc = 0
consnc = 0
matb = 0
pet = 0
saud = 0
ti = 0
util = 0
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
ann1 = model_from_json(loaded_model_json)
ann1.load_weights("model.h5")
if (input_button_submit):
    
    roa = [input_EBIT/input_Ativo_Def]
    #size = [np.log(input_Ativo_At)]
    ppe = [np.log ((input_IMOB/input_Ativo_Def))]
    #mb = [input_VM/input_PL]
    end = [input_DIV/input_Ativo_Def]
    etrdif = [(((input_LAIR*0.34)-input_IRCS)/abs(input_LAIR))]
    etrdifdef = [(((input_LAIR_Def*0.34)-input_IRCS_Def)/abs(input_LAIR_Def))]

    if (input_Setor == "Bens industriais"):
        ind = 1.0
    else:
        ind = 0.0
    if (input_Setor == "Comunicações"):
        comun = 1.0
    else:
        comun = 0.0
    if (input_Setor == "Consumo cíclico"):
        consc = 1.0
    else:
        consc = 0.0
    if (input_Setor == "Consumo não cíclico"):
        consnc = 1.0
    else:
        consnc = 0.0
    if (input_Setor == "Materiais básicos"):
        matb = 1.0
    else: 
        matb = 0.0
    if (input_Setor == "Petróleo, gás e biocombustíveis"):
        pet = 1.0
    else:
        pet = 0.0
    if (input_Setor == "Saúde"):

        saud = 1.0
    else:
        saud = 0.0
    if (input_Setor == "Tecnologia da informação"):
        ti = 1.0
    else:
        ti = 0.0
    if (input_Setor == "Utilidade pública"):
        util = 1.0
    else:
        util = 0.0
    x_test = pd.DataFrame ({"ROA":roa,"ETRDIF": etrdif, "ETRDIFDEF": etrdifdef,"END": end, "PPE":ppe, "comun":comun, "consc": consc,"consnc": consnc,"pet":pet,"saud": saud,"ind": ind, "ti":ti,"matb": matb,"UTIL":util },index=[0])
    y_pred = ann1.predict(x_test)
    y_pred_arg = np.argmax(y_pred, axis=1)
    if (y_pred_arg == 1):
        st.write ("Práticas tributárias muito conservadoras")
    elif (y_pred_arg == 2):
        st.write ("Práticas tributárias conservadoras")
    elif (y_pred_arg == 3):
        st.write ("Práticas tributárias agressivas")
    else:
        st.write ("Práticas tributárias muito agressivas") 
    
 



text = st.text ( '''Possibilidades de classificação, considerando o nível ótimo de práticas tributárias
pela perspectiva do desempenho corporativo:
    
    
    Práticas tributárias muito conservadoras;
    Práticas tributárias conservadoras;
    Práticas tributárias agressivas e
    Práticas tributárias muito agressivas.''')