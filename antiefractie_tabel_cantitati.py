import pandas as pd
from antiefractie import calcul_capacitate_acumulatoare
df_db = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_efractie.xlsx')
df_read_zonare = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\zonare.txt',
                             delimiter="\t")

#print(df_acumulatoare)



def creare_tabel_lista_cantitati():
    # global df_intrussion_dwg
    qty_table = df_read_zonare.groupby("COD_ECHIPAMENT")["CANTITATE"].count()
    #qty_table = df_acumulatoare.groupby("COD_ECHIPAMENT")["CANTITATE"].count()
    # print(qty_table.index)
    final_qty_table = pd.merge(qty_table, df_db, on="COD_ECHIPAMENT")
    # print(final_qty_table["COD_ECHIPAMENT"])
    # Pentru ca in lista de cantitati apar si alarma de incendiu, Tamperul, le-am bagat intr-o lista dupa care se face stergerea lor din tabel
    list_value_need_dropped = ['Alarma incendiu', 'Tamper']
    final_qty_table = final_qty_table.drop(
        final_qty_table[final_qty_table.COD_ECHIPAMENT.isin(list_value_need_dropped)].index.tolist())

    # creez dataframe-ul pt a afisa ce coloane ma intereseaza si fac filtrarea in functie de coloana 'Nr. Crt'
    # pt ca nu vreau sa afisez coloana 'Nr. Crt', fac atribuirea df-ului la el insusi dar fara coloana 'Nr. Crt'

    final_qty_table = pd.DataFrame(final_qty_table[
                                       ['Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'Producator', 'Furnizor',
                                        'Document insotior', 'Nr. Crt']]).sort_values(by='Nr. Crt', ascending=True)

    final_qty_table = final_qty_table[
        ['Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'Producator', 'Furnizor',
         'Document insotior']]

    df_final_qty_table_for_word = final_qty_table[
        ['Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'Producator', 'Furnizor',
         'Document insotior']]

    final_qty_table.reset_index(drop=True, inplace=True)
    final_qty_table.index = final_qty_table.index + 1
    # sortez valorile afisate in functie de 'CANTITATE' si 'COD_ECHIPAMENT'
    # final_qty_table = final_qty_table.sort_values(by=['Denumire_element', 'CANTITATE'], ascending=False)
    final_qty_table.rename(columns={'COD_ECHIPAMENT': 'Cod echipament', 'CANTITATE': 'Cantitate'}, inplace=True)
    # print(final_qty_table)
    # final_qty_table.to_excel(writer, sheet_name='Cantitati echip', index=True)

    df_final_qty_table_for_word.reset_index(drop=True, inplace=True)
    df_final_qty_table_for_word.index = df_final_qty_table_for_word.index + 1
    df_final_qty_table_for_word['nr_crt_cantitati'] = df_final_qty_table_for_word.index
    df_final_qty_table_for_word = df_final_qty_table_for_word[
        ['nr_crt_cantitati', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'Producator', 'Furnizor',
         'Document insotior']]

    df_final_qty_table_for_word = df_final_qty_table_for_word.astype(str)
    df_final_qty_table_for_word.rename(columns={'nr_crt_cantitati': 'efr_cantitati_nr_crt',
                                                'Denumire_element': 'efr_cantitati_denumire_element',
                                                'COD_ECHIPAMENT': 'efr_cantitati_tip_element',
                                                'CANTITATE': 'efr_cantitati_cantitate',
                                                'Producator': 'efr_cantitati_producator',
                                                'Furnizor': 'efr_cantitati_furnizor',
                                                'Document insotior': 'efr_cantitati_CE'}, inplace=True)
    dict_df_final_qty_table_for_word = df_final_qty_table_for_word.to_dict('records')
    # print(dict_df_final_qty_table_for_word)
    return dict_df_final_qty_table_for_word

