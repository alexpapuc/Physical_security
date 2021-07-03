import pandas as pd
df_db = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_efractie.xlsx')
df_intrussion_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\zonare.txt',
                                delimiter="\t")

def creare_tabel_zonare():
    # global df_intrussion_dwg
    # df_db = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_efractie.xlsx')
    # combinam df_intrussion_dwg cu df_db in fct de 'COD_ECHIPAMENT' pt a avea denumirile de echipamente cu diacritice ă, etc
    df_intrussion = pd.merge(df_intrussion_dwg, df_db, on='COD_ECHIPAMENT')
    # creez data frame zonare_table cu coloanele necesare pt tabelul zonare
    zonare_table = pd.DataFrame(df_intrussion[['NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE',
                                               'SIMBOL_ECHIPAMENT', 'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA',
                                               'Tip cablu']])
    # sterg liniile ce nu contin valori pe coloana 'NUMAR_ZONA'
    # toate zonele din sistem vor trebui sa aiba atribuita o zona, altfel(daca nu se completeaza atributul corespunzator zonei in autocad) zona/zonele nu vor aparea in tabelul zonare
    zonare_table = zonare_table.dropna(subset=['NUMAR_ZONA'])
    # verificam daca elementele din fisierul importat din dwg se inseriaza sau nu. verificarea se face prin introducerea zonelor
    # care se repeta in lista seried_zones_list. Ulterior verific daca lista seried_zones_list are vreun element in ea sau nu.
    # daca are, inseamna ca avem zone inseriate si se executa conditiile de sub if
    # daca nu are, insemana ca nu avem zone inseriate si se executa conditiile de sub else
    check_seried_zones = list(zonare_table['NUMAR_ZONA'])
    #check_seried_zones
    unic_zones_list = []
    seried_zones_list = []
    for item in check_seried_zones:
        if item not in unic_zones_list:
            unic_zones_list.append(item)
        else:
            seried_zones_list.append(item)
    if len(seried_zones_list) != 0:
        # din df zonare_table grupez elementele care se inseriaza(elementele ce se inseriaza, apar in zonare cu acelasi nr de zona)
        # si le sortez in functie de coloana 'SIMBOL_ECHIPAMENT' astfel incat in tabelul de zonare simbolurile inseriate sa apara in ordine crescatoare
        # de exemplu vor fi afisate SOC1,SOC2,SOC3 nu SOC2,SOC3,SOC1
        df_group_seried_zones = zonare_table.loc[zonare_table.NUMAR_ZONA.duplicated(keep=False), :].sort_values(
            by='SIMBOL_ECHIPAMENT', ascending=True)
        # df_group_seried_zones
        # din df_group_seried_zones fac concatenarea pe coloanele'Denumire_element','COD_ECHIPAMENT','SIMBOL_ECHIPAMENT' (doar stringuri)
        # !!!Atentie!!!! in cazul in care la zonele ce se inseriaza nu exista aceleasi denumiri pe coloanele 'NUMAR_ZONA','TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA'
        # atunci in tabelul zonare zonele respective nu se vor inseria!!!! Este obligatoriu sa avem fix aceleasi denumiri
        concat_seried_zones = \
        df_group_seried_zones.groupby(['NUMAR_ZONA', 'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA'])[
            ['Denumire_element', 'COD_ECHIPAMENT', 'SIMBOL_ECHIPAMENT', 'Tip cablu']].agg(','.join).reset_index()
        # concat_seried_zones
        # scot zonele care se inseriaza si le bag intr-o lista pentru a le sterge din dataframe-ul zonare_table
        # dupa ce sterg zonele care se repeta in df zonare_table, o sa adaug la noul zonare table liniile cu zonele inseriate
        val_should_be_dropped = list(concat_seried_zones['NUMAR_ZONA'])
        # aceasta linie sterge din df zonare_table zonele care apar de 2 sau mai multe ori. Ulterior aceste zone se vor prelucra(inseria) si se vor adauga la data frame zonare_table  -> vezi ultimile linii din functie
        zonare_table = zonare_table.drop(
            zonare_table[zonare_table.NUMAR_ZONA.isin(val_should_be_dropped)].index.tolist())

        # pentru ca pe coloana cod echipament atunci cand avem acelasi tip de simbol, prin concatenare simbolul apare de mai multe ori
        # prin metoda split extrag coloana COD_ECHIPAMENT si o introduc intr-o lista
        # !!!Atentie!!! elementele extrase din coloana COD_ECHIPAMENT prin  metoda split nu sunt string-uri - sunt float-uri
        # creez o functie care itereaza elementele extrase din coloana COD_ECHIPAMENT prin metoda split si le introduce intr-o lista
        # in lista vor fi introduse doar elemente ce apar o singura data(asa realizez eliminarea codurilor de echipament ce apar de mai multe ori pe coloana COD_ECHIPAMENT in df concat_seried_zones )
        # concat_seried_zones.COD_ECHIPAMENT.str.split(',')
        def remove_duplicates(my_list):
            list = []
            for item in my_list:
                if item not in list:
                    list.append(item)
                    list.sort()
            return list

        concat_seried_zones['COD_ECHIPAMENT'] = concat_seried_zones.COD_ECHIPAMENT.str.split(',').apply(
            remove_duplicates)
        # pentru ca valorile extrase din coloana 'COD_ECHIPAMENT' reprezentau o lista, am creat variabila concatenare_cod_echip
        # prin care am transformat valorile de pe coloana 'COD_ECHIPAMENT' din lista in string
        # fac acelasi lucru si pentru coloana 'Denumire_element'
        concatenare_cod_echip = concat_seried_zones['COD_ECHIPAMENT'].apply(', '.join)
        concat_seried_zones['COD_ECHIPAMENT'] = concatenare_cod_echip
        concat_seried_zones['Denumire_element'] = concat_seried_zones.Denumire_element.str.split(',').apply(
            remove_duplicates)
        concatenare_den_elem = concat_seried_zones['Denumire_element'].apply(', '.join)
        concat_seried_zones['Denumire_element'] = concatenare_den_elem

        concat_seried_zones['Tip cablu'] = concat_seried_zones['Tip cablu'].str.split(',').apply(remove_duplicates)
        concatenare_tip_cablu = concat_seried_zones['Tip cablu'].apply(', '.join)
        concat_seried_zones['Tip cablu'] = concatenare_tip_cablu

        # din df_group_seried_zones fac concatenarea pe coloana'CANTITATE' (doar int-uri)
        concat_seried_zones_by_qty = df_group_seried_zones.groupby(['NUMAR_ZONA'])['CANTITATE'].sum().reset_index()
        # concat_seried_zones_by_qty

        # pentru realizarea df-ului final combin 'concat_seried_zones' cu 'concat_seried_zones_by_qty' in functie de coloana 'NUMAR_ZONA'
        seried_zones = (pd.merge(concat_seried_zones, concat_seried_zones_by_qty, on='NUMAR_ZONA'))
        seried_zones = seried_zones[
            ['NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'SIMBOL_ECHIPAMENT', 'TIP_ZONA',
             'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA', 'Tip cablu']]
        # seried_zones

        # la dataframe-ul zonare_table(care nu mai contine zonele care apareau de mai mult de 1 data) adaugam zonele inseriate dupa ce au fost prelucrate
        zonare_table = zonare_table.append(seried_zones, ignore_index=True, sort=False)
        # sortez valorile din tabelul final de zonare in functie de numarul zonei
        zonare_table = pd.DataFrame(zonare_table.sort_values(by=['NUMAR_ZONA'], ignore_index=True))
        # resetez index-ul si salvez resetarea in data frame
        zonare_table.reset_index(drop=True, inplace=True)
        # setez ca noul index sa inceapa de la 1
        zonare_table.index = zonare_table.index + 1
        zonare_table['nr_crt_zonare'] = zonare_table.index
        # apelez functia journal_cables_table si folosesc ca argument data frame-ul zonare table
        # aici pierd coloana "Tip cablu din DF-ul zonare_table astfel incat in excel sa nu mai afisez aceasta coloana
        # journal_cables_table(zonare_table)
        zonare_table = zonare_table[
            ['nr_crt_zonare', 'NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'SIMBOL_ECHIPAMENT',
             'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA']]
        df_zonare_table = zonare_table[
            ['nr_crt_zonare', 'NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'SIMBOL_ECHIPAMENT',
             'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA']]
        # redenumim coloanele cu denumirile ce vrem sa le afisam in excel
        zonare_table.rename(columns={'NUMAR_ZONA': 'Număr zonă', 'Denumire_element': 'Denumire echipament',
                                     'COD_ECHIPAMENT': 'Cod echipament', 'CANTITATE': 'Cantitate',
                                     'SIMBOL_ECHIPAMENT': 'Simbol echipament', 'TIP_ZONA': 'Tip zonă',
                                     'PARTITIE': 'Aria', 'DENUMIRE_ZONA_PROTEJATA': 'Zonă protejată'}, inplace=True)

        # scriem tabelul zonare in fisierul cu toate informatiile despre efractie
        #zonare_table.to_excel(writer, sheet_name='Zonare', index=True)
        # creare dictionar pentru docx-mailmerge in word
        df_zonare_table['PARTITIE'] = df_zonare_table['PARTITIE'].astype(int)
        df_zonare_table = df_zonare_table.astype(str)
        df_zonare_table.rename(columns={'nr_crt_zonare': 'efr_zonare_nr_crt',
                                        'NUMAR_ZONA': 'efr_zonare_nr_zona',
                                        'Denumire_element': 'efr_zonare_denumire_element',
                                        'COD_ECHIPAMENT': 'efr_zonare_tip_element',
                                        'CANTITATE': 'efr_zonare_cantitate',
                                        'SIMBOL_ECHIPAMENT': 'efr_zonare_simbol_element',
                                        'TIP_ZONA': 'efr_zonare_tip_zona',
                                        'PARTITIE': 'efr_zonare_partitie',
                                        'DENUMIRE_ZONA_PROTEJATA': 'efr_zonare_zona_protejata'}, inplace=True)
        dict_df_zonare_table = df_zonare_table.to_dict('records')
        print(dict_df_zonare_table)
        return dict_df_zonare_table


    else:
        # sortez valorile din tabelul final de zonare in functie de numarul zonei
        zonare_table = pd.DataFrame(zonare_table.sort_values(by=['NUMAR_ZONA'], ignore_index=True))
        # resetez index-ul si salvez resetarea in data frame
        zonare_table.reset_index(drop=True, inplace=True)
        # setez ca noul index sa inceapa de la 1
        zonare_table.index = zonare_table.index + 1
        zonare_table['nr_crt_zonare'] = zonare_table.index
        # apelez functia journal_cables_table si folosesc ca argument data frame-ul zonare table
        # journal_cables_table(zonare_table)
        zonare_table = zonare_table[
            ['nr_crt_zonare', 'NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'SIMBOL_ECHIPAMENT',
             'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA']]
        df_zonare_table = zonare_table[
            ['nr_crt_zonare', 'NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'SIMBOL_ECHIPAMENT',
             'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA']]
        # redenumim coloanele cu denumirile ce vrem sa le afisam in excel
        zonare_table.rename(columns={'NUMAR_ZONA': 'Număr zonă', 'Denumire_element': 'Denumire echipament',
                                     'COD_ECHIPAMENT': 'Cod echipament', 'CANTITATE': 'Cantitate',
                                     'SIMBOL_ECHIPAMENT': 'Simbol echipament', 'TIP_ZONA': 'Tip zonă',
                                     'PARTITIE': 'Aria', 'DENUMIRE_ZONA_PROTEJATA': 'Zonă protejată'}, inplace=True)

        # scriem tabelul zonare in fisierul cu toate informatiile despre efractie
        zonare_table.to_excel(writer, sheet_name='Zonare', index=True)

        df_zonare_table = df_zonare_table.astype(str)
        df_zonare_table.rename(columns={'nr_crt_zonare': 'efr_zonare_nr_crt',
                                        'NUMAR_ZONA': 'efr_zonare_nr_zona',
                                        'Denumire_element': 'efr_zonare_denumire_element',
                                        'COD_ECHIPAMENT': 'efr_zonare_tip_element',
                                        'CANTITATE': 'efr_zonare_cantitate',
                                        'SIMBOL_ECHIPAMENT': 'efr_zonare_simbol_element',
                                        'TIP_ZONA': 'efr_zonare_tip_zona',
                                        'PARTITIE': 'efr_zonare_partitie',
                                        'DENUMIRE_ZONA_PROTEJATA': 'efr_zonare_zona_protejata'}, inplace=True)
        dict_df_zonare_table = df_zonare_table.to_dict('records')
        print(dict_df_zonare_table)
        return dict_df_zonare_table

if __name__ == '__main__':
    creare_tabel_zonare()