import pandas as pd
#from antiefractie import preluare_coduri_echip_din_lista_cantitati_efractie
#from antiefractie import efr_coduri_echip_pt_fise_tehnice
from antiefractie import *

df_db = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_efractie.xlsx')
df_intrussion_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\zonare.txt',
                                delimiter="\t")

#print(df_db.columns)
#print(df_intrussion_dwg.columns)

dict_lista_cantitati_efr = creare_tabel_lista_cantitati()
df_lista_cantitati_efr = pd.DataFrame(dict_lista_cantitati_efr)
lista_coduri_echipamente_antiefractie = list(df_lista_cantitati_efr['efr_cantitati_tip_element'])

# test = preluare_coduri_echip_din_lista_cantitati_efractie()
# lista_coduri_echipamente_antiefractie = efr_coduri_echip_pt_fise_tehnice()


dict_caract_tehnice_antiefractie = {}
lista_dict_caract_tehnice_antiefractie = []



for i in range(len(lista_coduri_echipamente_antiefractie)):
    filt = df_db["COD_ECHIPAMENT"] == lista_coduri_echipamente_antiefractie[i]
    df_get_caract_tehnice = pd.DataFrame(df_db.loc[filt, ['COD_ECHIPAMENT','Caracteristici tehnice']])
    caracteristici_tehnice = df_get_caract_tehnice['Caracteristici tehnice'].iloc[0]
    dict_caract_tehnice_antiefractie.update({'var_efr'+ str(i) : caracteristici_tehnice})
    lista_dict_caract_tehnice_antiefractie.append(dict_caract_tehnice_antiefractie)
#print(dict_caract_tehnice_antiefractie)

def variabile_caracteristic_tehnice():
    return lista_dict_caract_tehnice_antiefractie


if __name__ == '__main__':
    variabile_caracteristic_tehnice()


# de vazut de ce se blocheaza la efractieeeee2 din main atunci
# cand #test = creare_tabel_lista_cantitati() este activ in acets modul