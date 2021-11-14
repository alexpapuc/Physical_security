import pandas as pd
import time
from pyautocad import Autocad, APoint

df_db = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_efractie.xlsx')
df_intrussion_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\zonare.txt',
                                delimiter="\t")
df_data_points = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm'\
'\Pandas Safe World Design\Pandas Docx Merge Safe World Design\Schema_bloc_antiefractie'\
'\Insertion_points_zone_acad.xls', converters={'NUMAR_ZONA':str})

pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 200)

acad = Autocad(create_if_not_exists=True)
acad.Application.Documents.Open (r'C:\Users\alexa\Desktop\Proiecte PyCharm'\
'\Pandas Safe World Design\Pandas Docx Merge Safe World Design\Schema_bloc_antiefractie\Schema_bloc_antiefractie.dwg')
#acad.prompt('Salut din pyautocad!')
#print(acad.doc.Name)
time.sleep(12) # ofer timp pentru a se deschide fisierul autocad

df_puncte_de_inserare = pd.DataFrame(df_data_points[['NUMAR_ZONA','Position X', 'Position Y']])
df_puncte_de_inserare = df_puncte_de_inserare.sort_values(by = ['NUMAR_ZONA'], ascending=True, inplace=False)
df_puncte_de_inserare.reset_index(drop=True, inplace=True)
dict_puncte_inserare = df_puncte_de_inserare.to_dict(orient = 'index')
print(dict_puncte_inserare)

def tabel_zonare():
    # combinam df_intrussion_dwg cu df_db in fct de 'COD_ECHIPAMENT' pt a avea denumirile de echipamente cu diacritice ă, etc
    df_intrussion = pd.merge(df_intrussion_dwg, df_db, on='COD_ECHIPAMENT')
    # creez data frame zonare_table cu coloanele necesare pt tabelul zonare
    zonare_table = pd.DataFrame(df_intrussion[['NUMAR_ZONA',
                                               'COD_ECHIPAMENT',
                                               'SIMBOL_ECHIPAMENT',
                                               'DENUMIRE_ZONA_PROTEJATA',
                                               'Denumire_bloc_ACAD']])
    # sterg liniile ce nu contin valori pe coloana 'NUMAR_ZONA'
    # toate zonele din sistem vor trebui sa aiba atribuita o zona, altfel(daca nu se completeaza atributul corespunzator zonei in autocad) zona/zonele nu vor aparea in tabelul zonare
    zonare_table = zonare_table.dropna(subset=['NUMAR_ZONA'])
    zonare_table = zonare_table.sort_values(by = ['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT'], ascending=True, inplace=False)
    #print(zonare_table)

    """extrag "Zona " din numerotarea zonelor(coloana efr_zonare_nr_zona)"""
    zonare_table['NUMAR_ZONA'] = zonare_table['NUMAR_ZONA'].apply(lambda x: x.lstrip("zZona "))
    print(zonare_table)
    """resetez indexul pt ca indexul vechi nu contine numere consecutive(am sters linii cand am aplicat dropna mai sus)"""
    zonare_table.reset_index(drop=True, inplace=True)
    #zonare_table = zonare_table.to_dict(orient = 'index')
    #print(zonare_table)

    #fac merge intre df zonare si df puncte de insert in Acad pt a lucra cu un singur df
    df_zone_cu_APoint = pd.merge(zonare_table, df_puncte_de_inserare, on='NUMAR_ZONA')
    df_zone_cu_APoint = df_zone_cu_APoint.to_dict(orient = 'index')

    return df_zone_cu_APoint

#apelez functia tabel_zonare() si stochez dictionarul in variabila dict_zone_inseriate_APoint
dict_zone_inseriate_APoint =  tabel_zonare()

"""creez o lista goala in care introduc cate o singura data numerele zonelor. Zonele inseriate apar de mai multe ori 
(de ex zona 01 poate sa apara de 5 ori) in dictionarul returnat de functia tabel_zonare().
In dictionarul count_zone_inseriate introduc key label-ul zonelor iar ca val o sa se introduca valoarea rezultata prin
numararea zonei. De ex daca zona 01 apare de 5 ori o sa avem {'01' : '5'}"""
lista_zone_inseriate = []
count_zone_inseriate = {}

for key, value in dict_zone_inseriate_APoint.items():
    if dict_zone_inseriate_APoint[key]['NUMAR_ZONA'] not in lista_zone_inseriate:
        lista_zone_inseriate.append(dict_zone_inseriate_APoint[key]['NUMAR_ZONA'])

for key, value in dict_zone_inseriate_APoint.items():
    if dict_zone_inseriate_APoint[key]['NUMAR_ZONA'] in lista_zone_inseriate:
        count_zone_inseriate.setdefault(dict_zone_inseriate_APoint[key]['NUMAR_ZONA'], 0)
        count_zone_inseriate[dict_zone_inseriate_APoint[key]['NUMAR_ZONA']] += 1

#print(count_zone_inseriate)
"""prin cele 2 for de mai jos iterez dictionarul count_zone_inseriate si in functie de numarul datilor pentru care 
apare o zona inseriata, se translateaza pe axa oX cu valoarea deplasare_axa_X, punctul de inserare in autocad 
al blocul corespunzator simbolului iterat
valoare = 1 -> pleaca de la 1 pentru ca rezultatul numararii zonelor inseriate este minim 1
acad.model.InsertBlock(APoint(coordonata_axa_X, coordonata_axa_Y), 'denumire_bloc_de_inserat', 1, 1, 1, 0=unghirotation) 
text = acad.model.AddText("text_de_inserat", APoint(coordonata_axa_X, coordonata_axa_Y), 0.2=inaltime text)"""

for key, value in count_zone_inseriate.items():
    valoare = 1
    deplasare_axa_X = 0
    for index, dictionar in dict_zone_inseriate_APoint.items():
        if dict_zone_inseriate_APoint[index]['NUMAR_ZONA'] == key and valoare <= value:
            acad.model.InsertBlock(APoint(dict_zone_inseriate_APoint[index]['Position X'] + deplasare_axa_X,
                                         dict_zone_inseriate_APoint[index]['Position Y']),
                                         dict_zone_inseriate_APoint[index]['Denumire_bloc_ACAD'], 1, 1, 1,0)
            text_simbol = acad.model.AddText(dict_zone_inseriate_APoint[index]['SIMBOL_ECHIPAMENT'],
                                    APoint(dict_zone_inseriate_APoint[index]['Position X'] + deplasare_axa_X - 0.07,
                                    dict_zone_inseriate_APoint[index]['Position Y'] + 0.35), 0.2)
            if valoare == value:
                print(valoare)
                text_zona = acad.model.AddText(dict_zone_inseriate_APoint[index]['DENUMIRE_ZONA_PROTEJATA'],
                                    APoint(dict_zone_inseriate_APoint[index]['Position X'] + deplasare_axa_X + 0.8,
                                    dict_zone_inseriate_APoint[index]['Position Y'] - 0.1), 0.2)

            deplasare_axa_X += 1.2
            print(deplasare_axa_X)
            valoare += 1
