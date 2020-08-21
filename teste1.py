import streamlit as st
import pandas as pd
import numpy as np

DATA_URL = 'data/TS_PROFESSOR_2017.csv'

st.title(DATA_URL)

@st.cache
def load_data(path):
    data = pd.read_csv(path)
    data = data.dropna()
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def format_municipio(el):
    try:
        return DICIONARIO['id_municipio'][el]
    except:
        return 'Não encontrado'

DICIONARIO = {
    "id_uf":{
        "11": "RO",
        "12": "AC",
        "13": "AM",
        "14": "RR",
        "15": "PA",
        "16": "AP",
        "17": "TO",
        "21": "MA",
        "22": "PI",
        "23": "CE",
        "24": "RN",
        "25": "PB",
        "26": "PE",
        "27": "AL",
        "28": "SE",
        "29": "BA",
        "31": "MG",
        "32": "ES",
        "33": "RJ",
        "35": "SP",
        "41": "PR",
        "42": "SC",
        "43": "RS",
        "50": "MS",
        "51": "MT",
        "52": "GO",
        "53": "DF",
    },
    "id_municipio": load_data('data/dicionario_municipios.csv').set_index('co_municipio').to_dict()['no_municipio']
}

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(DATA_URL)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data.head())

st.write('id_prova_brasil, id_uf ,id_municipio ,id_serie')
st.write(data['id_prova_brasil'].unique())
st.write(data['id_serie'].unique())

id_uf = st.sidebar.selectbox('UF', data['id_uf'].unique(), format_func=lambda el: DICIONARIO['id_uf'][str(el)])
id_municipio = st.sidebar.selectbox('Município', data[data['id_uf'] == id_uf]['id_municipio'].unique(), format_func=format_municipio)

st.write(id_uf)
#st.write(id_municipio)

st.write(data['tx_resp_q001'].value_counts())