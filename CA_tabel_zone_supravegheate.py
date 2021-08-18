import pandas as pd
df_db_CA = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_CA.xlsx')
df_CA_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\CA.txt', delimiter="\t")

def CA_tabel_zone_supravegheate():
    df_tabel_zone_supravegheate = pd.DataFrame(df_CA_dwg[['APARTENENTA_FCA','ZONA_SUPRAVEGHEATA', 'SIMBOL_ECHIPAMENT']])
    filt_FCA_zone_supravegheate = (df_tabel_zone_supravegheate['APARTENENTA_FCA'] ==
                                   df_tabel_zone_supravegheate['SIMBOL_ECHIPAMENT'])
    #df_tabel_zone_supravegheate = df_tabel_zone_supravegheate[df_tabel_zone_supravegheate['ZONA_SUPRAVEGHEATA'].notnull()]
    df_tabel_FCA = pd.DataFrame(df_tabel_zone_supravegheate.loc[filt_FCA_zone_supravegheate, ['SIMBOL_ECHIPAMENT',
                                                                                              'ZONA_SUPRAVEGHEATA']])
    df_tabel_FCA = df_tabel_FCA.sort_values(by='SIMBOL_ECHIPAMENT', ignore_index=True)
    df_tabel_FCA['Denumire_zona_CA'] = 'Uşă acces ' + (df_tabel_FCA['ZONA_SUPRAVEGHEATA']).str.lower()
    df_tabel_FCA['Tip_zona'] = '24 Ore'
    df_tabel_FCA.index = df_tabel_FCA.index + 1
    df_tabel_FCA['Nr_Crt'] = df_tabel_FCA.index

    df_tabel_FCA = df_tabel_FCA.astype(str)
    #print(df_tabel_FCA.head())

    df_tabel_FCA.rename(columns= {'Nr_Crt' : 'CA_zonare_nr_crt',
                                  'Denumire_zona_CA' : 'CA_zonare_zona_CA',
                                  'SIMBOL_ECHIPAMENT' : 'CA_zonare_FCA',
                                  'ZONA_SUPRAVEGHEATA' : 'CA_zonare_zona_supravegheata',
                                  'Tip_zona' : 'CA_zonare_tip_zona'}, inplace=True)
    dict_tabel_FCA_word = df_tabel_FCA.to_dict('records')

    #print(dict_tabel_FCA_word)
    return(dict_tabel_FCA_word)

if __name__ == '__main__':
    CA_tabel_zone_supravegheate()