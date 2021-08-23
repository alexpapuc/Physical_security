import pandas as pd
from CA_tabel_lista_cantitati import df_CA_lista_cantitati

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

print(df_CA_tabel_cantitati)