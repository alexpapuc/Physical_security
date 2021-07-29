from TVCI_lista_echipamente import *
df_db_TVCI = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_TVCI.xlsx')
df_TVCI_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\TVCI.txt', delimiter="\t")

#creez o variabila dict_lista_cantitati_TVCI in care stochez ceea ce returneaza fct TVCI_equipment_qty_table()
dict_lista_cantitati_TVCI = TVCI_equipment_qty_table()

#convertesc dictionarul intr-un dataframe
df_lista_cantitati_TVCI = pd.DataFrame(dict_lista_cantitati_TVCI)

#din dataframe introduc intr-o lista coloana cu codurile de echipamente
lista_coduri_echipamente_TVCI = list(df_lista_cantitati_TVCI['TVCI_qty_tip_element'])

dict_caract_tehnice_TVCI = {}
lista_dict_caract_tehnice_TVCI = []

#verific fiecare cod de echipament in baza de date si pentru fiecare cod extrag de pe coloana caracteristici tehnice
#din baza de date informatiile despre echipamentul respectiv, informatii ce vor fi stocate intr-o lista de dictionare
#ce vor fi returnate pt a fi utilizate in modulul main.
for i in range(len(lista_coduri_echipamente_TVCI)):
    filt = df_db_TVCI["COD_ECHIPAMENT"] == lista_coduri_echipamente_TVCI[i]
    df_get_caract_tehnice = pd.DataFrame(df_db_TVCI.loc[filt, ['COD_ECHIPAMENT','Caracteristici tehnice']])
    caracteristici_tehnice = df_get_caract_tehnice['Caracteristici tehnice'].iloc[0]
    dict_caract_tehnice_TVCI.update({'var_tvci'+ str(i) : caracteristici_tehnice})
    lista_dict_caract_tehnice_TVCI.append(dict_caract_tehnice_TVCI)
#print(dict_caract_tehnice_TVCI)

def variabile_caracteristici_tehnice_TVCI():
    return lista_dict_caract_tehnice_TVCI


if __name__ == '__main__':
    variabile_caracteristici_tehnice_TVCI()