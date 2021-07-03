import pandas as pd

df_db_TVCI = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_TVCI.xlsx')
df_TVCI_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\TVCI.txt', delimiter="\t")

df_TVCI_equipments_with_attributes = pd.DataFrame(pd.merge(df_TVCI_dwg, df_db_TVCI, on='COD_ECHIPAMENT'))

# creare tabel de descriere a zonelor protejate subsistem TVCI
def TVCI_camera_labels():
    # creez un df df_table_cameras din df_TVCI_equipments_with_attributes cu coloanele ['SIMBOL_ECHIPAMENT','COD_ECHIPAMENT','SPATIUL_SUPRAVEGHEAT']
    df_table_cameras = df_TVCI_equipments_with_attributes[
        ['SIMBOL_ECHIPAMENT', 'COD_ECHIPAMENT', 'SPATIUL_SUPRAVEGHEAT']]
    # combin df_table_cameras cu baza de date in functie de coloana 'COD_ECHIPAMENT' pt a avea si coloanele din baza de date
    df_keep_only_cameras = pd.merge(df_table_cameras, df_db_TVCI, on='COD_ECHIPAMENT')
    # creez variabila filt care imi filtreaza din df_keep_only_cameras doar liniile care au pe coloana 'Rezolutie_MP' o valoare mai mare ca 0
    # asa selectez doar camerele. Pe coloana 'Rezolutie_MP' trebuie sa existe valori doar pentru camere!!!!!
    filt = (df_keep_only_cameras['Rezolutie_MP'] > 0)
    # creez un data frame ce contine elementele filtrate in baza variabilei filt de mai sus, dupa care le sortez in functie de 'SIMBOL_ECHIPAMENT'
    df_keep_only_cameras = pd.DataFrame(df_keep_only_cameras.loc[
                                            filt, ['SIMBOL_ECHIPAMENT', 'Denumire_element', 'COD_ECHIPAMENT',
                                                   'Modul_de_programare', 'SPATIUL_SUPRAVEGHEAT']])
    df_keep_only_cameras.sort_values(by='SIMBOL_ECHIPAMENT', ascending=True, inplace=True)
    # resetam indexul si il salvam pt dataframe
    df_keep_only_cameras.reset_index(drop=True, inplace=True)
    df_keep_only_cameras.index = df_keep_only_cameras.index + 1
    df_keep_only_cameras['nr_crt_zonare'] = df_keep_only_cameras.index.astype(str)

    df_keep_only_cameras.rename(
        columns={'nr_crt_zonare': 'TVCI_zonare_nr_crt',
                 'SIMBOL_ECHIPAMENT': 'TVCI_zonare_simbol_element',
                 'Denumire_element': 'TVCI_zonare_denumire_element',
                 'COD_ECHIPAMENT': 'TVCI_zonare_tip_element',
                 'Modul_de_programare': 'TVCI_zonare_mod_programare',
                 'SPATIUL_SUPRAVEGHEAT': 'TVCI_zonare_spatiu_supravegheat'}, inplace=True)
    df_keep_only_cameras = df_keep_only_cameras.to_dict('records')

    #return print(df_keep_only_cameras)
    return df_keep_only_cameras

if __name__ == '__main__':
    TVCI_camera_labels()
