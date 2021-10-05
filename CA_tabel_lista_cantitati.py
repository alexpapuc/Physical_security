import pandas as pd
from CA_tabele_consum_energetic import df_CA_dwg_merged_with_db, dict_acumulatoare_SA_CA, tabele_consum_energetic_CA
pd.options.display.width=None





#initializare_modul = valori_tabele_consum_energetic_CA()
initializare_modul = tabele_consum_energetic_CA()
lista_dictionare_SA_CA = dict_acumulatoare_SA_CA()
print(lista_dictionare_SA_CA)


#pentru a putea crea dataframe, avem nevoie ca lista_dictionare_SA_CA sa fie o lista de dictionare, nu o
# lista de liste de dictionare
#pentru a avea ca rezultat o lista de dictionare dintr-o lista de liste de dictionare, folosim nested for de mai jos
flatten_matrix = []
for sublist in lista_dictionare_SA_CA:
    for val in sublist:
        flatten_matrix.append(val)
#print(flatten_matrix)

def CA_lista_cantitati():
    #dataframe df_SA_CA se va adauga in functia de calcul a listei de cantitati echipamente TVCI
    df_CA_lista_cantitati = pd.DataFrame(df_CA_dwg_merged_with_db[['Nr_Crt',
                                                                   'Denumire_element',
                                                                   'COD_ECHIPAMENT',
                                                                   'CANTITATE',
                                                                   'Producator',
                                                                   'Furnizor',
                                                                   'Document insotior']])
    df_SA_CA = pd.DataFrame(flatten_matrix)
    #print(df_SA_CA)
    df_CA_lista_cantitati = df_CA_lista_cantitati.append(df_SA_CA)

    #print(df_CA_lista_cantitati)
    df_CA_tabel_cantitati  = df_CA_lista_cantitati.groupby(['Nr_Crt',
                           'COD_ECHIPAMENT',
                           'Denumire_element',
                           'Producator',
                           'Furnizor',
                           'Document insotior']).agg({'CANTITATE' : 'sum'}).reset_index()


    df_CA_tabel_cantitati.set_index('COD_ECHIPAMENT', inplace = True)
    #elimin FCA(Filtrele de CA din lista de cantitati
    df_CA_tabel_cantitati.drop(index = ['FCA'], inplace = True)


    #resetez index-ul si il setez sa inceapa de la 1
    df_CA_tabel_cantitati = df_CA_tabel_cantitati.reset_index()
    df_CA_tabel_cantitati.index = df_CA_tabel_cantitati.index + 1
    df_CA_tabel_cantitati['Nr_Crt'] = df_CA_tabel_cantitati.index

    print(df_CA_tabel_cantitati[['Nr_Crt',
                           'Denumire_element',
                           'COD_ECHIPAMENT',
                           'CANTITATE',
                           'Producator',
                           'Furnizor',
                           'Document insotior']])

    df_CA_tabel_cantitati = df_CA_tabel_cantitati.astype(str)
    df_CA_tabel_cantitati.rename(columns={'Nr_Crt' : 'CA_cantitati_nr_crt',
                                                'Denumire_element': 'CA_cantitati_denumire_element',
                                                'COD_ECHIPAMENT': 'CA_cantitati_tip_element',
                                                'CANTITATE': 'CA_cantitati_cantitate',
                                                'Producator': 'CA_cantitati_producator',
                                                'Furnizor': 'CA_cantitati_furnizor',
                                                'Document insotior': 'CA_cantitati_CE'}, inplace=True)
    dict_df_CA_tabel_cantitati = df_CA_tabel_cantitati.to_dict('records')
    return(dict_df_CA_tabel_cantitati)

if __name__ == '__main__':
    CA_lista_cantitati()





#dict_SA_CA = df_SA_CA.to_dict('records')


#!!!!! de vazut cum sa import dictionarul cu acumulatoarele fara sa se ruleze de mai mult de
#o singura data modulul CA_tabele_consum_energetic