import pandas as pd
import sys
from itertools import chain
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)


df_db_CA = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_CA.xlsx')
df_CA_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\CA.txt', delimiter="\t")
df_CA_dwg_merged_with_db = pd.merge(df_CA_dwg, df_db_CA, on = 'COD_ECHIPAMENT')
#print(df_CA_dwg_merged_with_db)
df_SA_CA = pd.DataFrame(df_CA_dwg_merged_with_db[['Nr_Crt',
                                                  'Denumire_element',
                                                  'SURSA_ALIMENTARE',
                                                  'APARTENENTA_FCA',
                                                  'COD_ECHIPAMENT',
                                                  'SIMBOL_ECHIPAMENT',
                                                  'CANTITATE',
                                                  'CONSUM_VEGHE',
                                                  'CONSUM_ALARMA']]).dropna()

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
    print(check_list_db)
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

def verificare_simboluri_echipamente():
    lista_simboluri_echipamente_CA = list(df_CA_dwg['SIMBOL_ECHIPAMENT'])
    #print(lista_simboluri_echipamente_efr)
    lista_simboluri_verificate = []
    lista_simboluri_dublate = []
    for item in lista_simboluri_echipamente_CA:
        if item not in lista_simboluri_verificate:
            lista_simboluri_verificate.append(item)
        else:
            lista_simboluri_dublate.append(item)
    lista_simboluri_dublate.sort()
    if len(lista_simboluri_dublate) > 1:
        print('Verificati numerotarea echipamentelor!'
              ' Urmatoarele simboluri', ', '.join(map(str, lista_simboluri_dublate)),
              'apar de mai multe ori in fisierul autocad.')
        sys.exit(3)
    else:
        if len(lista_simboluri_dublate) == 1:
            print(f'Verificati numerotarea echipamentelor! Simbolul {lista_simboluri_dublate[0]} apare de'
             f' mai multe ori in fisierul autocad.')
            sys.exit(3)
    #continue


def verificare_elemente_ce_nu_au_sursa_atribuita():
    df_lipsa_SA = pd.DataFrame(df_CA_dwg[['COD_ECHIPAMENT','SURSA_ALIMENTARE','SIMBOL_ECHIPAMENT']])
    df_lipsa_SA = df_lipsa_SA[df_lipsa_SA['COD_ECHIPAMENT'].notnull()]
    filt_nan = df_lipsa_SA['SURSA_ALIMENTARE'].isnull()
    df_elemente_fara_SA = pd.DataFrame(df_lipsa_SA.loc[filt_nan,['SIMBOL_ECHIPAMENT']])
    df_elemente_fara_SA = df_elemente_fara_SA.sort_values(by=['SIMBOL_ECHIPAMENT'])
    elemente_fara_SA = list(df_elemente_fara_SA['SIMBOL_ECHIPAMENT'])
    if len(elemente_fara_SA) == 0:
        pass
    elif len(elemente_fara_SA) == 1:
        print(f'Simbolul {elemente_fara_SA[0]} nu are o sursa de alimentare atribuita')
        sys.exit(4)
    elif len(elemente_fara_SA) > 1:
        #print(f'Simbolurile {str(elemente_fara_SA)[1:-1]} nu au sursa de alimentare atribuita')
        print('Simbolurile',', '.join(map(str, elemente_fara_SA)), 'nu au sursa de alimentare atribuita')
        sys.exit(4)


def verificare_elemente_fara_simbol_atribuit():
    df_elemente_lipsa_simbol = pd.DataFrame(df_CA_dwg[['COD_ECHIPAMENT', 'SIMBOL_ECHIPAMENT']])
    df_elemente_lipsa_simbol = df_elemente_lipsa_simbol[df_elemente_lipsa_simbol['COD_ECHIPAMENT'].notnull()]
    filt_nan = df_elemente_lipsa_simbol['SIMBOL_ECHIPAMENT'].isnull()
    df_elemente_fara_simbol = pd.DataFrame(df_elemente_lipsa_simbol.loc[filt_nan,['COD_ECHIPAMENT']])
    df_elemente_fara_simbol = df_elemente_fara_simbol.sort_values(by=['COD_ECHIPAMENT'])
    elemente_fara_simbol = list(df_elemente_fara_simbol['COD_ECHIPAMENT'])
    if len(elemente_fara_simbol) == 0:
        pass
    elif len(elemente_fara_simbol) == 1:
        print(f'Echipamentul {elemente_fara_simbol[0]} nu are un simbol definit')
        sys.exit(4)
    elif len(elemente_fara_simbol) > 1:
        #print(f'Simbolurile {str(elemente_fara_SA)[1:-1]} nu au sursa de alimentare atribuita')
        print('Echipamentele',', '.join(map(str, elemente_fara_simbol)), 'nu au simboluri definite')
        sys.exit(4)

def lista_surse_alimentare_CA():
    # pentru calculul consumurilor pe sursele de alimentare este nevoie sa extrag denumirile tuturor surselor de
    # alimentare din sistem
    # aceste denumiri de surse sunt introduse in lista list_pwr_supply_labels si utilizate ulterior pentru calcule
    read_pwr_supply_labels = df_SA_CA['SURSA_ALIMENTARE'].astype(str)
    list_pwr_supply_labels = []
    for item in read_pwr_supply_labels:
        if item not in list_pwr_supply_labels:
            list_pwr_supply_labels.append(item)
            list_pwr_supply_labels.sort()
    #print(list_pwr_supply_labels)
    return(list_pwr_supply_labels)

def citire_valoare_capacitate_acc_CA():
    capacitate_acc_SA_CA = int(input(f'Introdu valoarea capacitatii acumulatorului utilizat la sursele de CA'))
    return capacitate_acc_SA_CA

def creare_dictionar_acc_surse_CA(capacitate_acc_SA_CA, lista_surse_alimentare_CA):
    # creare dictionar pentru acumulatoarele surselor de alimentare de la sistemul de CA
    filt_acc_SA_CA = (df_db_CA['Capacitate_Acumulator'] == capacitate_acc_SA_CA)
    df_acc_SA_CA = pd.DataFrame(df_db_CA.loc[filt_acc_SA_CA, ['Nr_Crt',
                                                              'Denumire_element',
                                                              'COD_ECHIPAMENT',
                                                              'CANTITATE',
                                                              'Producator',
                                                              'Furnizor',
                                                              'Document insotior']])
    dict_acc_SA_CA = df_acc_SA_CA.to_dict('records')
    copy_dict_acc_SA_CA = dict_acc_SA_CA.copy()

    # creez o lista goala in care voi stoca acumulatoarele surselor de alimentare ale CA
    lista_dict_acc_SA_CA = []

    for item in lista_surse_alimentare_CA:
        lista_dict_acc_SA_CA.append(copy_dict_acc_SA_CA)

    return lista_dict_acc_SA_CA

def tabele_consum_energetic_CA(lista_surse_alimentare_CA):
    lista_tabele_consum_energetic_CA =[]
    #lista_valori_calcule_sub_tabele_consum_energetic_CA =[]

    for i in range(len(lista_surse_alimentare_CA)):
        # creez variablia filtru_SA care selecteaza elementele din df_SA_CA ce au pe coloana "SURSA_ALIMENTARE"
        # denumirea sursei din
        # lista de surse de alimentare si au consumul de veghe sau consumul de alarma > 0
        filtru_SA = ((df_SA_CA['SURSA_ALIMENTARE'] == lista_surse_alimentare_CA[i]) &
                     ((df_SA_CA["CONSUM_VEGHE"] > 0) | (df_SA_CA["CONSUM_ALARMA"] > 0)))

        # creez data frame-ul table_calc_SA din data frame df_SA_CA si fac afisare pe coloana(.loc) pt valorile
        # selectate de variablia filtru_SA
        # si in plus adaug coloanele "COD_ECHIPAMENT","CANTITATE","CONSUM_VEGHE", "CONSUM_ALARMA" la acest dataframe
        table_calc_SA = pd.DataFrame(df_SA_CA.loc[filtru_SA, ['Nr_Crt',
                                                              'Denumire_element',
                                                              'SURSA_ALIMENTARE',
                                                              'COD_ECHIPAMENT',
                                                              'APARTENENTA_FCA',
                                                              'SIMBOL_ECHIPAMENT',
                                                              'CANTITATE',
                                                              'CONSUM_VEGHE',
                                                              'CONSUM_ALARMA']])

        print(table_calc_SA)

        # creez df_tabele_calcule_energetice_CA in care sortez in fct de Nr_Crt din baza de date si fac agregare
        # pe coloana SIMBOL_ECHIPAMENT - atunci cand sunt mai multe elemente de acelasi fel aplic functia lambda si
        # simbolurile de echipamente vor fi concatenate sub forma E1, E2, E3  etc
        # pe coloana APARTENENTA_FCA - atunci cand sunt mai multe filtre de control acces alimentate din acceeasi
        # sursa de alimentare aplic functia lambda pentru a concatena echipamentele care se repeta
        # simbolurile de echipamente vor fi concatenate sub forma E1, E2, E3  etc
        # pe coloana cantitate fac suma elementelor de acelasi fel
        df_tabele_calcule_energetice_CA = table_calc_SA.groupby(['Nr_Crt',
                                                                 'COD_ECHIPAMENT',
                                                                 'Denumire_element',
                                                                 'CONSUM_VEGHE',
                                                                 'CONSUM_ALARMA'], sort=True).agg(
            {'SIMBOL_ECHIPAMENT': lambda x: ', '.join(x),
             'APARTENENTA_FCA' : lambda x: ', '.join(x),
             'CANTITATE': 'sum'}).reset_index()

        df_tabele_calcule_energetice_CA['CONSUM_TOTAL_VEGHE'] = df_tabele_calcule_energetice_CA['CONSUM_VEGHE'] * \
                                                                df_tabele_calcule_energetice_CA['CANTITATE']
        df_tabele_calcule_energetice_CA['CONSUM_TOTAL_ALARMA'] = df_tabele_calcule_energetice_CA['CONSUM_ALARMA'] * \
                                                                 df_tabele_calcule_energetice_CA['CANTITATE']

        #creare variabile cu valorile totale de consum veghe, alarma ; variabilele vor fi folosite pt a scrie valorile
        #in tabelele de calcul al acumulatoarelor
        consum_total_veghe_CA_mA = df_tabele_calcule_energetice_CA['CONSUM_TOTAL_VEGHE'].sum()
        consum_total_alarma_CA_mA = df_tabele_calcule_energetice_CA['CONSUM_TOTAL_ALARMA'].sum()


        # resetez index-ul si il setez sa inceapa de la 1
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
                                                        'CONSUM_VEGHE' : 'CA_consum_veghe'+str(i),
                                                        'CONSUM_ALARMA' : 'CA_consum_alarma'+str(i),
                                                        'CONSUM_TOTAL_VEGHE' : 'CA_consum_total_veghe'+str(i),
                                                        'CONSUM_TOTAL_ALARMA' : 'CA_consum_total_alarma'+str(i)},
                                               inplace=True)
        dict_df_tabele_calcule_energetice_CA = df_tabele_calcule_energetice_CA.to_dict('records')
        #print(dict_df_tabele_calcule_energetice_CA)
        lista_tabele_consum_energetic_CA.append(dict_df_tabele_calcule_energetice_CA)

    #     #################################################################################################
    #     # creare variabile ce se vor scrie sub tabelele de calcul consum curent CA
    #     sursa_alim = lista_surse_alimentare_CA[i]
    #     filtru_control_acces = df_tabele_calcule_energetice_CA['APARTENENTA_FCA'].iloc[0]
    #     # capacitate_acc_SA_CA = input(f'Introdu valoarea capacitatii acumulatorului utilizat la sursele de CA')
    #     # ### de creat un dictionar pt acumulatorul utilizat astfel incat sa il adaug in lista de cantitati de la CA
    #     consum_total_veghe_CA_Amperi = consum_total_veghe_CA_mA/1000
    #     consum_total_alarma_CA_Amperi = consum_total_alarma_CA_mA/1000
    #
    #     # aici se convertesc rezultatele din float in ore si minute pentru capacitate acc\consum_veghe si consum_alarma
    #     timp_veghe = capacitate_acc_SA_CA / consum_total_veghe_CA_Amperi
    #     ore_veghe,minute_veghe = divmod(timp_veghe,1)
    #     minute_veghe = minute_veghe * 60
    #     if minute_veghe == 0:
    #         rezultat_timp_veghe = 'în stare de veghe: {}Ah / {}A = {}ore'.format(str(capacitate_acc_SA_CA),
    #                                                                              str(consum_total_veghe_CA_Amperi),
    #                                                                              int(ore_veghe))
    #     else:
    #         rezultat_timp_veghe = 'în stare de veghe: {}Ah / {}A = {}ore şi {}minute'.format(str(capacitate_acc_SA_CA),
    #                                                                     str(consum_total_veghe_CA_Amperi),
    #                                                                     int(ore_veghe),
    #                                                                     int(minute_veghe))
    #     print(rezultat_timp_veghe)
    #
    #     if consum_total_alarma_CA_Amperi != 0:
    #         timp_alarma = capacitate_acc_SA_CA / consum_total_alarma_CA_Amperi
    #         ore_alarma, minute_alarma = divmod(timp_alarma, 1)
    #         minute_alarma = minute_alarma * 60
    #         if minute_alarma == 0:
    #             rezultat_timp_alarma = 'în stare de alarmă: {}Ah / {}A = {}ore'.format(str(capacitate_acc_SA_CA),
    #                                                                                  str(consum_total_alarma_CA_Amperi),
    #                                                                                  int(ore_alarma))
    #         else:
    #             rezultat_timp_alarma = 'în stare de alarmă: {}Ah / {}A = {}ore şi {}minute'.format(str(capacitate_acc_SA_CA),
    #                                                                         str(consum_total_alarma_CA_Amperi),
    #                                                                         int(ore_alarma),
    #                                                                         int(minute_alarma))
    #
    #
    #     elif consum_total_alarma_CA_Amperi == 0:
    #         rezultat_timp_alarma = f'în stare de alarmă: nu există consum pe sursa de alimentare {sursa_alim}'
    #
    #     print(rezultat_timp_alarma)
    #     #timp_veghe = f'{timp_veghe:.2f}'
    #     #timp_alarma = f'{timp_alarma:.2f}'
    #
    #
    #     dict_val_tabel_consum_CA = {}
    #     dict_val_tabel_consum_CA.update({'CA_consum_SA' + str(i) : sursa_alim,
    #                                      'CA_consum_FCA' + str(i) : filtru_control_acces,
    #                                      'CA_consum_TOTAL_veghe_mA' + str(i) : str(consum_total_veghe_CA_mA),
    #                                      'CA_consum_TOTAL_alarma_mA' + str(i) : str(consum_total_alarma_CA_mA),
    #                                      'CA_acc_SA' + str(i) : str(capacitate_acc_SA_CA),
    #                                      'CA_consum_TOTAL_veghe_A' + str(i) : str(consum_total_veghe_CA_Amperi),
    #                                      'CA_consum_TOTAL_alarma_A' + str(i) : str(consum_total_alarma_CA_Amperi),
    #                                      'CA_timp_veghe_' + str(i) : str(rezultat_timp_veghe),
    #                                      'CA_timp_alarma_' + str(i) : str(rezultat_timp_alarma)})
    #
    #     lista_valori_calcule_sub_tabele_consum_energetic_CA.append(dict_val_tabel_consum_CA)
    #
    #     print(sursa_alim,
    #           filtru_control_acces,
    #           capacitate_acc_SA_CA,
    #           consum_total_veghe_CA_Amperi,
    #           consum_total_alarma_CA_Amperi,
    #           consum_total_veghe_CA_mA,
    #           consum_total_alarma_CA_mA,
    #           rezultat_timp_veghe, rezultat_timp_alarma)
    # #print(lista_valori_calcule_sub_tabele_consum_energetic_CA)
    # #print(lista_tabele_consum_energetic_CA)
    return lista_tabele_consum_energetic_CA


def valori_calcule_sub_tabele_consum_energetic_CA(capacitate_acc_SA_CA, lista_surse_alimentare_CA):
    #lista_tabele_consum_energetic_CA =[]
    lista_valori_calcule_sub_tabele_consum_energetic_CA =[]

    for i in range(len(lista_surse_alimentare_CA)):
        # creez variablia filtru_SA care selecteaza elementele din df_SA_CA ce au pe coloana "SURSA_ALIMENTARE"
        # denumirea sursei din
        # lista de surse de alimentare si au consumul de veghe sau consumul de alarma > 0
        filtru_SA = ((df_SA_CA['SURSA_ALIMENTARE'] == lista_surse_alimentare_CA[i]) &
                     ((df_SA_CA["CONSUM_VEGHE"] > 0) | (df_SA_CA["CONSUM_ALARMA"] > 0)))

        # creez data frame-ul table_calc_SA din data frame df_SA_CA si fac afisare pe coloana(.loc) pt valorile
        # selectate de variablia filtru_SA
        # si in plus adaug coloanele "COD_ECHIPAMENT","CANTITATE","CONSUM_VEGHE", "CONSUM_ALARMA" la acest dataframe
        table_calc_SA = pd.DataFrame(df_SA_CA.loc[filtru_SA, ['Nr_Crt',
                                                              'Denumire_element',
                                                              'SURSA_ALIMENTARE',
                                                              'COD_ECHIPAMENT',
                                                              'APARTENENTA_FCA',
                                                              'SIMBOL_ECHIPAMENT',
                                                              'CANTITATE',
                                                              'CONSUM_VEGHE',
                                                              'CONSUM_ALARMA']])

        #print(table_calc_SA)

        # creez df_tabele_calcule_energetice_CA in care sortez in fct de Nr_Crt din bazade date si fac agregare
        # pe coloana SIMBOL_ECHIPAMENT - atunci cand sunt mai multe elemente de acelasi fel aplic functia lambda si
        # simbolurile de echipamente vor fi concatenate sub forma E1, E2, E3  etc
        # pe coloana cantitate fac suma elementelor de acelasi fel
        df_tabele_calcule_energetice_CA = table_calc_SA.groupby(['Nr_Crt',
                                                                 'APARTENENTA_FCA',
                                                                 'COD_ECHIPAMENT',
                                                                 'Denumire_element',
                                                                 'CONSUM_VEGHE',
                                                                 'CONSUM_ALARMA'], sort=True).agg(
            {'SIMBOL_ECHIPAMENT': lambda x: ', '.join(x),
             'CANTITATE': 'sum'}).reset_index()

        df_tabele_calcule_energetice_CA['CONSUM_TOTAL_VEGHE'] = df_tabele_calcule_energetice_CA['CONSUM_VEGHE'] * \
                                                                df_tabele_calcule_energetice_CA['CANTITATE']
        df_tabele_calcule_energetice_CA['CONSUM_TOTAL_ALARMA'] = df_tabele_calcule_energetice_CA['CONSUM_ALARMA'] * \
                                                                 df_tabele_calcule_energetice_CA['CANTITATE']

        #creare variabile cu valorile totale de consum veghe, alarma ; variabilele vor fi folosite pt a scrie valorile
        #in tabelele de calcul al acumulatoarelor
        consum_total_veghe_CA_mA = df_tabele_calcule_energetice_CA['CONSUM_TOTAL_VEGHE'].sum()
        consum_total_alarma_CA_mA = df_tabele_calcule_energetice_CA['CONSUM_TOTAL_ALARMA'].sum()


        # resetez index-ul si il setez sa inceapa de la 1
        df_tabele_calcule_energetice_CA.reset_index(drop=True, inplace=True)
        df_tabele_calcule_energetice_CA.index = df_tabele_calcule_energetice_CA.index + 1
        df_tabele_calcule_energetice_CA['Nr_Crt'] = df_tabele_calcule_energetice_CA.index

        #print(df_tabele_calcule_energetice_CA)

        # creare dictionar pentru a scrie tabelul de calcul consum curent CA in fisierul template word
        df_tabele_calcule_energetice_CA = df_tabele_calcule_energetice_CA.astype(str)
        # df_tabele_calcule_energetice_CA.rename(columns={'Nr_Crt' : 'CA_consum_nr_crt'+str(i),
        #                                                 'Denumire_element' : 'CA_consum_denumire_element'+str(i),
        #                                                 'COD_ECHIPAMENT' : 'CA_consum_cod_echipament'+str(i),
        #                                                 'CANTITATE' : 'CA_consum_cantitate'+str(i),
        #                                                 'CONSUM_VEGHE' : 'CA_consum_veghe'+str(i),
        #                                                 'CONSUM_ALARMA' : 'CA_consum_alarma'+str(i),
        #                                                 'CONSUM_TOTAL_VEGHE' : 'CA_consum_total_veghe'+str(i),
        #                                                 'CONSUM_TOTAL_ALARMA' : 'CA_consum_total_alarma'+str(i)},
        #                                        inplace=True)
        # dict_df_tabele_calcule_energetice_CA = df_tabele_calcule_energetice_CA.to_dict('records')
        # #print(dict_df_tabele_calcule_energetice_CA)
        # lista_tabele_consum_energetic_CA.append(dict_df_tabele_calcule_energetice_CA)

        #################################################################################################
        # creare variabile ce se vor scrie sub tabelele de calcul consum curent CA
        # creare variabila ce contine denumirea filtrelor de control acces sub tabelele de consum curent CA
        sursa_alim = lista_surse_alimentare_CA[i]
        filtru_control_acces = list(df_tabele_calcule_energetice_CA['APARTENENTA_FCA'])
        # pentru ca pot fi mai multe filtre de control acces alocate la aceeasi sursa de alimentare,pt afisare vreau sa
        # elimin duplicates din lista df_tabele_calcule_energetice_CA['APARTENENTA_FCA'] si sa le salvez intr-o
        # variabila sub forma FCA1, FCA2, FCA3
        #print(filtru_control_acces)
        lista_denumiri_FCA = []
        for FCA in filtru_control_acces:
            if FCA not in lista_denumiri_FCA:
                lista_denumiri_FCA.append(FCA)
            lista_denumiri_FCA.sort()
        #print(lista_denumiri_FCA)
        denumire_FCA ='filtrelor de control acces ' + ', ' .join(lista_denumiri_FCA) \
            if len(lista_denumiri_FCA) > 1 else 'filtrului de control acces ' + ', ' .join(lista_denumiri_FCA)
        #print(denumire_FCA )
        # capacitate_acc_SA_CA = input(f'Introdu valoarea capacitatii acumulatorului utilizat la sursele de CA')
        # ### de creat un dictionar pt acumulatorul utilizat astfel incat sa il adaug in lista de cantitati de la CA
        consum_total_veghe_CA_Amperi = consum_total_veghe_CA_mA/1000
        consum_total_alarma_CA_Amperi = consum_total_alarma_CA_mA/1000

        # aici se convertesc rezultatele din float in ore si minute pentru capacitate acc\consum_veghe si consum_alarma
        timp_veghe = capacitate_acc_SA_CA / consum_total_veghe_CA_Amperi
        ore_veghe,minute_veghe = divmod(timp_veghe,1)
        minute_veghe = minute_veghe * 60
        if minute_veghe == 0:
            rezultat_timp_veghe = 'în stare de veghe: {}Ah / {}A = {}ore'.format(str(capacitate_acc_SA_CA),
                                                                                 str(consum_total_veghe_CA_Amperi),
                                                                                 int(ore_veghe))
        else:
            rezultat_timp_veghe = 'în stare de veghe: {}Ah / {}A = {}ore şi {}minute'.format(str(capacitate_acc_SA_CA),
                                                                        str(consum_total_veghe_CA_Amperi),
                                                                        int(ore_veghe),
                                                                        int(minute_veghe))
        print(rezultat_timp_veghe)

        if consum_total_alarma_CA_Amperi != 0:
            timp_alarma = capacitate_acc_SA_CA / consum_total_alarma_CA_Amperi
            ore_alarma, minute_alarma = divmod(timp_alarma, 1)
            minute_alarma = minute_alarma * 60
            if minute_alarma == 0:
                rezultat_timp_alarma = 'în stare de alarmă: {}Ah / {}A = {}ore'.format(str(capacitate_acc_SA_CA),
                                                                                     str(consum_total_alarma_CA_Amperi),
                                                                                     int(ore_alarma))
            else:
                rezultat_timp_alarma = 'în stare de alarmă: {}Ah / {}A = {}ore şi {}minute'.format(str(capacitate_acc_SA_CA),
                                                                            str(consum_total_alarma_CA_Amperi),
                                                                            int(ore_alarma),
                                                                            int(minute_alarma))


        elif consum_total_alarma_CA_Amperi == 0:
            rezultat_timp_alarma = f'în stare de alarmă: nu există consum pe sursa de alimentare {sursa_alim}'

        print(rezultat_timp_alarma)
        #timp_veghe = f'{timp_veghe:.2f}'
        #timp_alarma = f'{timp_alarma:.2f}'

        dict_val_tabel_consum_CA = {}
        dict_val_tabel_consum_CA.update({'CA_consum_SA' + str(i) : sursa_alim,
                                         'CA_consum_FCA' + str(i) : denumire_FCA,
                                         'CA_consum_TOTAL_veghe_mA' + str(i) : str(consum_total_veghe_CA_mA),
                                         'CA_consum_TOTAL_alarma_mA' + str(i) : str(consum_total_alarma_CA_mA),
                                         'CA_acc_SA' + str(i) : str(capacitate_acc_SA_CA),
                                         'CA_consum_TOTAL_veghe_A' + str(i) : str(consum_total_veghe_CA_Amperi),
                                         'CA_consum_TOTAL_alarma_A' + str(i) : str(consum_total_alarma_CA_Amperi),
                                         'CA_timp_veghe_' + str(i) : str(rezultat_timp_veghe),
                                         'CA_timp_alarma_' + str(i) : str(rezultat_timp_alarma)})

        lista_valori_calcule_sub_tabele_consum_energetic_CA.append(dict_val_tabel_consum_CA)

        # print(sursa_alim,
        #       filtru_control_acces,
        #       capacitate_acc_SA_CA,
        #       consum_total_veghe_CA_Amperi,
        #       consum_total_alarma_CA_Amperi,
        #       consum_total_veghe_CA_mA,
        #       consum_total_alarma_CA_mA,
        #       rezultat_timp_veghe, rezultat_timp_alarma)
    #print(lista_valori_calcule_sub_tabele_consum_energetic_CA)
    #print(lista_tabele_consum_energetic_CA)
    return lista_valori_calcule_sub_tabele_consum_energetic_CA

def CA_tabel_zone_supravegheate():
    df_tabel_zone_supravegheate = pd.DataFrame(df_CA_dwg[['APARTENENTA_FCA','ZONA_SUPRAVEGHEATA', 'SIMBOL_ECHIPAMENT']])
    filt_FCA_zone_supravegheate = (df_tabel_zone_supravegheate['APARTENENTA_FCA'] ==
                                   df_tabel_zone_supravegheate['SIMBOL_ECHIPAMENT'])
    #df_tabel_zone_supravegheate = df_tabel_zone_supravegheate[df_tabel_zone_supravegheate['ZONA_SUPRAVEGHEATA'].notnull()]
    df_tabel_FCA = pd.DataFrame(df_tabel_zone_supravegheate.loc[filt_FCA_zone_supravegheate, ['SIMBOL_ECHIPAMENT',
                                                                                              'ZONA_SUPRAVEGHEATA']])
    df_tabel_FCA = df_tabel_FCA.sort_values(by='SIMBOL_ECHIPAMENT', ignore_index=True)
    df_tabel_FCA['Denumire_zona_CA'] = 'Uşă acces ' + (df_tabel_FCA['ZONA_SUPRAVEGHEATA']).str.lower()
    #df_tabel_FCA['Denumire_zona_CA'] = 'Uşă acces ' + (df_tabel_FCA['ZONA_SUPRAVEGHEATA']).str.lower()
    #df_tabel_FCA['Denumire_zona_CA'] = df_tabel_FCA['Denumire_zona_CA'].apply(lambda x: ', '.join(set([y.strip() for y in x.split(' ')])))
    print(df_tabel_FCA['Denumire_zona_CA'])

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

def creare_df_acc_SA_CA(lista_dict_acc_surse_alimentare_CA):
    # pentru a putea crea dataframe, avem nevoie ca lista_dict_acc_surse_alimentare_CA sa fie o lista de dictionare,
    # nu o lista cu liste de dictionare
    # pentru a avea ca rezultat o lista de dictionare dintr-o lista de liste de dictionare, folosim nested for mai jos
    flatten_matrix = []
    for sublist in lista_dict_acc_surse_alimentare_CA:
        for val in sublist:
            flatten_matrix.append(val)

    #cream data frame-ul cu acumulatoarele
    df_SA_CA = pd.DataFrame(flatten_matrix)

    return(df_SA_CA)

def CA_lista_cantitati(df_acc_SA_CA):
    #dataframe df_SA_CA se va adauga in functia de calcul a listei de cantitati echipamente TVCI
    df_CA_lista_cantitati = pd.DataFrame(df_CA_dwg_merged_with_db[['Nr_Crt',
                                                                   'Denumire_element',
                                                                   'COD_ECHIPAMENT',
                                                                   'CANTITATE',
                                                                   'Producator',
                                                                   'Furnizor',
                                                                   'Document insotior']])

    df_CA_lista_cantitati = df_CA_lista_cantitati.append(df_acc_SA_CA)

    print(df_CA_lista_cantitati)

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
    return dict_df_CA_tabel_cantitati

def caracteristici_tehnice_CA(dict_df_CA_tabel_cantitati):
    #dict_df_CA_tabel_cantitati este o lista de dictionare si o convertesc intr-un dataframe
    df_lista_cantitati_CA = pd.DataFrame(dict_df_CA_tabel_cantitati)

    # din dataframe introduc intr-o lista coloana cu codurile de echipamente
    lista_coduri_echipamente_CA= list(df_lista_cantitati_CA['CA_cantitati_tip_element'])

    dict_caract_tehnice_CA = {}
    lista_dict_caract_tehnice_CA = []

    # verific fiecare cod de echipament in baza de date si pentru fiecare cod extrag de pe coloana caracteristici
    # tehnice din baza de date informatiile despre echipamentul respectiv, informatii ce vor fi stocate intr-o
    # lista de dictionare ce vor fi returnate pt a fi utilizate in CA_functii
    for i in range(len(lista_coduri_echipamente_CA)):
        filt = df_db_CA["COD_ECHIPAMENT"] == lista_coduri_echipamente_CA[i]
        df_get_caract_tehnice = pd.DataFrame(df_db_CA.loc[filt, ['COD_ECHIPAMENT', 'Caracteristici tehnice']])
        caracteristici_tehnice = df_get_caract_tehnice['Caracteristici tehnice'].iloc[0]
        dict_caract_tehnice_CA.update({'var_CA' + str(i): caracteristici_tehnice})
        lista_dict_caract_tehnice_CA.append(dict_caract_tehnice_CA)
    #print(lista_dict_caract_tehnice_CA)

    return lista_dict_caract_tehnice_CA

"""
Pentru creare jurnal cabluri CA trebuie sa identificam echipamentele ce se vor conecta la modulul de control acces
sau la cititor(in cazul in care este stand alone).
"""
""" Creez dataframe cu echipamentele care vor fi introduse in jurnalul de cabluri"""
def creare_df_echip_jurnal_cabluri_CA():
    df_echip_pt_jurnal_cabluri_CA = \
        df_CA_dwg_merged_with_db[['Nr_Crt',
                                  'Denumire_element',
                                  'SIMBOL_ECHIPAMENT',
                                  'CONECTARE_LA',
                                  'APARTENENTA_FCA',
                                  'SURSA_ALIMENTARE',
                                  'Tip cablu']].drop(df_CA_dwg_merged_with_db
        [df_CA_dwg_merged_with_db['SIMBOL_ECHIPAMENT'].str.contains('FCA')].index.tolist())

    df_echip_pt_jurnal_cabluri_CA.sort_values(['Nr_Crt',
                                               'APARTENENTA_FCA',
                                               'CONECTARE_LA',
                                               'SIMBOL_ECHIPAMENT',
                                               'SURSA_ALIMENTARE',
                                               'Denumire_element',
                                               'Tip cablu'], inplace=True)


    #print(df_echip_pt_jurnal_cabluri_CA)
    return df_echip_pt_jurnal_cabluri_CA


def identificare_FCA(df_echip_pt_jurnal_cabluri_CA):
    """Identificam care sunt filtrele de control acces pe care le avem in componenta sistemului, dupa care
    le sortam in ordine crescatoare"""
    lista_filtre_CA = list(df_echip_pt_jurnal_cabluri_CA['APARTENENTA_FCA'].dropna())
    lista_FCA = []
    for item in lista_filtre_CA:
        if item not in lista_FCA:
            lista_FCA.append(item)
    lista_FCA.sort()
    #print(lista_FCA)
    return lista_FCA

def dict_elemente_de_la_pana_la_CA(df_echip_pt_jurnal_cabluri_CA, lista_FCA):
    """Grupam echipamentele in functie de filtrele de control acces de care apartin"""
    #def creare_df_pt_fiecare_FCA(df_echip_pt_jurnal_cabluri_CA, lista_FCA):
    #df_FCA = df_echip_pt_jurnal_cabluri_CA.groupby(by = 'APARTENENTA_FCA', dropna = True)
    df_FCA = df_echip_pt_jurnal_cabluri_CA.groupby('APARTENENTA_FCA')

    """am creat un nou dictionar dict_de_la_pana_la_CA in care vom stoca si ordona toate elementele ce se vor scrie 
    in jurnalul de cabluri"""
    dict_de_la_pana_la_CA = {}
    lista_emg_BU = []

    for FCA in lista_FCA:
        """selectez din df_FCA doar elementele care apartin FCA1, FCA2, etc """
        df_FCA.get_group(FCA)
        """creez un dictionar cu simbolurile de echipamente ca si chei si denumirile de echip ca valori """
        dict_elemente_FCA = dict(zip(df_FCA.get_group(FCA)['SIMBOL_ECHIPAMENT'],
                                     df_FCA.get_group(FCA)['Denumire_element']))

        """De aici preiau dictionarul ce contine echipamentele ce apartin fiecarui filtru de control acces"""
        print(dict_elemente_FCA)

        def get_key(val):
            for key, value in dict_elemente_FCA.items():
                if val == value:
                    return key
            return print("key doesn't exist")

        """Aici sunt elementele in baza carora se face cautarea echipamentelor ce apartin fiecarui filtru de CA"""
        lista_cuvinte_tinta_echipamente_FCA = ['aliment',
                                               'odul',
                                               'ititor',
                                               'erere',
                                               'ontact',
                                               'elector',
                                               'lectromagnet',
                                               'urgen',
                                               'ala']
        # #dictionarul dict ar trebui updatat cu valorile din dataframe-ul df_FCA.get_group('FCA1') grupat in functie de FCA
        # dict_elemente_FCA = {'SC1':'Sursă de alimentare 12V 5.4A',
        #                      'R1.1':'Cititor de proximitate',
        #                      'R1.2':'Cititor de proximitate',
        #                      'BI1':'Buton cerere ieșire',
        #                      'BU1':'Buton de ieșire urgență',
        #                      'E1':'Electromagnet blocare uși control acces',
        #                      'E2':'Electromagnet blocare uși control acces'}

        """Pentru ca in valorile dictionarului dict_elemente_FCA apar valori care se repeta(denumirea 
        electromagnetilor, sau denumirea cititoarelor - atunci cand avem mai multe pe acelasi FCA), am utilizat 
        functiile de mai jos pentru
        - gasire valori dublate in dictionarul dict_elemente_FCA;
        - adaugarea unui caracter la fiecare valoare dublata astfel incat sa o fac unica in dictionar
        - updatarea dictionarului cu noile valori"""
        # finding duplicate values
        # from dictionary using set
        rev_dict = {}
        for key, value in dict_elemente_FCA.items():
            rev_dict.setdefault(value, set()).add(key)

        #result = filter(lambda x: len(x)>1, rev_dict.values())
        result = set(chain.from_iterable(
                 values for key, values in rev_dict.items()
                 if len(values) > 1))
        lista_elemente_dublate = list(result)

        #adaugarea unui caracter la fiecare valoare dublata astfel incat sa o fac unica in dictionar si sa se
        # poata face potrivirea cuvantului cheie cu toate valorile din dictionar. Daca nu faceam acest arificiu, atunci
        # cand aveam 2 cititoare, tot timpul potrivirea se oprea la prima valoare a primului cititor
        for i in range(len(lista_elemente_dublate)):
            for key, value in dict_elemente_FCA.items():
                if lista_elemente_dublate[i] == key:
                    dict_elemente_FCA.update({key : value + str(i)})
                    #print(lista_elemente_dublate[i])
                else:
                    pass

        """Trebuie avut in vedere ca aici dict_elemente_FCA va avea noi valori fata de cele initiale, asadar, 
        de aici vom extrage lista ce contine valorile dictionarului dict_elemente_FCA.
        In aceste valori vom cauta cuvintele cheie, astfel incat sa aflam elementele(cititoare, emg, bu, etc) pe care
        le vom ordona in jurnalul de cabluri"""
        #print(dict_elemente_FCA)
        #cream o lista cu toate denumirile elementelor componente pentru un filtru de CA dupa care
        lista_denumiri_echipamente_in_FCA = dict_elemente_FCA.values()
        #print(lista_denumiri_echipamente_in_FCA)

        for valoare in lista_denumiri_echipamente_in_FCA:
            #for i in range(len(lista_cuvinte_tinta_echipamente_FCA)):
            if lista_cuvinte_tinta_echipamente_FCA[0] in valoare:
                cheie = get_key(valoare)
                #print(cheie)
                val_conectare_la = df_echip_pt_jurnal_cabluri_CA.loc[
                    df_echip_pt_jurnal_cabluri_CA['SIMBOL_ECHIPAMENT'] == cheie, 'CONECTARE_LA'].iloc[0]
                dict_de_la_pana_la_CA.update({cheie : val_conectare_la})
            elif lista_cuvinte_tinta_echipamente_FCA[1] in valoare:
                cheie = get_key(valoare)
                #print(cheie)
                val_conectare_la = df_echip_pt_jurnal_cabluri_CA.loc[
                    df_echip_pt_jurnal_cabluri_CA['SIMBOL_ECHIPAMENT'] == cheie, 'SURSA_ALIMENTARE'].iloc[0]
                dict_de_la_pana_la_CA.update({cheie : val_conectare_la})
            elif lista_cuvinte_tinta_echipamente_FCA[2] in valoare:
                cheie = get_key(valoare)
                #print(cheie)
                val_conectare_la = df_echip_pt_jurnal_cabluri_CA.loc[
                    df_echip_pt_jurnal_cabluri_CA['SIMBOL_ECHIPAMENT'] == cheie, 'CONECTARE_LA'].iloc[0]
                dict_de_la_pana_la_CA.update({cheie : val_conectare_la})
            elif lista_cuvinte_tinta_echipamente_FCA[3] in valoare:
                cheie = get_key(valoare)
                # print(cheie)
                val_conectare_la = df_echip_pt_jurnal_cabluri_CA.loc[
                    df_echip_pt_jurnal_cabluri_CA['SIMBOL_ECHIPAMENT'] == cheie, 'CONECTARE_LA'].iloc[0]
                dict_de_la_pana_la_CA.update({cheie: val_conectare_la})
            elif lista_cuvinte_tinta_echipamente_FCA[4] in valoare:
                cheie = get_key(valoare)
                # print(cheie)
                val_conectare_la = df_echip_pt_jurnal_cabluri_CA.loc[
                    df_echip_pt_jurnal_cabluri_CA['SIMBOL_ECHIPAMENT'] == cheie, 'CONECTARE_LA'].iloc[0]
                dict_de_la_pana_la_CA.update({cheie: val_conectare_la})
            elif lista_cuvinte_tinta_echipamente_FCA[5] in valoare:
                cheie = get_key(valoare)
                # print(cheie)
                val_conectare_la = df_echip_pt_jurnal_cabluri_CA.loc[
                    df_echip_pt_jurnal_cabluri_CA['SIMBOL_ECHIPAMENT'] == cheie, 'CONECTARE_LA'].iloc[0]
                dict_de_la_pana_la_CA.update({cheie: val_conectare_la})
            elif lista_cuvinte_tinta_echipamente_FCA[6] in valoare:
                cheie = get_key(valoare)
                if cheie not in lista_emg_BU:
                    lista_emg_BU.append(cheie)
                    #print(lista_emg_BU)
            elif lista_cuvinte_tinta_echipamente_FCA[7] in valoare:
                cheie = get_key(valoare)
                cheie_concat = (cheie + '-') + df_echip_pt_jurnal_cabluri_CA.loc[
                    df_echip_pt_jurnal_cabluri_CA['SIMBOL_ECHIPAMENT'] == cheie, 'CONECTARE_LA'].iloc[0]
                print(cheie_concat)
                """cheie_concat este variabila ce stocheaza MCU-BU pt a putea crea in jurnalul de cabluri 
                             E-BU-MCU la SA"""
                if cheie_concat not in lista_emg_BU:
                    lista_emg_BU.append(cheie_concat)
                    print(lista_emg_BU)
                val_conectare_la = df_echip_pt_jurnal_cabluri_CA.loc[
                    df_echip_pt_jurnal_cabluri_CA['SIMBOL_ECHIPAMENT'] == cheie, 'SURSA_ALIMENTARE'].iloc[0]
        print(val_conectare_la)
        #print(lista_emg_BU)
        caracter_de_separare = '-'
        lista_emg_BU_cu_caract_separare = caracter_de_separare.join(lista_emg_BU[::-1])
        cheie = lista_emg_BU_cu_caract_separare
        #print(val_conectare_la)
        dict_de_la_pana_la_CA.update({cheie: val_conectare_la})
        lista_emg_BU.clear()

    print(dict_de_la_pana_la_CA)
    #print(lista_emg_BU)
    return dict_de_la_pana_la_CA

def serie_de_la_jurnal_cabluri_CA(dict_de_la_pana_la_CA):
    simboluri_echip_jurnal_cabl_CA = dict_de_la_pana_la_CA.keys()
    serie_de_la = pd.Series(simboluri_echip_jurnal_cabl_CA)
    return serie_de_la

def serie_pana_la_jurnal_cabluri_CA(dict_de_la_pana_la_CA):
    valori_pana_la_jurnal_cabl_CA = dict_de_la_pana_la_CA.values()
    serie_pana_la = pd.Series(valori_pana_la_jurnal_cabl_CA)
    #print(serie_pana_la)
    return serie_pana_la


"""pentru simbolurile de tip E1.1-E1.2-BU1-MCU1, trebuie sa scot primul simbol din string astfel incat sa
pot adauga cabul in seria tip cablu"""
def scoate_primul_simbol_din_echip_inseriate(dict_de_la_pana_la_CA):
    simboluri_echip_jurnal_cabl_CA = dict_de_la_pana_la_CA.keys()
    target_letter = '-'
    lst_simboluri_echip_jurnal_cabl_CA = []
    for simbol in simboluri_echip_jurnal_cabl_CA:
        if target_letter in simbol:
            new_simbol = simbol
            index_position = new_simbol.index(target_letter)
            index_position = int(index_position)
            str_target = simbol[:index_position]
            lst_simboluri_echip_jurnal_cabl_CA.append(str_target)
        else:
            lst_simboluri_echip_jurnal_cabl_CA.append(simbol)
    return lst_simboluri_echip_jurnal_cabl_CA

def serie_tip_cabluri_jurnal_CA(df_echip_pt_jurnal_cabluri_CA, lst_simboluri_echip_jurnal_cabl_CA):
    lista_tipuri_cabluri = []
    for simbol in lst_simboluri_echip_jurnal_cabl_CA:
        if simbol in list(df_echip_pt_jurnal_cabluri_CA['SIMBOL_ECHIPAMENT']):
            #return print(df_echip_pt_jurnal_cabluri_CA.loc[simbol, ['Tip cablu']][0])
            tip_cablu = (df_echip_pt_jurnal_cabluri_CA.loc[
                df_echip_pt_jurnal_cabluri_CA['SIMBOL_ECHIPAMENT'] == simbol, 'Tip cablu'].iloc[0])
            lista_tipuri_cabluri.append(tip_cablu)
        else:
            val_de_afisat =  f" Simbolul {simbol } nu se regaseste in {list(df_echip_pt_jurnal_cabluri_CA['SIMBOL_ECHIPAMENT'])}"
            print(val_de_afisat)
    serie_tip_cabluri = pd.Series(lista_tipuri_cabluri)
    return serie_tip_cabluri

def df_jurnal_cabluri(serie_de_la, serie_pana_la, serie_tip_cabluri):
    # se creeaza dataframe-ul final cu toate seriile de mai sus care va reprezenta jurnalul de cabluri pt CA
    df_jurnal_cabluri_CA = pd.DataFrame({'De la': serie_de_la.values,
                                         'Pana la': serie_pana_la.values,
                                         'Tip cablu': serie_tip_cabluri.values})

    # resetez index-ul si salvam
    df_jurnal_cabluri_CA.reset_index(drop=True, inplace=True)
    # numerotam index-ul incepand de la 1
    df_jurnal_cabluri_CA.index = df_jurnal_cabluri_CA.index + 1
    df_jurnal_cabluri_CA['Nr crt'] = df_jurnal_cabluri_CA.index
    lista_cod_cablu_CA = []
    for i in range(len(df_jurnal_cabluri_CA['Nr crt'])):
        lista_cod_cablu_CA.append('C'+ str(i+1))
    df_jurnal_cabluri_CA['Cod cablu'] = lista_cod_cablu_CA
    #print(df_jurnal_cabluri_camere)
    df_jurnal_cabluri_CA = df_jurnal_cabluri_CA.astype(str)

    #print(df_jurnal_cabluri_CA)
    return df_jurnal_cabluri_CA

def creare_dict_jurnal_cabluri_CA(df_jurnal_cabluri_CA):
    df_jurnal_cabluri_CA.rename(columns={'Nr crt': 'CA_jurnal_nr_crt',
                                         'Cod cablu': 'CA_jurnal_cod_cablu',
                                         'De la': 'CA_jurnal_de_la',
                                         'Pana la': 'CA_jurnal_pana_la',
                                         'Tip cablu': 'CA_jurnal_tip_cablu'}, inplace=True)
    dict_jurnal_cabluri_CA = df_jurnal_cabluri_CA.to_dict('records')
    #print(dict_jurnal_cabluri_CA)
    return dict_jurnal_cabluri_CA























