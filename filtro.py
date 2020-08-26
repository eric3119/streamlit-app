import re
import pandas as pd

professor = pd.read_csv('data/TS_PROFESSOR_2017.csv')
professor = professor.dropna()

municipios = pd.read_excel('data/TS_MUNICIPIO.xlsx')
municipios = municipios.rename({'CO_MUNICIPIO': "ID_MUNICIPIO"}, axis="columns")

municipios_alagoas = municipios[municipios['NO_UF'] == 'Alagoas']
professor_alagoas = professor[professor['ID_UF'] == 27]

municipio_professor = municipios_alagoas.merge(professor_alagoas)

mean_cols_MT = list(
        filter(lambda x: re.match("nivel_.*_MT", str(x)), list(municipio_professor.columns))
    )
mean_cols_LP = list(
        filter(lambda x: re.match("nivel_.*_LP", str(x)), list(municipio_professor.columns))
    )

MEDIA_MT = municipio_professor[mean_cols_MT].mean().mean()
MEDIA_LP = municipio_professor[mean_cols_LP].mean().mean()
municipio_professor['MEDIA_MT'] = municipio_professor[mean_cols_MT].mean(axis=1)
municipio_professor['MEDIA_LP'] = municipio_professor[mean_cols_LP].mean(axis=1)

def get_rank(el, mean):
    if(el > mean):
        return 'ACIMA DA MEDIA'
    elif(el < mean):
        return 'ABAIXO DA MEDIA'
    else:
        return 'IGUAL A MEDIA'

municipio_professor['MEDIA_MT'] = municipio_professor['MEDIA_MT'].apply(lambda x: get_rank(x, MEDIA_MT))
municipio_professor['MEDIA_LP'] = municipio_professor['MEDIA_LP'].apply(lambda x: get_rank(x, MEDIA_LP))
