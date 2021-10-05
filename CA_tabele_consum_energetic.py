import pandas as pd
import sys


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
verificare_simboluri_echipamente()

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
verificare_elemente_ce_nu_au_sursa_atribuita()

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
verificare_elemente_fara_simbol_atribuit()



# pentru calculul consumurilor pe sursele de alimentare este nevoie sa extrag denumirile tuturor surselor de
# alimentare din sistem
# aceste denumiri de surse sunt introduse in lista list_pwr_supply_labels si utilizate ulterior pentru calcule
read_pwr_supply_labels = df_SA_CA['SURSA_ALIMENTARE'].astype(str)
list_pwr_supply_labels = []
for item in read_pwr_supply_labels:
    if item not in list_pwr_supply_labels:
        list_pwr_supply_labels.append(item)
        list_pwr_supply_labels.sort()
#list_pwr_supply_labels

capacitate_acc_SA_CA = int(input(f'Introdu valoarea capacitatii acumulatorului utilizat la sursele de CA'))
### de creat un dictionar pt acumulatorul utilizat astfel incat sa il adaug in lista de cantitati de la CA
lista_tabele_consum_energetic_CA = []
lista_valori_calcule_sub_tabele_consum_energetic_CA = []

############
#creare dictionar pentru acumulatoarele surselor de alimentare de la sistemul de CA
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

def tabele_consum_energetic_CA():

    for i in range(len(list_pwr_supply_labels)):
        # creez variablia filtru_SA care selecteaza elementele din df_SA_CA ce au pe coloana "SURSA_ALIMENTARE"
        # denumirea sursei din
        # lista de surse de alimentare si au consumul de veghe sau consumul de alarma > 0
        filtru_SA = ((df_SA_CA['SURSA_ALIMENTARE'] == list_pwr_supply_labels[i]) &
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

        # creez df_tabele_calcule_energetice_CA in care sortez in fct de Nr_Crt din bazade date si fac agregare
        # pe coloana SIMBOL_ECHIPAMENT - atunci cand sunt mai multe elemente de acelasi fel aplic functia lambda si
        # simbolurile de echipamente vor fi concatenate sub forma E1, E2, E3  etc
        # pe coloana cantitate fac suma elementelor de acelasi fel
        df_tabele_calcule_energetice_CA = table_calc_SA.groupby(['Nr_Crt',
                                                                 'COD_ECHIPAMENT',
                                                                 'Denumire_element',
                                                                 'APARTENENTA_FCA',
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

        #################################################################################################
        # creare variabile ce se vor scrie sub tabelele de calcul consum curent CA
        sursa_alim = list_pwr_supply_labels[i]
        filtru_control_acces = df_tabele_calcule_energetice_CA['APARTENENTA_FCA'].iloc[0]
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
                                         'CA_consum_FCA' + str(i) : filtru_control_acces,
                                         'CA_consum_TOTAL_veghe_mA' + str(i) : str(consum_total_veghe_CA_mA),
                                         'CA_consum_TOTAL_alarma_mA' + str(i) : str(consum_total_alarma_CA_mA),
                                         'CA_acc_SA' + str(i) : str(capacitate_acc_SA_CA),
                                         'CA_consum_TOTAL_veghe_A' + str(i) : str(consum_total_veghe_CA_Amperi),
                                         'CA_consum_TOTAL_alarma_A' + str(i) : str(consum_total_alarma_CA_Amperi),
                                         'CA_timp_veghe_' + str(i) : str(rezultat_timp_veghe),
                                         'CA_timp_alarma_' + str(i) : str(rezultat_timp_alarma)})

        lista_valori_calcule_sub_tabele_consum_energetic_CA.append(dict_val_tabel_consum_CA)

        print(sursa_alim,
              filtru_control_acces,
              capacitate_acc_SA_CA,
              consum_total_veghe_CA_Amperi,
              consum_total_alarma_CA_Amperi,
              consum_total_veghe_CA_mA,
              consum_total_alarma_CA_mA,
              rezultat_timp_veghe, rezultat_timp_alarma)
    #print(lista_valori_calcule_sub_tabele_consum_energetic_CA)
    #print(lista_tabele_consum_energetic_CA)

        # adaugam acumulatorul aferent sursei de alimentare intr-o lista de dictionare ce va fi importata in modulul care
        # creeaza lista de cantitati pentru subsistemul de control acces
        lista_dict_acc_SA_CA.append(copy_dict_acc_SA_CA)

    return lista_tabele_consum_energetic_CA, lista_valori_calcule_sub_tabele_consum_energetic_CA, lista_dict_acc_SA_CA


def valori_tabele_consum_energetic_CA():
    tabele_consum_energetic_CA()
    #lista_echipamente_tabele_consum = list(map(dict, chain.from_iterable(lst)))
    lista_valori_tabele_consum_energetic_CA = lista_tabele_consum_energetic_CA

    #print(lista_tabele_consum_energetic_CA)
    return lista_valori_tabele_consum_energetic_CA

#functia var_surse_alim() aduce lista de dictionare lista_valori_calcule_sub_tabele_consum_energetic_CA,
# o salveaza in variabila lista_valori_calcule_CA si
# o retuneaza pentru a fi utilizata in modulul main pt a scrie valorile in fisierul word.
def valori_calcule_surse_alim_CA():
    #lista_echipamente_tabele_consum = list(map(dict, chain.from_iterable(lst)))
    lista_valori_calcule_CA = lista_valori_calcule_sub_tabele_consum_energetic_CA
    #print(lista_valori_calcule_CA)
    return lista_valori_calcule_CA


def dict_acumulatoare_SA_CA():
    lista_dictionare_SA_CA =  lista_dict_acc_SA_CA
    return lista_dictionare_SA_CA



#functia tabele_consum_energetic_CA() o apelez din functia valori_tabele_consum_energetic_CA() pentru a
# se adauga listele de dictionare(pt tabele si pt calculele de sub tabele) in listele returnate de
# functiile valori_tabele_consum_energetic_CA() si valori_calcule_surse_alim_CA()
if __name__ == '__main__':
    #tabele_consum_energetic_CA()
    valori_tabele_consum_energetic_CA()
    valori_calcule_surse_alim_CA()
    dict_acumulatoare_SA_CA()

