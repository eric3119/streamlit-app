DATA_URL = 'data/TS_PROFESSOR_2017.csv'
RES_MUNICIPIOS_URL = 'data/TS_MUNICIPIO.xlsx'
MUNICIPIOS_URL = 'data/dicionario_municipios.csv'

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