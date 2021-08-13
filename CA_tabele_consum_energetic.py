import pandas as pd
import sys

df_db_CA = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_CA.xlsx')
df_CA_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\CA.txt', delimiter="\t")
df_CA_dwg_merged_with_db = pd.merge(df_CA_dwg, df_db_CA, on = 'COD_ECHIPAMENT')
df_SA_CA = pd.DataFrame(df_CA_dwg_merged_with_db[['Nr_Crt',
                                                  'Denumire_element',
                                                  'SURSA_ALIMENTARE',
                                                  'COD_ECHIPAMENT',
                                                  'SIMBOL_ECHIPAMENT',
                                                  'CANTITATE',
                                                  'CONSUM_VEGHE_y',
                                                  'CONSUM_ALARMA_y']]).dropna()

# prin functia check_items() fac verificarea daca un cod de echipament este scris gresit sau nu se afla in
# vreunul din cele 2 dataframe-uri
def check_items():
    # citesc codurile de echipamente din df_CA_dwg si le introduc in lista read_check_list
    read_check_list = df_CA_dwg["COD_ECHIPAMENT"]
    # creez o noua lista in care introduc valori unice ale codurilor de chipamente(elimin codurile care apar de
    # mai multe ori)
    check_list = []
    # introduc valori unice ale codurilor de chipamente(elimin codurile care apar de mai multe ori) in lista check_list
    for item in read_check_list:
        if item not in check_list:
            check_list.append(item)
        # list_pwr_supply_labels.sort()
    #print(check_list)
    # citesc codurile de echipamente din baza de date a sistemului antiefractie
    read_check_list_db = df_db_CA['COD_ECHIPAMENT']
    check_list_db = []
    # introduc valori unice ale codurilor de chipamente(elimin codurile care apar de mai multe ori) in lista
    # check_list_db
    for item in read_check_list_db:
        if item not in check_list_db:
            check_list_db.append(item)
    #print(check_list_db)
    # fac verificarea codurilor de echipamente exportate din autocad cu cele existente in baza de date
    # in cazul in care codurile de echipamente exportate nu se regasesc in baza de date sau baza de date nu
    # contine vreun cod
    #  din codurile exportate programul va afisa acest lucru
    for item in check_list:
        if item not in check_list_db:
            print("\n \n \n Codul de produs", item, "nu se afla in baza de date sau a fost scris gresit")
            sys.exit(2)
        else:
            continue

            # print("Toate elementele folosite se regasesc in baza de date")
            # continue
            # sys.exit(2)
check_items()

# pentru calculul consumurilor pe sursele de alimentare este nevoie sa extrag denumirile tuturor surselor de
# alimentare din sistem
# aceste denumiri de surse sunt introduse in lista list_pwr_supply_labels si utilizate ulterior pentru calcule
read_pwr_supply_labels = df_SA_CA['SURSA_ALIMENTARE'].astype(str)
list_pwr_supply_labels = []
for item in read_pwr_supply_labels:
    if item not in list_pwr_supply_labels:
        list_pwr_supply_labels.append(item)
        list_pwr_supply_labels.sort()
list_pwr_supply_labels

def tabele_consum_energetic_CA():
    lista_tabele_consum_energetic_CA = []
    for i in range(len(list_pwr_supply_labels)):
        # creez variablia filtru_SA care selecteaza elementele din df_SA_CA ce au pe coloana "SURSA_ALIMENTARE"
        # denumirea sursei din
        # lista de surse de alimentare si au consumul de veghe sau consumul de alarma > 0
        filtru_SA = ((df_SA_CA['SURSA_ALIMENTARE'] == list_pwr_supply_labels[i]) &
                     ((df_SA_CA["CONSUM_VEGHE_y"] > 0) | (df_SA_CA["CONSUM_ALARMA_y"] > 0)))

        # creez data frame-ul table_calc_SA din data frame df_SA_CA si fac afisare pe coloana(.loc) pt valorile
        # selectate de variablia filt7
        # si in plus adaug coloanele "COD_ECHIPAMENT","CANTITATE","CONSUM_VEGHE", "CONSUM_ALARMA" la acest dataframe
        table_calc_SA = pd.DataFrame(df_SA_CA.loc[filtru_SA, ['Nr_Crt',
                                                              'Denumire_element',
                                                              'SURSA_ALIMENTARE',
                                                              'COD_ECHIPAMENT',
                                                              'SIMBOL_ECHIPAMENT',
                                                              'CANTITATE',
                                                              'CONSUM_VEGHE_y',
                                                              'CONSUM_ALARMA_y']])

        # print(table_calc_SA)

        df_tabele_calcule_energetice_CA = table_calc_SA.groupby(['Nr_Crt',
                                                                 'COD_ECHIPAMENT',
                                                                 'Denumire_element',
                                                                 'CONSUM_VEGHE_y',
                                                                 'CONSUM_ALARMA_y'], sort=True).agg(
            {'SIMBOL_ECHIPAMENT': lambda x: ', '.join(x),
             'CANTITATE': 'sum'}).reset_index()

        df_tabele_calcule_energetice_CA['CONSUM_TOTAL_VEGHE'] = df_tabele_calcule_energetice_CA['CONSUM_VEGHE_y'] * \
                                                                df_tabele_calcule_energetice_CA['CANTITATE']
        df_tabele_calcule_energetice_CA['CONSUM_TOTAL_ALARMA'] = df_tabele_calcule_energetice_CA['CONSUM_ALARMA_y'] * \
                                                                 df_tabele_calcule_energetice_CA['CANTITATE']

        df_tabele_calcule_energetice_CA.reset_index(drop=True, inplace=True)
        df_tabele_calcule_energetice_CA.index = df_tabele_calcule_energetice_CA.index + 1
        df_tabele_calcule_energetice_CA['Nr_Crt'] = df_tabele_calcule_energetice_CA.index

        #print(df_tabele_calcule_energetice_CA)

        # creare dictionar pentru a scrie tabelul de calcul consum curent CA in fisierul template word
        df_tabele_calcule_energetice_CA = df_tabele_calcule_energetice_CA.astype(str)
        df_tabele_calcule_energetice_CA.rename(columns={'Nr_Crt' : 'CA_consum_nr_crt'+str(i),
                                                        'Denumire_element' : 'CA_consum_denumire_element'+str(i),
                                                        'COD_ECHIPAMENT' : 'CA_consum_cod_echipament'+str(i),
                                                        'CANTITATE' : 'CA_consum_cantitate'+str(i),
                                                        'CONSUM_VEGHE_y' : 'CA_consum_veghe'+str(i),
                                                        'CONSUM_ALARMA_y' : 'CA_consum_alarma'+str(i),
                                                        'CONSUM_TOTAL_VEGHE' : 'CA_consum_total_veghe'+str(i),
                                                        'CONSUM_TOTAL_ALARMA' : 'CA_consum_total_alarma'+str(i)},
                                               inplace=True)
        dict_df_tabele_calcule_energetice_CA = df_tabele_calcule_energetice_CA.to_dict('records')
        #print(dict_df_tabele_calcule_energetice_CA)
        lista_tabele_consum_energetic_CA.append(dict_df_tabele_calcule_energetice_CA)
    return(lista_tabele_consum_energetic_CA)

if __name__ == '__main__':
    tabele_consum_energetic_CA()
