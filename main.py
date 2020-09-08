import streamlit as st
import pandas as pd
import numpy as np

from sklearn.feature_selection import SelectKBest, VarianceThreshold
from sklearn.feature_selection import f_classif, mutual_info_classif

DATA_URL = 'data/TS_PROFESSOR_2017.csv'
RES_MUNICIPIOS_URL = 'data/TS_MUNICIPIO.xlsx'
MUNICIPIOS_URL = 'data/dicionario_municipios.csv'

st.title(DATA_URL)

@st.cache
def load_data(path):
    data = pd.read_csv(path)
    data = data.dropna()
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data
@st.cache
def load_excel(path):
    data = pd.read_excel(path)
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

def format_serie(el):
    return DICIONARIO['id_serie'][el]

def get_rank(el, mean):
    if(el > mean):
        return 1#'ACIMA DA MEDIA'
    elif(el < mean):
        return 2#'ABAIXO DA MEDIA'
    else:
        return 3#'IGUAL A MEDIA'

def classify(X, y, text):
    kbest = SelectKBest(score_func=f_classif, k=4)
    fit = kbest.fit(X,y)
    features = fit.transform(X)

    # Visualizando as features:
    st.write(text)
    st.write(features)
    return fit.get_support(indices=True)


def clear_variance(X):
    constant_filter = VarianceThreshold(threshold=0)
    constant_filter.fit(X)
    constant_columns = [column for column in X.columns if column not in X.columns[constant_filter.get_support()]]
    X_test = constant_filter.transform(X)
    
    st.write("Removed columns VarianceThreshold(threshold=0)")
    st.write(constant_columns)
    
    return X[X.columns[constant_filter.get_support()]]

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')

data = load_data(DATA_URL)
municipios = load_data(MUNICIPIOS_URL)

res_municipios = load_excel(RES_MUNICIPIOS_URL)
res_municipios = res_municipios.rename({'co_municipio': "id_municipio"}, axis="columns")
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")


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
    "id_municipio": municipios.set_index('co_municipio').to_dict()['no_municipio'],
    "id_serie":{
        5: "4ª série/5º ano EF",
        9: "8ª série/9º ano EF",
        12: "3ª Série do Ensino Médio",
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

# filters
id_uf = st.sidebar.selectbox('UF', data['id_uf'].unique(), format_func=format_uf)
id_municipio = st.sidebar.selectbox('Município', data[data['id_uf'] == id_uf]['id_municipio'].unique(), format_func=format_municipio)
id_serie = st.sidebar.selectbox('Série', list(DICIONARIO['id_serie']), format_func=format_serie)

rows = ([
        #'id_prova_brasil', 
        'id_uf', 
        'id_municipio', 
        'id_escola',
        'id_dependencia_adm',
        'id_localizacao',
        'id_turma',
        'co_professor',
        'id_serie',
        'in_preenchimento_questionario'
    ] + [f'tx_resp_q{x:03d}' for x in range(1,126)]
    )

filtered_data = data[data['id_municipio'] == id_municipio][rows]
filtered_data = filtered_data[filtered_data['id_serie'] == id_serie]

st.subheader(f'Filtros:\nUF: {format_uf(id_uf)}, Município: {format_municipio(id_municipio)}, Série: {format_serie(id_serie)}')
st.write(f"{filtered_data['id_escola'].nunique()} escolas")
if st.checkbox('Show raw data'):
    st.write(filtered_data)
    st.write(f'(linhas, colunas) = {filtered_data.shape}')


res_municipios_filtered = res_municipios[res_municipios['id_municipio'] == id_municipio]

municipio_professor = res_municipios_filtered.merge(filtered_data)

MEDIA_MT = municipio_professor['media_5_mt'].mean()
MEDIA_LP = municipio_professor['media_5_lp'].mean()
if st.checkbox('sklearn SelectKBest'):
    X = municipio_professor[[f'tx_resp_q{x:03d}' for x in range(1,126)]]
    X = X.apply(lambda x: list(map(ord, x)))
    X = clear_variance(X)

    y = municipio_professor['media_5_mt'].apply(lambda x: get_rank(x, MEDIA_MT))
    cols = classify(X,y, 'media_5_mt')
    st.write(X.iloc[:,cols])

    y = municipio_professor['media_5_lp'].apply(lambda x: get_rank(x, MEDIA_LP))
    cols = classify(X,y, 'media_5_lp')
    st.write(X.iloc[:,cols])

if st.checkbox('sklearn LogisticRegression'):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(max_iter=2000)
    from sklearn.feature_selection import RFE
    rfe = RFE(model, 4)

    X = municipio_professor[[f'tx_resp_q{x:03d}' for x in range(1,126)]]
    X = X.apply(lambda x: list(map(ord, x)))
    y = municipio_professor['media_5_mt'].apply(lambda x: get_rank(x, MEDIA_MT))
    fit = rfe.fit(X, y)
    cols = fit.get_support(indices=True)
    st.write("Número de features: {}".format(fit.n_features_))
    st.write(X.iloc[:,cols])