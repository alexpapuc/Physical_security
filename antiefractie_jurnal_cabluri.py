import pandas as pd
from antiefractie_tabel_zonare_cu_cablu import creare_tabel_zonare_cu_cablu

df_db = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_efractie.xlsx')
df_intrussion_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\zonare.txt',
                                delimiter="\t")

zonare_table = creare_tabel_zonare_cu_cablu()


def journal_cables_table(zonare_table):
    # creare df gol ce va folosit pt crearea tabelului cu jurnalul de cabluri
    df_cables_journal = pd.DataFrame(columns=['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu'])
    # creez o serie pt a putea adauga centrala de efractie si modulele de extensie la zone. Aceasta serie va fi coloana "Pana la"
    serie_pana_la = pd.Series(dtype=object)
    # combin dataframe-ul read zonare cu baza de date pentru a avea disponibile toate coloanele
    df_merged_zonare_with_db = pd.merge(df_intrussion_dwg, df_db, on="COD_ECHIPAMENT")

    # extragere centrala si module de extensie din zonare
    # creez un dataframe gol df_list_of_modules in care stochez centrala si modulele de extensie, dupa care introudc continutul
    # coloanei 'SIMBOL_ECHIPAMENT' in lista list_of_modules pe care o voi folosi pentru a putea crea seria Pana la
    # lista_module a fost adaugata manual pt a putea face identificarea centralei si mex-urilor in zonare
    # totodata adaug centrala si modulele de extensie la dataframe-ul df_cables_journal
    df_list_of_modules = pd.DataFrame(columns=['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu'])
    df_only_modules = pd.DataFrame(columns=['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu'])
    lista_module = ['Centrală', 'Surs', 'Micromod', 'Modul de', 'Tastat']

    for item in lista_module:
        filter_module = df_merged_zonare_with_db['Denumire_element'].str.contains(item)
        df_module = pd.DataFrame(
            df_merged_zonare_with_db.loc[filter_module, ['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu']])
        df_list_of_modules = df_list_of_modules.append(df_module)
        # df_cables_journal = df_cables_journal.append(df_module)
    # df_cables_journal
    list_of_modules = list(df_list_of_modules['SIMBOL_ECHIPAMENT'])
    list_of_modules.sort()
    #rint(list_of_modules)

    # functia get_nr_of_zones_per_device preia din baza de date numarul de zone de pe placa de baza a
    # fiecarei centrale sau modul de extensie
    def get_nr_of_zones_per_device(i):
        filt = df_merged_zonare_with_db["SIMBOL_ECHIPAMENT"] == list_of_modules[i]
        df_get_number_of_zones_from_db = pd.DataFrame(df_merged_zonare_with_db.loc[
                                                          filt, ['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu',
                                                                 'Nr_zone', 'Nr_total_zone', 'INDEX']])
        number_zone_per_device = df_get_number_of_zones_from_db['Nr_zone'].iloc[0].astype(int)
        return number_zone_per_device

    # creare dataframe cu elementele care sunt surse de alimentare
    df_merged_zonare_with_db.sort_values(by=['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT'], ascending=True)
    fliter_modules_with_power_supplies = (df_merged_zonare_with_db['Putere consumata (Watt)'] > 0)
    df_only_power_supplies = df_merged_zonare_with_db.loc[
        fliter_modules_with_power_supplies, ['Denumire_element', 'NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu',
                                             'Nr_zone', 'Nr_total_zone', 'INDEX', 'Nr. Crt']]
    df_only_power_supplies = df_only_power_supplies.sort_values(by=['Nr. Crt', 'SIMBOL_ECHIPAMENT'], ascending=True)
    df_only_power_supplies[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu']]
    df_only_power_supplies['Pana la'] = 'TAS'
    df_only_power_supplies = df_only_power_supplies[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Pana la', 'Tip cablu']]

    # creare dataframe cu elementele care nu sunt zone(centrale, module de extensie, tast, etc)
    # filter_modules = pd.isna(df_merged_zonare_with_db['NUMAR_ZONA'])
    # df_only_modules = df_merged_zonare_with_db.loc[filter_modules, ['Denumire_element','NUMAR_ZONA',
    # 'SIMBOL_ECHIPAMENT','Tip cablu','Nr_zone','Nr_total_zone','INDEX', 'Nr. Crt']]
    # df_only_modules = df_only_modules.sort_values(by = ['Nr. Crt','SIMBOL_ECHIPAMENT'], ascending = True)
    # df_only_modules[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu']]

    # adaug la df_only_modules BUS-urile de comunicatie
    nr_linii_BUS = int(input("Cate linii de BUS contine sistemul antiefractie"))
    lista_surse = []
    dictionar = {}
    for i in range(0, nr_linii_BUS):
        element = input(f'Introdu elementele componente pentru BUS{i + 1} separate de virgula si fara spatii:')
        element = element.split(',')
        dictionar.update({i + 1 : element})

        # df_only_modules = df_only_modules.append
        # print(lista)
        # nr_linii_BUS +=1
    # dictionar.items()

    serie_de_la_module = pd.Series(dtype=object)
    serie_pana_la_module = pd.Series(dtype=object)

    for i in range(len(dictionar)):
        for key, value in dictionar.items():
            serie_valori = pd.Series(dictionar.values())

    # serie_valori
    for i in range(len(serie_valori)):
        for p in range(len(serie_valori[i])):
            if ((p >= 0) & (p < (len(serie_valori[i]) - 1))):
                serie_de_la_module = serie_de_la_module.append(pd.Series(serie_valori[i][p]), ignore_index=True)
            if ((p >= 1) & (p < (len(serie_valori[i])))):
                serie_pana_la_module = serie_pana_la_module.append(pd.Series(serie_valori[i][p]), ignore_index=True)

    df_only_modules['SIMBOL_ECHIPAMENT'] = list(serie_de_la_module)
    df_only_modules['Pana la'] = list(serie_pana_la_module)
    df_only_modules['Tip cablu'] = 'Lyy6x0.22'
    df_only_modules[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Pana la', 'Tip cablu']]

    # creare dataframe cu sirene
    df_only_sirens = pd.DataFrame(columns=['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu'])
    lista_sirene = ['Siren', 'siren']

    for item in lista_sirene:
        filter_sirene = df_merged_zonare_with_db['Denumire_element'].str.contains(item)
        df_sirens = pd.DataFrame(
            df_merged_zonare_with_db.loc[filter_sirene, ['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'INDEX', 'Tip cablu']])
        df_only_sirens = df_only_sirens.append(df_sirens)
    df_only_sirens = df_only_sirens.sort_values(by='SIMBOL_ECHIPAMENT', ascending=False)
    df_only_sirens.rename(columns={'INDEX': 'Pana la'}, inplace=True)
    df_only_sirens = df_only_sirens[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Pana la', 'Tip cablu']]


    # creare dataframe cu elementele care sunt doar zone
    # df_only_zones = df_merged_zonare_with_db.dropna(subset=['NUMAR_ZONA'])
    # df_only_zones = df_only_zones.sort_values(by = ['NUMAR_ZONA','SIMBOL_ECHIPAMENT'], ascending = True)
    # zonare_table este preluat dion functia creare_tabel_zonare()
    # este atributul functiei journal_cables_table
    # pentru ca zonare table nu purta coloana tip cablu, am adaugat aceasta coloana si va trebui extrasa astfel
    # incat sa nu mai fie afisata in tabelul cu zonarea.
    df_only_zones = zonare_table
    # extrag din fiecare string "Zona " si convertesc valorile ramase in int-uri
    df_only_zones['NUMAR_ZONA'] = df_only_zones['NUMAR_ZONA'].replace({'Zona ': ''}, regex=True)
    df_only_zones['NUMAR_ZONA'] = df_only_zones['NUMAR_ZONA'].astype('int')

    no_of_zones = df_only_zones['NUMAR_ZONA'].count()

    # df_only_zones
    # print(zonare_table)

    # adaugare CE si ME(modulele de extensie) la seria pana la (se completeaza coloana pana la)
    # creez un dictionar gol in care voi introduce key =(CE, ME1, ME2, etc) iar ca valori voi asocia lista "zones"
    intrussion_modules_and_zones = {}
    count2 = 0
    count = 1
    for i in range(len(list_of_modules)):
        # creez o lista goala in care introduc valorile ce se vor asocia la fiecare modul de extensie in parte 1-8,9-16,17-24 etc
        zones = []
        for p in range(0, get_nr_of_zones_per_device(i)):
            zones.append(count)
            count += 1
            #print(zones)
            if count2 < no_of_zones:
                df_cables_journal = df_cables_journal.append(df_only_zones.iloc[count2], ignore_index=True)
                count2 += 1
                # print(count2)
            else:
                continue

        intrussion_modules_and_zones.update({list_of_modules[i]: zones})
        #print(intrussion_modules_and_zones)
    # afisare cheie si valoare pt dictioanr
    # intrussion_modules_and_zones.items()
    # creez o serie din dictionalul intrussion_modules_and_zones
    series = pd.Series(intrussion_modules_and_zones)
    # series

    for i in range(len(df_only_zones['NUMAR_ZONA'])):
        for key, value in intrussion_modules_and_zones.items():
            if df_only_zones['NUMAR_ZONA'].iloc[i] in value:
                serie_pana_la = serie_pana_la.append(pd.Series(key), ignore_index=True)

    #     serie_pana_la
    #     count2 = 0
    #     for i in range(len(list_of_modules)):
    #         for p in range(0, get_nr_of_zones_per_device(i)):
    #             df_cables_journal = df_cables_journal.append(df_only_zones.iloc[count2], ignore_index=True)
    #             serie_pana_la = serie_pana_la.append(pd.Series(list_of_modules[i]), ignore_index=True)
    #             count2 += 1

    df_cables_journal['Pana la'] = serie_pana_la
    df_cables_journal = df_cables_journal[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Pana la', 'Tip cablu']]
    # print(df_cables_journal)

    # adaunam cele 4 dataframe-uri pentru a avea un tabel final
    frames = [df_only_power_supplies, df_only_modules, df_only_sirens, df_cables_journal]
    result = pd.concat(frames)
    result.reset_index(drop=True, inplace=True)
    result.index = result.index + 1
    # creez coloana cu numerotarile cablurilor E1, E2, E2.....cate cabluri sunt in total
    label_cable = []
    for i in range(len(result['NUMAR_ZONA'])):
        label_cable.append('E' + str(i + 1))
    result['NUMAR_ZONA'] = label_cable
    result['SIMBOL_ECHIPAMENT'] = result['SIMBOL_ECHIPAMENT'].replace({',': ' prin '}, regex=True)
    result.rename(columns={'NUMAR_ZONA': 'Cod cablu', 'SIMBOL_ECHIPAMENT': 'De la', 'Pana la': 'Până la'}, inplace=True)
    result[['Cod cablu', 'De la', 'Până la', 'Tip cablu']]
    df_result_to_word = pd.DataFrame(result[['Cod cablu', 'De la', 'Până la', 'Tip cablu']])
    # scriem tabelul zonare in fisierul cu toate informatiile despre efractie
    #result.to_excel(writer, sheet_name='Jurnal cabluri', index=True)

    #creez dictionarul pentru a putea scrie in fisierul word
    df_result_to_word.reset_index(drop=True, inplace=True)
    df_result_to_word.index = df_result_to_word.index + 1
    df_result_to_word['nr_crt'] = df_result_to_word.index
    df_result_to_word[['nr_crt','Cod cablu', 'De la', 'Până la', 'Tip cablu']]
    df_result_to_word = df_result_to_word.astype(str)
    df_result_to_word.rename(columns={'nr_crt': 'efr_jurnal_nr_crt',
                                    'Cod cablu': 'efr_jurnal_cod_cablu',
                                    'De la': 'efr_jurnal_de_la',
                                    'Până la': 'efr_jurnal_pana_la',
                                    'Tip cablu': 'efr_jurnal_tip_cablu'}, inplace=True)
    dict_df_result_to_word = df_result_to_word.to_dict('records')
    #print(dict_df_result_to_word)
    return dict_df_result_to_word


if __name__ == '__main__':
    journal_cables_table(zonare_table)