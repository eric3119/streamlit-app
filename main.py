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

def format_uf(el):
    return DICIONARIO['id_uf'][str(el)]

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
    "id_municipio": load_data('data/dicionario_municipios.csv').set_index('co_municipio').to_dict()['no_municipio'],
    "id_serie":{
        "5": "4ª série/5º ano EF",
        "9": "8ª série/9º ano EF",
        "12": "3ª Série do Ensino Médio",
    },
    "id_dependencia_adm":{
        "1": "Federal",
        "2": "Estadual",
        "3": "Municipal",
        "4": "Privada",
    },
    "id_localizacao":{
        "1": "Urbana",
        "2": "Rural",
    },
    "id_preenchimento_questionario":{
        "0": "Não preenchido",
        "1": "Preenchido parcial ou totalmente",
    }
}

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(DATA_URL)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

# filters
id_uf = st.sidebar.selectbox('UF', data['id_uf'].unique(), format_func=format_uf)
id_municipio = st.sidebar.selectbox('Município', data[data['id_uf'] == id_uf]['id_municipio'].unique(), format_func=format_municipio)

rows = ([
        #'id_prova_brasil', 
        #'id_uf', 
        #'id_municipio', 
        'id_escola',
        'id_dependencia_adm',
        'id_localizacao',
        'id_turma',
        'co_professor',
        'id_serie',
        'in_preenchimento_questionario'
    ]# + [f'tx_resp_q{x:03d}' for x in range(1,126)]
    )

filtered_data = data[data['id_municipio'] == id_municipio][rows]

st.subheader(f'Filtros - UF: {format_uf(id_uf)}, Município: {format_municipio(id_municipio)}')
st.write(f"{filtered_data['id_escola'].nunique()} escolas")
if st.checkbox('Show raw data'):
    st.write(filtered_data)
    st.write(f'(linhas, colunas) = {filtered_data.shape}')

#st.write(id_municipio)

#st.write(filtered_data['tx_resp_q001'].value_counts())