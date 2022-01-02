import pandas as pd
import sys
import xlrd
from math import ceil
from itertools import chain

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)

try:
    df_db = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_efractie.xlsx')


    df_intrussion_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\zonare.txt',
                                    delimiter="\t")
    df_read_zonare = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\zonare.txt',
                                 delimiter="\t")
except FileNotFoundError as exception_label:
    print(f' Fisierul {exception_label} nu se afla in folderul radacina')
    sys.exit(3)
# creez data frame df.pwr_supply din df_intrussion_dwg (din tabelul exportat din Autocad), in care afisez coloanele "SURSA_ALIMENTARE", "CONSUM_VEGHE", "CONSUM_ALARMA" , le grupez dupa coloana "SURSA_ALIMENTARE" si le adun .sum()
#df_pwr_supply = df_intrussion_dwg[["INDEX", "CONSUM_VEGHE", "CONSUM_ALARMA"]].groupby(["INDEX"]).sum()
df_pwr_supply = pd.merge(df_intrussion_dwg, df_db, on='COD_ECHIPAMENT')[
    ["INDEX", "CONSUM_VEGHE_y", "CONSUM_ALARMA_y"]].groupby(["INDEX"]).sum()
#print(df_pwr_supply.columns)
# creez un nou data frame df_pwr_supply_calculation derivat din df_pwr_supply
df_pwr_supply_calculation = pd.DataFrame(df_pwr_supply)
# redenumesc coloanele astfel incat acest df sa il adaug la dataframe-ul cu lista de ecehipamente/consum pt fiecare sursa din sistem
df_pwr_supply_calculation.rename(columns={"CONSUM_VEGHE": "TOTAL CONSUM VEGHE", "CONSUM_ALARMA": "TOTAL CONSUM ALARMA"},
                                 inplace=True)

# in lista lst adaugam listele de dictionare ce sunt returnate de functia creare_tabele_calcul_consum(i, battery, nr_of_battery)
lst = []
lst_var_SA =[]

#creez o lista goala in care stochez codurile echipamentelor utilizate in modulul efractie
#aceste coduri vor fi utilizate in modulul antiefractie_TVCI_caract_tehnice pt a scrie caract tehnice in fisierul word
lst_coduri_echip_pt_fise_tehnice = []


# pentru calculul consumurilor pe sursele de alimentare este nevoie sa extrag denumirile tuturor surselor de alimentare din sistem
# aceste denumiri de surse sunt introduse in lista list_pwr_supply_labels si utilizate ulterior pentru calcule, denumire sheet-uri fisier exportat
read_pwr_supply_labels = df_intrussion_dwg["INDEX"]
list_pwr_supply_labels = []
for item in read_pwr_supply_labels:
    #print(item)
    if item not in list_pwr_supply_labels:
        list_pwr_supply_labels.append(item)
        list_pwr_supply_labels.sort()
list_pwr_supply_labels


def verificare_simboluri_echipamente():
    lista_simboluri_echipamente_efr = list(df_intrussion_dwg['SIMBOL_ECHIPAMENT'])
    #print(lista_simboluri_echipamente_efr)
    lista_simboluri_verificate = []
    lista_simboluri_dublate = []
    for item in lista_simboluri_echipamente_efr:
        if item not in lista_simboluri_verificate:
            lista_simboluri_verificate.append(item)
        else:
            lista_simboluri_dublate.append(item)
    if len(lista_simboluri_dublate) > 1:
        print(f'Verificati numerotarea echipamentelor! Urmatoarele simboluri {lista_simboluri_dublate} apar de mai multe ori in fisierul autocad.')
        sys.exit(3)
    else:
        if len(lista_simboluri_dublate) == 1:
            print(f'Verificati numerotarea echipamentelor! Simbolul {lista_simboluri_dublate[0]} apare de mai multe ori in fisierul autocad.')
            sys.exit(3)
    #continue
verificare_simboluri_echipamente()


# def verific_echip_inainte_de_calcule_consum():
#     """Avand in vedere faptul ca lista cu echipamentele pe care le exportam din dwg poate sa aiba valori
#     gresite sau sa nu aiba valori completate
#     pe anumite coloane(in special 'COD_ECHIPAMENT','CONSUM_VEGHE', 'CONSUM_ALARMA' - in baza carora facem calcule)
#     am creat functia verific_echip_inainte_de_calcule_consum() astfel incat sa verific fiecare linie din fisierul
#     exportat din dwg cu
#     elementele existente in baza de date
#     verificarea se face pt fiecare valoare de pe coloanele 'COD_ECHIPAMENT','CONSUM_VEGHE', 'CONSUM_ALARMA'
#     in momentul in care elementele exportate din dwg au diferente fata de baza de date, aceste elemente sunt
#     afisate si vor trebui modificate manual, astfel incat sa nu fie diferente"""
#     # df_db = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_efractie.xlsx')
#     # df_intrussion_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\zonare.csv')
#     # df_intrussion_dwg.head()
#
#     # citesc fisierul exportat din dwg si il afisez in functie de coloanele'COD_ECHIPAMENT','CONSUM_VEGHE', 'CONSUM_ALARMA'
#     df_equipments_from_dwg = df_intrussion_dwg[['COD_ECHIPAMENT', 'CONSUM_VEGHE', 'CONSUM_ALARMA']]
#     df_equipments_from_dwg
#     # creez o lista cu valorile de pe coloana 'COD_ECHIPAMENT' din fisierul exportat din dwg
#     list_equip_codes_from_dwg = list(df_equipments_from_dwg['COD_ECHIPAMENT'])
#     # creez data frame df_from_db din df_db cu colanele 'COD_ECHIPAMENT','CONSUM_VEGHE','CONSUM_ALARMA'
#     df_from_db = pd.DataFrame(
#         df_db[['COD_ECHIPAMENT', 'CONSUM_VEGHE', 'CONSUM_ALARMA']].sort_values(by=['COD_ECHIPAMENT'], ascending=True))
#     # creez o lista cu valorile de pe coloana 'COD_ECHIPAMENT' din baza de date
#     list_equip_codes_from_db = list(df_from_db['COD_ECHIPAMENT'])
#     # list_equip_codes_from_db
#     # creez o lista goala in care voi introduce valorile de pe coloana 'COD_ECHIPAMENT' din df_from_db pe care nu vreau sa le afisez in data frame-ul final
#     list_equip_codes_need_dropped = []
#     # itezez lista list_equip_codes_from_db si introduc in lista list_equip_codes_need_dropped valorile pe care nu vreau sa le afisez in data frame-ul final
#     for item in list_equip_codes_from_db:
#         if item not in list_equip_codes_from_dwg:
#             list_equip_codes_need_dropped.append(item)
#
#     # print(list_equip_codes_need_dropped)
#     # sterg liniile din df_from_db ale caror coduri de echipament nu sunt aceleasi cu codurile de echipament din df df_equipments_from_dwg(codurile de echipamente exportate din dwg)
#     df_from_db = df_from_db.drop(
#         df_from_db[df_from_db.COD_ECHIPAMENT.isin(list_equip_codes_need_dropped)].index.tolist())
#     # df_from_db
#     # df_equipments_from_dwg
#
#     # facem verificarea daca fiecare linie(toate valorile unei linii) din df df_equipments_from_dwg se regasesc in df_from_db
#     # https://stackoverflow.com/questions/40514187/check-if-multiple-rows-exist-in-another-dataframe
#     checked_df = pd.merge(df_equipments_from_dwg, df_from_db, indicator=True, how='outer')
#     # print(checked_df)
#     # pentru a afisa dataframe-ul din care elementele ce vor fi afisate fac parte, redenumim valorile de pe noua coloana '_merge'
#     # ce se creeaza odata cu verificarea facuta prin merge(vezi linia de mai sus)
#     checked_df = checked_df.replace({'_merge': {'left_only': 'fisier din DWG', 'right_only': 'baza de date'}})
#     # vreau sa afisez o lista cu elementele ce nu se potrivesc intre df exportat din dwg si baza de date
#     # pt asta introduc valorile de pe coloana '_merge' intr-o lista pe care o iterez
#     # daca am alte valori in afara de "both" le afisez dupa care intrerup executia script-ului
#     list_merged_df = list(checked_df['_merge'])
#     list_merged_values = []
#     for item in list_merged_df:
#         if item == 'both':
#             continue
#         else:
#             list_merged_values.append(item)
#             # print(list_merged_values)
#             # filt = (checked_df != 'both')
#             checked_df = checked_df.loc[checked_df._merge.isin(list_merged_values)]
#             print(checked_df)
#             print(''' \n \n Echipamentul/Echipamentele din lista de mai sus au diferente fata de baza de date.
# In cazul in care pe coloana cod echipament codurile sunt corecte, verifica valorile din coloana cod echipament
# in baza de date!!! ''')
#             sys.exit(2)
#
#
# verific_echip_inainte_de_calcule_consum()


def check_items():
    """Verificam daca codurile de echipamente citite din dwg se regasesc in baza de date. Daca nu se regasesc atunci
    acestea vor trebui introduse in baza de date"""

    # read equipment codes from df_intrussion_dwg and introducing them into a set in order to have a unique
    # equipment code in variable read_check_list
    read_check_list = set(list(df_intrussion_dwg["COD_ECHIPAMENT"]))
    #print(read_check_list)
    """read all equipment codes from intrussion database(df_db_CA) and store them in read_check_list_db list
    in order to verify if all equipment codes from read_check_list are in intrussion database or not.
    If they are not in intrussion database function verific_echip_inainte_de_calcule_consum() will print out
    all codes that are not in intrussion database and ask the user to introduce that equipments in database"""
    read_check_list_db = list(df_db['COD_ECHIPAMENT'])
    #print(read_check_list_db)

    for equipment_code in read_check_list:
        if equipment_code not in read_check_list_db:
            print(f' Codul de produs {equipment_code} nu se afla in baza de date sau a fost scris gresit!'
                  f' Introduceti codul de produs in baza de date!')
            sys.exit(2)
check_items()


# def creare_tabele_calcul_consum(i, battery, nr_of_battery):
#     # din functia calcul_capacitate_acumulatoare() aduc ca argumente i, capacitatile bateriilor si nr_of_battery
#     # creez variablia filt7 care selecteaza elementele din df_intrussion_dwg care au pe coloana "SURSA_ALIMENTARE" denumirea sursei din
#     # lista de surse de alimentare si au consumul de veghe sau consumul de alarma > 0
#     filt7 = ((df_intrussion_dwg["INDEX"] == list_pwr_supply_labels[i]) & (
#             (df_intrussion_dwg["CONSUM_VEGHE"] > 0) | (df_intrussion_dwg["CONSUM_ALARMA"] > 0)))
#     # creez data frame-ul table_calc din data frame df_intrussion_dwg si fac afisare pe coloana(.loc) pt valorile selectate de variablia filt7
#     # si in plus adaug coloanele "COD_ECHIPAMENT","CANTITATE","CONSUM_VEGHE", "CONSUM_ALARMA" la acest dataframe
#     table_calc = pd.DataFrame(
#         df_intrussion_dwg.loc[filt7, ["COD_ECHIPAMENT", "CANTITATE", "CONSUM_VEGHE", "CONSUM_ALARMA"]])
#     # transform valorile din coloana ["CANTITATE"] in valori intregiDENUMIRE_ECHIPAMENT
#     table_calc["CANTITATE"] = table_calc["CANTITATE"].astype('int')
#     # creez un nou dataframe table_calc_int care grupeaza elementele din dataframe-ul table_calc dupa "COD_ECHIPAMENT" si face suma pt "CANTITATE", "CONSUM_VEGHE", "CONSUM_ALARMA"
#     table_calc_int = table_calc.groupby("COD_ECHIPAMENT")[["CANTITATE", "CONSUM_VEGHE", "CONSUM_ALARMA"]].sum()
#     # redenumesc coloanele "CONSUM_VEGHE" : "TOTAL CONSUM VEGHE", "CONSUM_ALARMA" : "TOTAL CONSUM ALARMA" pt ca atunci cand se face merge cu
#     # baza de date denumirile coloanelor sunt aceleasi si nu se pot diferentia
#     table_calc_int.rename(columns={"CONSUM_VEGHE": "TOTAL CONSUM VEGHE", "CONSUM_ALARMA": "TOTAL CONSUM ALARMA"},
#                           inplace=True)
#     # combin elementele din dataframe-ul table_calc_int cu elementele din baza de date df_db in functie de codurile de echipament
#     # se vor afisa doar elementele ale caror coduri de echipament se regasesc in dataframe-ul table_calc_int si in df_db(baza de date)
#     # prin functia check_items() fac verificarea daca un cod de echipament este scris gresit sau nu se afla in vreunul din cele 2 dataframe-uri
#     table_calc_merge_with_db = pd.merge(table_calc_int, df_db, on='COD_ECHIPAMENT')
#     # creez data frame-ul table_calc_final in care afisez informatiile bazat pe coloanele necesare
#     table_calc_final = pd.DataFrame(table_calc_merge_with_db[
#                                         ['Denumire_element', 'COD_ECHIPAMENT', 'TENSIUNE_ALIMENTARE_DE_BAZA',
#                                          'TENSIUNE_ALIMENTARE_DE_REZERVA', 'CONSUM_VEGHE', 'CONSUM_ALARMA',
#                                          'CANTITATE',
#                                          'TOTAL CONSUM VEGHE', 'TOTAL CONSUM ALARMA', 'Nr. Crt']])
#     table_calc_final.sort_values(by=['Nr. Crt'], inplace=True)
#     table_calc_final = table_calc_final[
#         ['Denumire_element', 'COD_ECHIPAMENT', 'TENSIUNE_ALIMENTARE_DE_BAZA', 'TENSIUNE_ALIMENTARE_DE_REZERVA',
#          'CONSUM_VEGHE', 'CONSUM_ALARMA', 'CANTITATE', 'TOTAL CONSUM VEGHE', 'TOTAL CONSUM ALARMA']]
#     table_calc_final.reset_index(drop=True, inplace=True)
#     table_calc_final.index = table_calc_final.index + 1
#     table_calc_final['nr_crt'] = table_calc_final.index
#
#     # # creez o serie pe care o denumesc Total si care este egala cu suma coloanei 'Consum total (W)'
#     # Total = table_calc_final['TOTAL CONSUM VEGHE'].sum()
#     # # setez 'Total' ca index pt linia de Total si pentru toate coloanele vom avea NaN doar pentru coloana 'Consum total (W)' vom avea totalul
#     # table_calc_final.loc['Total'] = pd.Series(table_calc_final['TOTAL CONSUM VEGHE'].sum(),
#     #                                           index=['TOTAL CONSUM VEGHE'])
#     # # pt ca functia sa poata returna un data frame creez acest data frame
#     # table_calc_final = pd.DataFrame(table_calc_final)
#
#     # sortez in functie de coloana 'CONSUM_VEGHE' si 'CONSUM_ALARMA' (consumurile mari sunt afisate primele)
#     # table_calc_final = table_calc_final.sort_values(by=['CONSUM_VEGHE', 'CONSUM_ALARMA'], ascending=False)
#     # table_calc_final
#     """la tabelul cu consumul echipamentelor pt o sursa de alimentare adaug linia
#     cu consumul total pentru curentii de veghe si de alarma.
#     Am facut table_calc_final1 = table_calc_final pt a nu mai schimba denumirea table_calc_final1 mai jos in cod """
#     #table_calc_final1 = pd.DataFrame(table_calc_final.append(df_pwr_supply_calculation.iloc[i]))
#     table_calc_final1 = table_calc_final
#     #print(table_calc_final1)
#     table_calc_final1 = table_calc_final1.fillna(0)
#     #putem aplica applymap cu lambda insa rezultatul este acelasi ca cel dat de linia in care setez int pt nt_crt si cantitate
#     #table_calc_final1 = table_calc_final1.applymap(lambda x: int(round(x, 0)) if isinstance(x, (int, float)) else x)
#     # def check_float_values(x):
#     #     if x > int(x):
#     #         return x
#     #     else:
#     #         return int(x)
#     # table_calc_final1 = table_calc_final1.applymap(lambda x: check_float_values(x) if isinstance(x, (int, float)) else x)
#     table_calc_final1[['nr_crt','CANTITATE']] = table_calc_final1[['nr_crt','CANTITATE']].astype(int)
#
#     # redenumesc coloanele asa cum vreau sa fie afisate in tabelul final
#     table_calc_final1.rename(columns={"Denumire_element": "Denumire element", "COD_ECHIPAMENT": "Cod echipament",
#                                       "TENSIUNE_ALIMENTARE_DE_BAZA": "Tensiune alimentare de baza",
#                                       "TENSIUNE_ALIMENTARE_DE_REZERVA": "Tensiune alimentare de rezerva",
#                                       "CONSUM_VEGHE": "Consum veghe", "CONSUM_ALARMA": "Consum alarma",
#                                       "CANTITATE": "Cantitate", "TOTAL CONSUM VEGHE": "Consum total veghe",
#                                       "TOTAL CONSUM ALARMA": "Consum total alarma"}, inplace=True)
#
#     # scriu dataframe-ul cu tabelul de consum pt o sursa de alimentare in fisierul excel ce va avea sheet-urile denumite cu denumirile surselor de alimentare
#     # table_calc_final1.to_excel(writer, sheet_name=list_pwr_supply_labels[i], index=True)
#     # creez variabilele total_crt_veghe si total_crt_alarma pentru a putea afisa/scrie valorile in fisierul excel
#     total_crt_veghe = table_calc_final['TOTAL CONSUM VEGHE'].sum() / 1000
#     total_crt_alarma = table_calc_final['TOTAL CONSUM ALARMA'].sum() / 1000
#     #print(table_calc_final['TOTAL CONSUM VEGHE'].sum(),table_calc_final['TOTAL CONSUM ALARMA'].sum())
#     # scriu in fisierul excel formula de calcul pentru calculul acumulatorului
#     # folosesc functia ceil(pentru asta am importat modulul math)pt a face rotunjire la 1 chiar daca
#     # valoarea acumulatorului este sub 0.5 de ex 1.15 se va rotunji la 1, 1.55 se va rotunji tot la 1
#     text_power_supply = (
#         f' N= 1,25 x [({total_crt_veghe:.4f} x 24ore) + ({total_crt_alarma:.4f} x 0,5ore)] / {battery} Ah => N = {nr_of_battery:.2f} \
#     Numărul de acumulatoare de 12V/{battery}Ah necesare pentru sursa {list_pwr_supply_labels[i]} este N= {int(ceil(nr_of_battery))}.')
#
#     i_crt_veghe = f'{total_crt_veghe:.4f}'
#     i_crt_alarma = f'{total_crt_alarma:.4f}'
#     nr_acc = f'{nr_of_battery:.2f}'
#     nr_acc_rounded = f'{int(ceil(nr_of_battery))}'
#     totall_crt_veghe_mA = f'{table_calc_final["TOTAL CONSUM VEGHE"].sum():.1f}'
#     totall_crt_alarma_mA = f'{table_calc_final["TOTAL CONSUM ALARMA"].sum():.1f}'
#
#     #creare dictionar cu valori ce se afiseaza in descrierea calculelor de sub tabelul de calcul consum curent efractie
#     dict_val_tabel_consum_efr = {}
#     dict_val_tabel_consum_efr.update({'efr_consum_SA'+str(i) : list_pwr_supply_labels[i],
#                                       'efr_i_veghe_SA'+str(i) : i_crt_veghe,
#                                       'efr_i_alarma_SA'+str(i) : i_crt_alarma,
#                                       'efr_acc_SA'+str(i) : str(battery),
#                                       'efr_nr_acc_SA'+str(i) : nr_acc,
#                                       'efr_acc_SA'+str(i) : str(battery),
#                                       'efr_acc_rounded_SA'+str(i) : nr_acc_rounded,
#                                       'efr_consum_TOTALL_veghe'+str(i) : totall_crt_veghe_mA,
#                                       'efr_consum_TOTALL_alarma'+str(i) : totall_crt_alarma_mA})
#
#     # creare dictionar pentru a scrie tabelul de calcul consum curent efractie in fisierul template word
#     df_tabel_consum_efr = table_calc_final1
#     df_tabel_consum_efr = df_tabel_consum_efr.astype(str)
#     df_tabel_consum_efr.rename(columns={'nr_crt': 'efr_consum_nr_crt'+str(i),
#                                         'Denumire element': 'efr_consum_denumire_element'+str(i),
#                                         'Cod echipament': 'efr_consum_tip_element'+str(i),
#                                         'Tensiune alimentare de baza': 'efr_consum_tens_baza'+str(i),
#                                         'Tensiune alimentare de rezerva': 'efr_consum_tens_rez'+str(i),
#                                         'Consum veghe': 'efr_consum_crt_veghe'+str(i),
#                                         'Consum alarma': 'efr_consum_crt_alarma'+str(i),
#                                         'Cantitate': 'efr_consum_cantitate'+str(i),
#                                         'Consum total veghe': 'efr_consum_total_veghe'+str(i),
#                                         'Consum total alarma': 'efr_consum_total_alarma'+str(i)}, inplace=True)
#
#     dict_df_tabel_consum_efr = df_tabel_consum_efr.to_dict('records')
#     #print(dict_df_tabel_consum_efr,dict_val_tabel_consum_efr)
#     #adaugam lista de dictionare in lst si asa avem toate valorile pentru tabelele de calcul acumulatoare instr-o singura lista
#     return lst.append(dict_df_tabel_consum_efr), lst_var_SA.append(dict_val_tabel_consum_efr)


def creare_tabele_calcul_consum(i, battery, nr_of_battery):
    """Facem merge intre fisierul df_intrussion_dwg si baza de date astfel incat pentru fiecare cod de echipament
    sa avem toate caracteristicile(denumire, valorile pentru consumul in alarma si veghe, etc). Atunci cand facem merge
    si exista coloane cu acelasi nume, coloanele aferente fisierului din stanga se autodenumeste nume_coloana_x, iar
    pentru fisierul din dreapta avem nume_coloana_y. Acesta este motivul pentru care se regaseste CONSUM_VEGHE_y,
    CONSUM_ALARMA_y mai jos in cod."""
    df_intrussion_dwg_merged_with_db  = pd.merge(df_intrussion_dwg, df_db, on='COD_ECHIPAMENT')
    #print(df_intrussion_dwg_merged_with_db.columns)

    # din functia calcul_capacitate_acumulatoare() aduc ca argumente i, capacitatile bateriilor si nr_of_battery
    # creez variablia filt7 care selecteaza elementele din df_intrussion_dwg care au pe coloana "SURSA_ALIMENTARE"
    # denumirea sursei din lista de surse de alimentare si au consumul de veghe sau consumul de alarma > 0
    filt7 = ((df_intrussion_dwg_merged_with_db["INDEX"] == list_pwr_supply_labels[i]) & (
            (df_intrussion_dwg_merged_with_db["CONSUM_VEGHE_y"] > 0) | (df_intrussion_dwg_merged_with_db
                                                                      ["CONSUM_ALARMA_y"] > 0)))
    #print(filt7)
    # creez data frame-ul table_calc din data frame df_intrussion_dwg si fac afisare pe coloana(.loc) pt valorile
    # selectate de variablia filt7
    # si in plus adaug coloanele "COD_ECHIPAMENT","CANTITATE","CONSUM_VEGHE", "CONSUM_ALARMA" la acest dataframe
    table_calc = pd.DataFrame(
        df_intrussion_dwg_merged_with_db.loc[filt7, ["COD_ECHIPAMENT",
                                                     "CANTITATE",
                                                     "CONSUM_VEGHE_y",
                                                     "CONSUM_ALARMA_y"]])
    # print(table_calc)
    # transform valorile din coloana ["CANTITATE"] in valori intregiDENUMIRE_ECHIPAMENT
    table_calc["CANTITATE"] = table_calc["CANTITATE"].astype('int')
    # creez un nou dataframe table_calc_int care grupeaza elementele din dataframe-ul table_calc dupa "COD_ECHIPAMENT" si face suma pt "CANTITATE", "CONSUM_VEGHE", "CONSUM_ALARMA"
    table_calc_int = table_calc.groupby("COD_ECHIPAMENT")[["CANTITATE", "CONSUM_VEGHE_y", "CONSUM_ALARMA_y"]].sum()
    # redenumesc coloanele "CONSUM_VEGHE" : "TOTAL CONSUM VEGHE", "CONSUM_ALARMA" : "TOTAL CONSUM ALARMA" pt ca atunci cand se face merge cu
    # baza de date denumirile coloanelor sunt aceleasi si nu se pot diferentia
    table_calc_int.rename(columns={"CONSUM_VEGHE_y": "TOTAL CONSUM VEGHE", "CONSUM_ALARMA_y": "TOTAL CONSUM ALARMA"},
                          inplace=True)

    #print (table_calc_int)
    # combin elementele din dataframe-ul table_calc_int cu elementele din baza de date df_db in functie de codurile de echipament
    # se vor afisa doar elementele ale caror coduri de echipament se regasesc in dataframe-ul table_calc_int si in df_db(baza de date)
    # prin functia check_items() fac verificarea daca un cod de echipament este scris gresit sau nu se afla in vreunul din cele 2 dataframe-uri
    table_calc_merge_with_db = pd.merge(table_calc_int, df_db, on='COD_ECHIPAMENT')
    # creez data frame-ul table_calc_final in care afisez informatiile bazat pe coloanele necesare
    table_calc_final = pd.DataFrame(table_calc_merge_with_db[
                                        ['Denumire_element', 'COD_ECHIPAMENT', 'TENSIUNE_ALIMENTARE_DE_BAZA',
                                         'TENSIUNE_ALIMENTARE_DE_REZERVA', 'CONSUM_VEGHE', 'CONSUM_ALARMA',
                                         'CANTITATE',
                                         'TOTAL CONSUM VEGHE', 'TOTAL CONSUM ALARMA', 'Nr. Crt']])
    table_calc_final.sort_values(by=['Nr. Crt'], inplace=True)
    table_calc_final = table_calc_final[
        ['Denumire_element', 'COD_ECHIPAMENT', 'TENSIUNE_ALIMENTARE_DE_BAZA', 'TENSIUNE_ALIMENTARE_DE_REZERVA',
         'CONSUM_VEGHE', 'CONSUM_ALARMA', 'CANTITATE', 'TOTAL CONSUM VEGHE', 'TOTAL CONSUM ALARMA']]
    table_calc_final.reset_index(drop=True, inplace=True)
    table_calc_final.index = table_calc_final.index + 1
    table_calc_final['nr_crt'] = table_calc_final.index

    # # creez o serie pe care o denumesc Total si care este egala cu suma coloanei 'Consum total (W)'
    # Total = table_calc_final['TOTAL CONSUM VEGHE'].sum()
    # # setez 'Total' ca index pt linia de Total si pentru toate coloanele vom avea NaN doar pentru coloana 'Consum total (W)' vom avea totalul
    # table_calc_final.loc['Total'] = pd.Series(table_calc_final['TOTAL CONSUM VEGHE'].sum(),
    #                                           index=['TOTAL CONSUM VEGHE'])
    # # pt ca functia sa poata returna un data frame creez acest data frame
    # table_calc_final = pd.DataFrame(table_calc_final)

    # sortez in functie de coloana 'CONSUM_VEGHE' si 'CONSUM_ALARMA' (consumurile mari sunt afisate primele)
    # table_calc_final = table_calc_final.sort_values(by=['CONSUM_VEGHE', 'CONSUM_ALARMA'], ascending=False)
    # table_calc_final
    """la tabelul cu consumul echipamentelor pt o sursa de alimentare adaug linia 
    cu consumul total pentru curentii de veghe si de alarma.
    Am facut table_calc_final1 = table_calc_final pt a nu mai schimba denumirea table_calc_final1 mai jos in cod """
    #table_calc_final1 = pd.DataFrame(table_calc_final.append(df_pwr_supply_calculation.iloc[i]))
    table_calc_final1 = table_calc_final
    #print(table_calc_final1)
    table_calc_final1 = table_calc_final1.fillna(0)
    #putem aplica applymap cu lambda insa rezultatul este acelasi ca cel dat de linia in care setez int pt nt_crt si cantitate
    #table_calc_final1 = table_calc_final1.applymap(lambda x: int(round(x, 0)) if isinstance(x, (int, float)) else x)
    # def check_float_values(x):
    #     if x > int(x):
    #         return x
    #     else:
    #         return int(x)
    # table_calc_final1 = table_calc_final1.applymap(lambda x: check_float_values(x) if isinstance(x, (int, float)) else x)
    table_calc_final1[['nr_crt','CANTITATE']] = table_calc_final1[['nr_crt','CANTITATE']].astype(int)

    # redenumesc coloanele asa cum vreau sa fie afisate in tabelul final
    table_calc_final1.rename(columns={"Denumire_element": "Denumire element", "COD_ECHIPAMENT": "Cod echipament",
                                      "TENSIUNE_ALIMENTARE_DE_BAZA": "Tensiune alimentare de baza",
                                      "TENSIUNE_ALIMENTARE_DE_REZERVA": "Tensiune alimentare de rezerva",
                                      "CONSUM_VEGHE": "Consum veghe", "CONSUM_ALARMA": "Consum alarma",
                                      "CANTITATE": "Cantitate", "TOTAL CONSUM VEGHE": "Consum total veghe",
                                      "TOTAL CONSUM ALARMA": "Consum total alarma"}, inplace=True)

    # scriu dataframe-ul cu tabelul de consum pt o sursa de alimentare in fisierul excel ce va avea sheet-urile denumite cu denumirile surselor de alimentare
    # table_calc_final1.to_excel(writer, sheet_name=list_pwr_supply_labels[i], index=True)
    # creez variabilele total_crt_veghe si total_crt_alarma pentru a putea afisa/scrie valorile in fisierul excel
    total_crt_veghe = table_calc_final['TOTAL CONSUM VEGHE'].sum() / 1000
    total_crt_alarma = table_calc_final['TOTAL CONSUM ALARMA'].sum() / 1000
    #print(table_calc_final['TOTAL CONSUM VEGHE'].sum(),table_calc_final['TOTAL CONSUM ALARMA'].sum())
    # scriu in fisierul excel formula de calcul pentru calculul acumulatorului
    # folosesc functia ceil(pentru asta am importat modulul math)pt a face rotunjire la 1 chiar daca
    # valoarea acumulatorului este sub 0.5 de ex 1.15 se va rotunji la 1, 1.55 se va rotunji tot la 1
    text_power_supply = (
        f' N= 1,25 x [({total_crt_veghe:.4f} x 24ore) + ({total_crt_alarma:.4f} x 0,5ore)] / {battery} Ah => N = {nr_of_battery:.2f} \
    Numărul de acumulatoare de 12V/{battery}Ah necesare pentru sursa {list_pwr_supply_labels[i]} este N= {int(ceil(nr_of_battery))}.')

    i_crt_veghe = f'{total_crt_veghe:.4f}'
    i_crt_alarma = f'{total_crt_alarma:.4f}'
    nr_acc = f'{nr_of_battery:.2f}'
    nr_acc_rounded = f'{int(ceil(nr_of_battery))}'
    totall_crt_veghe_mA = f'{table_calc_final["TOTAL CONSUM VEGHE"].sum():.1f}'
    totall_crt_alarma_mA = f'{table_calc_final["TOTAL CONSUM ALARMA"].sum():.1f}'

    #creare dictionar cu valori ce se afiseaza in descrierea calculelor de sub tabelul de calcul consum curent efractie
    dict_val_tabel_consum_efr = {}
    dict_val_tabel_consum_efr.update({'efr_consum_SA'+str(i) : list_pwr_supply_labels[i],
                                      'efr_i_veghe_SA'+str(i) : i_crt_veghe,
                                      'efr_i_alarma_SA'+str(i) : i_crt_alarma,
                                      'efr_acc_SA'+str(i) : str(battery),
                                      'efr_nr_acc_SA'+str(i) : nr_acc,
                                      'efr_acc_SA'+str(i) : str(battery),
                                      'efr_acc_rounded_SA'+str(i) : nr_acc_rounded,
                                      'efr_consum_TOTALL_veghe'+str(i) : totall_crt_veghe_mA,
                                      'efr_consum_TOTALL_alarma'+str(i) : totall_crt_alarma_mA})

    # creare dictionar pentru a scrie tabelul de calcul consum curent efractie in fisierul template word
    df_tabel_consum_efr = table_calc_final1
    df_tabel_consum_efr = df_tabel_consum_efr.astype(str)
    df_tabel_consum_efr.rename(columns={'nr_crt': 'efr_consum_nr_crt'+str(i),
                                        'Denumire element': 'efr_consum_denumire_element'+str(i),
                                        'Cod echipament': 'efr_consum_tip_element'+str(i),
                                        'Tensiune alimentare de baza': 'efr_consum_tens_baza'+str(i),
                                        'Tensiune alimentare de rezerva': 'efr_consum_tens_rez'+str(i),
                                        'Consum veghe': 'efr_consum_crt_veghe'+str(i),
                                        'Consum alarma': 'efr_consum_crt_alarma'+str(i),
                                        'Cantitate': 'efr_consum_cantitate'+str(i),
                                        'Consum total veghe': 'efr_consum_total_veghe'+str(i),
                                        'Consum total alarma': 'efr_consum_total_alarma'+str(i)}, inplace=True)

    dict_df_tabel_consum_efr = df_tabel_consum_efr.to_dict('records')
    #print(dict_df_tabel_consum_efr,dict_val_tabel_consum_efr)
    #adaugam lista de dictionare in lst si asa avem toate valorile pentru tabelele de calcul acumulatoare instr-o singura lista
    return lst.append(dict_df_tabel_consum_efr), lst_var_SA.append(dict_val_tabel_consum_efr)


# functie pentru calculul capacitatii acumulatoarelor necesare la fiecare sursa de alimentare in parte
def calcul_capacitate_acumulatoare():
    # ddin aceasta functie preluam argumentele i, capacitatile bateriilor si nr_of_battery pt functia creare_tabele_calcul_consum
    # aducem variabila globala in functia noastra
    df_acumulatoare = pd.DataFrame(columns=['COD_ECHIPAMENT', 'CANTITATE'])
    lista_acumulatoare = []
    #global df_acumulatoare
    global df_read_zonare
    # iteram lista list_pwr_supply_labels(lista cu denumirile surselor de alimentare) bazat pe numarul elementelor din lista
    for i in range(len(list_pwr_supply_labels)):
        # print(a.iloc[i, 0])
        sum_crt_veghe = df_pwr_supply.iloc[i, 0]
        # print(a.iloc[i, 1])
        sum_crt_alarma = df_pwr_supply.iloc[i, 1]
        battery_capacity7Ah = 7
        battery_capacity12Ah = 12
        battery_capacity18Ah = 18
        battery_capacity24Ah = 24
        nr_of_battery = (1.25 * ((sum_crt_veghe / 1000 * 24) + (sum_crt_alarma / 1000 * 0.5))) / battery_capacity7Ah
        if nr_of_battery <= 1:
            # creez un dictionar pt acumulatorul de 7Ah
            acumulator_7Ah = {'COD_ECHIPAMENT': 'PL7Ah', 'CANTITATE': '1'}
            acumulator_7Ah_copy = acumulator_7Ah.copy()
            lista_acumulatoare.append(acumulator_7Ah_copy)
            # creez un data frame pt accumulatorul de 7Ah
            #df_acumulator_7Ah = pd.DataFrame(acumulator_7Ah, columns=['COD_ECHIPAMENT', 'CANTITATE'])
            # la dataframe-ul df_intrussion_dwg adaug acumulatorul de 7Ah pt a putea scoate lista completa de cantitati de echiopamente
            #df_read_zonare = df_read_zonare.append(df_acumulator_7Ah)
            #df_acumulatoare = df_acumulatoare.append(df_acumulator_7Ah)
            # print(df_read_zonare['COD_ECHIPAMENT'])
            # apelez functia pt crearea tabelului de consum
            creare_tabele_calcul_consum(i, battery_capacity7Ah, nr_of_battery)
            # print("Pentru sursa de alimentare", list_pwr_supply_labels[i], "numarul de acumulatori de 12V, 7Ah necesari este N =", nr_of_battery)
            # print("\n")
        else:
            nr_of_battery = (1.25 * (
                    (sum_crt_veghe / 1000 * 24) + (sum_crt_alarma / 1000 * 0.5))) / battery_capacity12Ah
            if nr_of_battery <= 1:
                acumulator_12h = {'COD_ECHIPAMENT': 'PL12Ah', 'CANTITATE': '1'}
                acumulator_12h_copy = acumulator_12h.copy()
                lista_acumulatoare.append(acumulator_12h_copy)
                #df_acumulator_12h = pd.DataFrame(acumulator_12Ah, columns=['COD_ECHIPAMENT', 'CANTITATE'])
                #df_read_zonare = df_read_zonare.append(df_acumulator_12h)
                #df_acumulatoare = df_acumulatoare.append(df_acumulator_12h)
                creare_tabele_calcul_consum(i, battery_capacity12Ah, nr_of_battery)
                print("Pentru sursa de alimentare", list_pwr_supply_labels[i],
                      "numarul de acumulatori de 12V, 12Ah necesari este N =", nr_of_battery)
                print("\n")

            else:
                nr_of_battery = (1.25 * (
                        (sum_crt_veghe / 1000 * 24) + (sum_crt_alarma / 1000 * 0.5))) / battery_capacity18Ah
                if nr_of_battery <= 1:
                    acumulator_18h = {'COD_ECHIPAMENT': 'PL18Ah', 'CANTITATE': '1'}
                    acumulator_18h_copy = acumulator_18h.copy()
                    lista_acumulatoare.append(acumulator_18h_copy)
                    #df_acumulator_18h = pd.DataFrame(acumulator_18h, columns=['COD_ECHIPAMENT', 'CANTITATE'])
                    #df_intrussion=df_intrussion_dwg.append(df_acumulator_18h)
                    #df_read_zonare = df_read_zonare.append(df_acumulator_18h)
                    #df_acumulatoare = df_acumulatoare.append(df_acumulator_18h)
                    creare_tabele_calcul_consum(i, battery_capacity18Ah, nr_of_battery)

                    print("Pentru sursa de alimentare", list_pwr_supply_labels[i],
                          "numarul de acumulatori de 12V, 18Ah necesari este N =", nr_of_battery)
                    print("\n")
                else:
                    nr_of_battery = (1.25 * (
                            (sum_crt_veghe / 1000 * 24) + (sum_crt_alarma / 1000 * 0.5))) / battery_capacity24Ah
                    if nr_of_battery <= 1:
                        acumulator_24h = {'COD_ECHIPAMENT': 'DD12240', 'CANTITATE': '1'}
                        acumulator_24h_copy = acumulator_24h.copy()
                        lista_acumulatoare.append(acumulator_24h_copy)
                        #df_acumulator_24h = pd.DataFrame(acumulator_24h, columns=['COD_ECHIPAMENT', 'CANTITATE'])
                        #df_read_zonare = df_read_zonare.append(df_acumulator_24h)
                        #df_acumulatoare = df_acumulatoare.append(df_acumulator_24h)
                        creare_tabele_calcul_consum(i, battery_capacity24Ah, nr_of_battery)
                        print("Pentru sursa de alimentare", list_pwr_supply_labels[i],
                              "numarul de acumulatori de 12V, 24Ah necesari este N =", nr_of_battery)

                    else:
                        print("Capacitatea acumulatorului este prea mare pentru a putea fi incarcat \n"
                              "de centrala sau sursa. Trebuie adaugata o sursa de alimentare suplimentara",
                              nr_of_battery)
    return lista_acumulatoare

# def main_capacitate_acumulatoare():
#     #return print(calcul_capacitate_acumulatoare())
#     df_acumulatoare_calculate = pd.DataFrame(calcul_capacitate_acumulatoare())
#     return print(df_acumulatoare_calculate)






def creare_tabel_lista_cantitati():
    #apelam functia calcul_capacitate_acumulatoare() pentru a ne returna lista de dictionare ce contine acumulatoarele calculate
    df_acumulatoare_calculate = pd.DataFrame(calcul_capacitate_acumulatoare())
    #la df_acumulatoare_calculate adaugam continutul data frame-ului df_read_zonare
    df_acumulatoare_calculate = df_acumulatoare_calculate.append(df_read_zonare)
    #cream un nou dataframe ce grupeaza elementele in functie de cod echipament si numara cate elemente de acelasi tip avem
    qty_table = df_acumulatoare_calculate.groupby("COD_ECHIPAMENT")["CANTITATE"].count()
    final_qty_table = pd.merge(qty_table, df_db, on="COD_ECHIPAMENT")
    # print(final_qty_table["COD_ECHIPAMENT"])
    # Pentru ca in lista de cantitati apar si alarma de incendiu, Tamperul, le-am bagat intr-o lista dupa care se face stergerea lor din tabel
    list_value_need_dropped = ['Alarma incendiu', 'Tamper']
    final_qty_table = final_qty_table.drop(
        final_qty_table[final_qty_table.COD_ECHIPAMENT.isin(list_value_need_dropped)].index.tolist())

    # creez dataframe-ul pt a afisa ce coloane ma intereseaza si fac filtrarea in functie de coloana 'Nr. Crt'
    # pt ca nu vreau sa afisez coloana 'Nr. Crt', fac atribuirea df-ului la el insusi dar fara coloana 'Nr. Crt'
    final_qty_table[
        ['Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'Producator', 'Furnizor', 'Document insotior', 'Nr. Crt']]
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
    #print(dict_df_final_qty_table_for_word)
    #print(lst_coduri_echip_pt_fise_tehnice)

    return dict_df_final_qty_table_for_word

# def preluare_coduri_echip_din_lista_cantitati_efractie():
#     #apelam functia calcul_capacitate_acumulatoare() pentru a ne returna lista de dictionare ce contine acumulatoarele calculate
#     df_acumulatoare_calculate = pd.DataFrame(calcul_capacitate_acumulatoare())
#     #la df_acumulatoare_calculate adaugam continutul data frame-ului df_read_zonare
#     df_acumulatoare_calculate = df_acumulatoare_calculate.append(df_read_zonare)
#     #cream un nou dataframe ce grupeaza elementele in functie de cod echipament si numara cate elemente de acelasi tip avem
#     qty_table = df_acumulatoare_calculate.groupby("COD_ECHIPAMENT")["CANTITATE"].count()
#     final_qty_table = pd.merge(qty_table, df_db, on="COD_ECHIPAMENT")
#     # print(final_qty_table["COD_ECHIPAMENT"])
#     # Pentru ca in lista de cantitati apar si alarma de incendiu, Tamperul, le-am bagat intr-o lista dupa care se face stergerea lor din tabel
#     list_value_need_dropped = ['Alarma incendiu', 'Tamper']
#     final_qty_table = final_qty_table.drop(
#         final_qty_table[final_qty_table.COD_ECHIPAMENT.isin(list_value_need_dropped)].index.tolist())
#
#     # creez dataframe-ul pt a afisa ce coloane ma intereseaza si fac filtrarea in functie de coloana 'Nr. Crt'
#     # pt ca nu vreau sa afisez coloana 'Nr. Crt', fac atribuirea df-ului la el insusi dar fara coloana 'Nr. Crt'
#     final_qty_table[
#         ['Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'Producator', 'Furnizor', 'Document insotior', 'Nr. Crt']]
#     final_qty_table = pd.DataFrame(final_qty_table[
#                                        ['Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'Producator', 'Furnizor',
#                                         'Document insotior', 'Nr. Crt']]).sort_values(by='Nr. Crt', ascending=True)
#
#     final_qty_table = final_qty_table[
#         ['Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'Producator', 'Furnizor',
#          'Document insotior']]
#
#     df_final_qty_table_for_word = final_qty_table[
#         ['Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'Producator', 'Furnizor',
#          'Document insotior']]
#
#     final_qty_table.reset_index(drop=True, inplace=True)
#     final_qty_table.index = final_qty_table.index + 1
#     # sortez valorile afisate in functie de 'CANTITATE' si 'COD_ECHIPAMENT'
#     # final_qty_table = final_qty_table.sort_values(by=['Denumire_element', 'CANTITATE'], ascending=False)
#     final_qty_table.rename(columns={'COD_ECHIPAMENT': 'Cod echipament', 'CANTITATE': 'Cantitate'}, inplace=True)
#     # print(final_qty_table)
#     # final_qty_table.to_excel(writer, sheet_name='Cantitati echip', index=True)
#
#     df_final_qty_table_for_word.reset_index(drop=True, inplace=True)
#     df_final_qty_table_for_word.index = df_final_qty_table_for_word.index + 1
#     df_final_qty_table_for_word['nr_crt_cantitati'] = df_final_qty_table_for_word.index
#     df_final_qty_table_for_word = df_final_qty_table_for_word[
#         ['nr_crt_cantitati', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'Producator', 'Furnizor',
#          'Document insotior']]
#     #creare lista cu codurile de echipamente din lista de cantitati, ce va fi folosita pentru a fi returnata de
#     # functia efr_coduri_echip_pt_fise_tehnice()
#     lista_coduri_echipamente = list(df_final_qty_table_for_word['COD_ECHIPAMENT'])
#     for item in lista_coduri_echipamente:
#         lst_coduri_echip_pt_fise_tehnice.append(item)
#
#     # df_final_qty_table_for_word = df_final_qty_table_for_word.astype(str)
#     # df_final_qty_table_for_word.rename(columns={'nr_crt_cantitati': 'efr_cantitati_nr_crt',
#     #                                             'Denumire_element': 'efr_cantitati_denumire_element',
#     #                                             'COD_ECHIPAMENT': 'efr_cantitati_tip_element',
#     #                                             'CANTITATE': 'efr_cantitati_cantitate',
#     #                                             'Producator': 'efr_cantitati_producator',
#     #                                             'Furnizor': 'efr_cantitati_furnizor',
#     #                                             'Document insotior': 'efr_cantitati_CE'}, inplace=True)
#     # dict_df_final_qty_table_for_word = df_final_qty_table_for_word.to_dict('records')
#     #print(dict_df_final_qty_table_for_word)
#     #print(lst_coduri_echip_pt_fise_tehnice)
#
#     return lst_coduri_echip_pt_fise_tehnice


def denumire_sursa_antiefractie(arg_SA):
    dict_sursa_alimentare = {'efr_consum_SA': arg_SA}
    dict_sursa_alimentare_copy = dict_sursa_alimentare.copy()
    list_of_dict_sursa_alimentare = []
    list_of_dict_sursa_alimentare.append(dict_sursa_alimentare_copy)
    #print(list_of_dict_sursa_alimentare)
    return list_of_dict_sursa_alimentare

# def creare_tabel_zonare():
#     # global df_intrussion_dwg
#     # df_db = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_efractie.xlsx')
#     # combinam df_intrussion_dwg cu df_db in fct de 'COD_ECHIPAMENT' pt a avea denumirile de echipamente cu diacritice ă, etc
#     df_intrussion = pd.merge(df_intrussion_dwg, df_db, on='COD_ECHIPAMENT')
#     # creez data frame zonare_table cu coloanele necesare pt tabelul zonare
#     zonare_table = pd.DataFrame(df_intrussion[['NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE',
#                                                'SIMBOL_ECHIPAMENT', 'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA',
#                                                'Tip cablu']])
#     # sterg liniile ce nu contin valori pe coloana 'NUMAR_ZONA'
#     # toate zonele din sistem vor trebui sa aiba atribuita o zona, altfel(daca nu se completeaza atributul corespunzator zonei in autocad) zona/zonele nu vor aparea in tabelul zonare
#     zonare_table = zonare_table.dropna(subset=['NUMAR_ZONA'])
#     # verificam daca elementele din fisierul importat din dwg se inseriaza sau nu. verificarea se face prin introducerea zonelor
#     # care se repeta in lista seried_zones_list. Ulterior verific daca lista seried_zones_list are vreun element in ea sau nu.
#     # daca are, inseamna ca avem zone inseriate si se executa conditiile de sub if
#     # daca nu are, insemana ca nu avem zone inseriate si se executa conditiile de sub else
#     check_seried_zones = list(zonare_table['NUMAR_ZONA'])
#     check_seried_zones
#     unic_zones_list = []
#     seried_zones_list = []
#     for item in check_seried_zones:
#         if item not in unic_zones_list:
#             unic_zones_list.append(item)
#         else:
#             seried_zones_list.append(item)
#     if len(seried_zones_list) != 0:
#         # din df zonare_table grupez elementele care se inseriaza(elementele ce se inseriaza, apar in zonare cu acelasi nr de zona)
#         # si le sortez in functie de coloana 'SIMBOL_ECHIPAMENT' astfel incat in tabelul de zonare simbolurile inseriate sa apara in ordine crescatoare
#         # de exemplu vor fi afisate SOC1,SOC2,SOC3 nu SOC2,SOC3,SOC1
#         df_group_seried_zones = zonare_table.loc[zonare_table.NUMAR_ZONA.duplicated(keep=False), :].sort_values(
#             by='SIMBOL_ECHIPAMENT', ascending=True)
#         # df_group_seried_zones
#         # din df_group_seried_zones fac concatenarea pe coloanele'Denumire_element','COD_ECHIPAMENT','SIMBOL_ECHIPAMENT' (doar stringuri)
#         # !!!Atentie!!!! in cazul in care la zonele ce se inseriaza nu exista aceleasi denumiri pe coloanele 'NUMAR_ZONA','TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA'
#         # atunci in tabelul zonare zonele respective nu se vor inseria!!!! Este obligatoriu sa avem fix aceleasi denumiri
#         concat_seried_zones = \
#         df_group_seried_zones.groupby(['NUMAR_ZONA', 'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA'])[
#             ['Denumire_element', 'COD_ECHIPAMENT', 'SIMBOL_ECHIPAMENT', 'Tip cablu']].agg(','.join).reset_index()
#         # concat_seried_zones
#         # scot zonele care se inseriaza si le bag intr-o lista pentru a le sterge din dataframe-ul zonare_table
#         # dupa ce sterg zonele care se repeta in df zonare_table, o sa adaug la noul zonare table liniile cu zonele inseriate
#         val_should_be_dropped = list(concat_seried_zones['NUMAR_ZONA'])
#         # aceasta linie sterge din df zonare_table zonele care apar de 2 sau mai multe ori. Ulterior aceste zone se vor prelucra(inseria) si se vor adauga la data frame zonare_table  -> vezi ultimile linii din functie
#         zonare_table = zonare_table.drop(
#             zonare_table[zonare_table.NUMAR_ZONA.isin(val_should_be_dropped)].index.tolist())
#
#         # pentru ca pe coloana cod echipament atunci cand avem acelasi tip de simbol, prin concatenare simbolul apare de mai multe ori
#         # prin metoda split extrag coloana COD_ECHIPAMENT si o introduc intr-o lista
#         # !!!Atentie!!! elementele extrase din coloana COD_ECHIPAMENT prin  metoda split nu sunt string-uri - sunt float-uri
#         # creez o functie care itereaza elementele extrase din coloana COD_ECHIPAMENT prin metoda split si le introduce intr-o lista
#         # in lista vor fi introduse doar elemente ce apar o singura data(asa realizez eliminarea codurilor de echipament ce apar de mai multe ori pe coloana COD_ECHIPAMENT in df concat_seried_zones )
#         # concat_seried_zones.COD_ECHIPAMENT.str.split(',')
#         def remove_duplicates(my_list):
#             list = []
#             for item in my_list:
#                 if item not in list:
#                     list.append(item)
#                     list.sort()
#             return list
#
#         concat_seried_zones['COD_ECHIPAMENT'] = concat_seried_zones.COD_ECHIPAMENT.str.split(',').apply(
#             remove_duplicates)
#         # pentru ca valorile extrase din coloana 'COD_ECHIPAMENT' reprezentau o lista, am creat variabila concatenare_cod_echip
#         # prin care am transformat valorile de pe coloana 'COD_ECHIPAMENT' din lista in string
#         # fac acelasi lucru si pentru coloana 'Denumire_element'
#         concatenare_cod_echip = concat_seried_zones['COD_ECHIPAMENT'].apply(', '.join)
#         concat_seried_zones['COD_ECHIPAMENT'] = concatenare_cod_echip
#         concat_seried_zones['Denumire_element'] = concat_seried_zones.Denumire_element.str.split(',').apply(
#             remove_duplicates)
#         concatenare_den_elem = concat_seried_zones['Denumire_element'].apply(', '.join)
#         concat_seried_zones['Denumire_element'] = concatenare_den_elem
#
#         concat_seried_zones['Tip cablu'] = concat_seried_zones['Tip cablu'].str.split(',').apply(remove_duplicates)
#         concatenare_tip_cablu = concat_seried_zones['Tip cablu'].apply(', '.join)
#         concat_seried_zones['Tip cablu'] = concatenare_tip_cablu
#
#         # din df_group_seried_zones fac concatenarea pe coloana'CANTITATE' (doar int-uri)
#         concat_seried_zones_by_qty = df_group_seried_zones.groupby(['NUMAR_ZONA'])['CANTITATE'].sum().reset_index()
#         # concat_seried_zones_by_qty
#
#         # pentru realizarea df-ului final combin 'concat_seried_zones' cu 'concat_seried_zones_by_qty' in functie de coloana 'NUMAR_ZONA'
#         seried_zones = (pd.merge(concat_seried_zones, concat_seried_zones_by_qty, on='NUMAR_ZONA'))
#         seried_zones = seried_zones[
#             ['NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'SIMBOL_ECHIPAMENT', 'TIP_ZONA',
#              'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA', 'Tip cablu']]
#         # seried_zones
#
#         # la dataframe-ul zonare_table(care nu mai contine zonele care apareau de mai mult de 1 data) adaugam zonele inseriate dupa ce au fost prelucrate
#         zonare_table = zonare_table.append(seried_zones, ignore_index=True, sort=False)
#         # sortez valorile din tabelul final de zonare in functie de numarul zonei
#         zonare_table = pd.DataFrame(zonare_table.sort_values(by=['NUMAR_ZONA'], ignore_index=True))
#         # resetez index-ul si salvez resetarea in data frame
#         zonare_table.reset_index(drop=True, inplace=True)
#         # setez ca noul index sa inceapa de la 1
#         zonare_table.index = zonare_table.index + 1
#         zonare_table['nr_crt_zonare'] = zonare_table.index
#         # apelez functia journal_cables_table si folosesc ca argument data frame-ul zonare table
#         # aici pierd coloana "Tip cablu din DF-ul zonare_table astfel incat in excel sa nu mai afisez aceasta coloana
#         journal_cables_table(zonare_table)
#         zonare_table = zonare_table[
#             ['nr_crt_zonare', 'NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'SIMBOL_ECHIPAMENT',
#              'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA']]
#         df_zonare_table = zonare_table[
#             ['nr_crt_zonare', 'NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'SIMBOL_ECHIPAMENT',
#              'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA']]
#         # redenumim coloanele cu denumirile ce vrem sa le afisam in excel
#         zonare_table.rename(columns={'NUMAR_ZONA': 'Număr zonă', 'Denumire_element': 'Denumire echipament',
#                                      'COD_ECHIPAMENT': 'Cod echipament', 'CANTITATE': 'Cantitate',
#                                      'SIMBOL_ECHIPAMENT': 'Simbol echipament', 'TIP_ZONA': 'Tip zonă',
#                                      'PARTITIE': 'Aria', 'DENUMIRE_ZONA_PROTEJATA': 'Zonă protejată'}, inplace=True)
#
#         # scriem tabelul zonare in fisierul cu toate informatiile despre efractie
#         zonare_table.to_excel(writer, sheet_name='Zonare', index=True)
#         # creare dictionar pentru docx-mailmerge in word
#         df_zonare_table = df_zonare_table.astype(str)
#         df_zonare_table.rename(columns={'nr_crt_zonare': 'efr_zonare_nr_crt',
#                                         'NUMAR_ZONA': 'efr_zonare_nr_zona',
#                                         'Denumire_element': 'efr_zonare_denumire_element',
#                                         'COD_ECHIPAMENT': 'efr_zonare_tip_element',
#                                         'CANTITATE': 'efr_zonare_cantitate',
#                                         'SIMBOL_ECHIPAMENT': 'efr_zonare_simbol_element',
#                                         'TIP_ZONA': 'efr_zonare_tip_zona',
#                                         'PARTITIE': 'efr_zonare_partitie',
#                                         'DENUMIRE_ZONA_PROTEJATA': 'efr_zonare_zona_protejata'}, inplace=True)
#         dict_df_zonare_table = df_zonare_table.to_dict('records')
#         return dict_df_zonare_table
#
#     else:
#         # sortez valorile din tabelul final de zonare in functie de numarul zonei
#         zonare_table = pd.DataFrame(zonare_table.sort_values(by=['NUMAR_ZONA'], ignore_index=True))
#         # resetez index-ul si salvez resetarea in data frame
#         zonare_table.reset_index(drop=True, inplace=True)
#         # setez ca noul index sa inceapa de la 1
#         zonare_table.index = zonare_table.index + 1
#         zonare_table['nr_crt_zonare'] = zonare_table.index
#         # apelez functia journal_cables_table si folosesc ca argument data frame-ul zonare table
#         journal_cables_table(zonare_table)
#         zonare_table = zonare_table[
#             ['nr_crt_zonare', 'NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'SIMBOL_ECHIPAMENT',
#              'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA']]
#         df_zonare_table = zonare_table[
#             ['nr_crt_zonare', 'NUMAR_ZONA', 'Denumire_element', 'COD_ECHIPAMENT', 'CANTITATE', 'SIMBOL_ECHIPAMENT',
#              'TIP_ZONA', 'PARTITIE', 'DENUMIRE_ZONA_PROTEJATA']]
#         # redenumim coloanele cu denumirile ce vrem sa le afisam in excel
#         zonare_table.rename(columns={'NUMAR_ZONA': 'Număr zonă', 'Denumire_element': 'Denumire echipament',
#                                      'COD_ECHIPAMENT': 'Cod echipament', 'CANTITATE': 'Cantitate',
#                                      'SIMBOL_ECHIPAMENT': 'Simbol echipament', 'TIP_ZONA': 'Tip zonă',
#                                      'PARTITIE': 'Aria', 'DENUMIRE_ZONA_PROTEJATA': 'Zonă protejată'}, inplace=True)
#
#         # scriem tabelul zonare in fisierul cu toate informatiile despre efractie
#         zonare_table.to_excel(writer, sheet_name='Zonare', index=True)
#
#         df_zonare_table = df_zonare_table.astype(str)
#         df_zonare_table.rename(columns={'nr_crt_zonare': 'efr_zonare_nr_crt',
#                                         'NUMAR_ZONA': 'efr_zonare_nr_zona',
#                                         'Denumire_element': 'efr_zonare_denumire_element',
#                                         'COD_ECHIPAMENT': 'efr_zonare_tip_element',
#                                         'CANTITATE': 'efr_zonare_cantitate',
#                                         'SIMBOL_ECHIPAMENT': 'efr_zonare_simbol_element',
#                                         'TIP_ZONA': 'efr_zonare_tip_zona',
#                                         'PARTITIE': 'efr_zonare_partitie',
#                                         'DENUMIRE_ZONA_PROTEJATA': 'efr_zonare_zona_protejata'}, inplace=True)
#         dict_df_zonare_table = df_zonare_table.to_dict('records')
#         return dict_df_zonare_table


# def journal_cables_table(zonare_table):
#     # creare df gol ce va folosit pt crearea tabelului cu jurnalul de cabluri
#     df_cables_journal = pd.DataFrame(columns=['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu'])
#     # creez o serie pt a putea adauga centrala de efractie si modulele de extensie la zone. Aceasta serie va fi coloana "Pana la"
#     serie_pana_la = pd.Series(dtype=object)
#     # combin dataframe-ul read zonare cu baza de date pentru a avea disponibile toate coloanele
#     df_merged_zonare_with_db = pd.merge(df_intrussion_dwg, df_db, on="COD_ECHIPAMENT")
#
#     # extragere centrala si module de extensie din zonare
#     # creez un dataframe gol df_list_of_modules in care stochez centrala si modulele de extensie, dupa care introudc continutul
#     # coloanei 'SIMBOL_ECHIPAMENT' in lista list_of_modules pe care o voi folosi pentru a putea crea seria Pana la
#     # lista_module a fost adaugata manual pt a putea face identificarea centralei si mex-urilor in zonare
#     # totodata adaug centrala si modulele de extensie la dataframe-ul df_cables_journal
#     df_list_of_modules = pd.DataFrame(columns=['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu'])
#     df_only_modules = pd.DataFrame(columns=['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu'])
#     lista_module = ['Centrală', 'Surs', 'Modul de', 'Tastat']
#
#     for item in lista_module:
#         filter_module = df_merged_zonare_with_db['Denumire_element'].str.contains(item)
#         df_module = pd.DataFrame(
#             df_merged_zonare_with_db.loc[filter_module, ['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu']])
#         df_list_of_modules = df_list_of_modules.append(df_module)
#         # df_cables_journal = df_cables_journal.append(df_module)
#     # df_cables_journal
#     list_of_modules = list(df_list_of_modules['SIMBOL_ECHIPAMENT'])
#     list_of_modules.sort()
#
#     # functia get_nr_of_zones_per_device preia din baza de date numarul de zone de pe placa de baza a
#     # fiecarei centrale sau modul de extensie
#     def get_nr_of_zones_per_device(i):
#         filt = df_merged_zonare_with_db["SIMBOL_ECHIPAMENT"] == list_of_modules[i]
#         df_get_number_of_zones_from_db = pd.DataFrame(df_merged_zonare_with_db.loc[
#                                                           filt, ['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu',
#                                                                  'Nr_zone', 'Nr_total_zone', 'INDEX']])
#         number_zone_per_device = df_get_number_of_zones_from_db['Nr_zone'].iloc[0].astype(int)
#         return number_zone_per_device
#
#     # creare dataframe cu elementele care sunt surse de alimentare
#     df_merged_zonare_with_db.sort_values(by=['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT'], ascending=True)
#     fliter_modules_with_power_supplies = (df_merged_zonare_with_db['Putere consumata (Watt)'] > 0)
#     df_only_power_supplies = df_merged_zonare_with_db.loc[
#         fliter_modules_with_power_supplies, ['Denumire_element', 'NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu',
#                                              'Nr_zone', 'Nr_total_zone', 'INDEX', 'Nr. Crt']]
#     df_only_power_supplies = df_only_power_supplies.sort_values(by=['Nr. Crt', 'SIMBOL_ECHIPAMENT'], ascending=True)
#     df_only_power_supplies[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu']]
#     df_only_power_supplies['Pana la'] = 'TAS'
#     df_only_power_supplies = df_only_power_supplies[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Pana la', 'Tip cablu']]
#
#     # creare dataframe cu elementele care nu sunt zone(centrale, module de extensie, tast, etc)
#     # filter_modules = pd.isna(df_merged_zonare_with_db['NUMAR_ZONA'])
#     # df_only_modules = df_merged_zonare_with_db.loc[filter_modules, ['Denumire_element','NUMAR_ZONA',
#     # 'SIMBOL_ECHIPAMENT','Tip cablu','Nr_zone','Nr_total_zone','INDEX', 'Nr. Crt']]
#     # df_only_modules = df_only_modules.sort_values(by = ['Nr. Crt','SIMBOL_ECHIPAMENT'], ascending = True)
#     # df_only_modules[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu']]
#
#     # adaug la df_only_modules BUS-urile de comunicatie
#     nr_linii_BUS = int(input("Cate linii de BUS contine sistemul antiefractie"))
#     lista_surse = []
#     dictionar = {}
#     for i in range(0, nr_linii_BUS):
#         element = input(f'Introdu elementele componente pentru BUS{i + 1} separate de virgula si fara spatii:')
#         element = element.split(',')
#         dictionar.update({i + 1: element})
#
#         # df_only_modules = df_only_modules.append
#         # print(lista)
#         # nr_linii_BUS +=1
#     # dictionar.items()
#
#     serie_de_la_module = pd.Series(dtype=object)
#     serie_pana_la_module = pd.Series(dtype=object)
#
#     for i in range(len(dictionar)):
#         for key, value in dictionar.items():
#             serie_valori = pd.Series(dictionar.values())
#
#     # serie_valori
#     for i in range(len(serie_valori)):
#         for p in range(len(serie_valori[i])):
#             if ((p >= 0) & (p < (len(serie_valori[i]) - 1))):
#                 serie_de_la_module = serie_de_la_module.append(pd.Series(serie_valori[i][p]), ignore_index=True)
#             if ((p >= 1) & (p < (len(serie_valori[i])))):
#                 serie_pana_la_module = serie_pana_la_module.append(pd.Series(serie_valori[i][p]), ignore_index=True)
#
#     df_only_modules['SIMBOL_ECHIPAMENT'] = list(serie_de_la_module)
#     df_only_modules['Pana la'] = list(serie_pana_la_module)
#     df_only_modules['Tip cablu'] = 'Lyy6x0.22'
#     df_only_modules[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Pana la', 'Tip cablu']]
#
#     # creare dataframe cu sirene
#     df_only_sirens = pd.DataFrame(columns=['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Tip cablu'])
#     lista_sirene = ['Siren', 'siren']
#
#     for item in lista_sirene:
#         filter_sirene = df_merged_zonare_with_db['Denumire_element'].str.contains(item)
#         df_sirens = pd.DataFrame(
#             df_merged_zonare_with_db.loc[filter_sirene, ['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'INDEX', 'Tip cablu']])
#         df_only_sirens = df_only_sirens.append(df_sirens)
#     df_only_sirens = df_only_sirens.sort_values(by='SIMBOL_ECHIPAMENT', ascending=False)
#     df_only_sirens.rename(columns={'INDEX': 'Pana la'}, inplace=True)
#     df_only_sirens = df_only_sirens[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Pana la', 'Tip cablu']]
#     df_only_sirens
#
#     # creare dataframe cu elementele care sunt doar zone
#     # df_only_zones = df_merged_zonare_with_db.dropna(subset=['NUMAR_ZONA'])
#     # df_only_zones = df_only_zones.sort_values(by = ['NUMAR_ZONA','SIMBOL_ECHIPAMENT'], ascending = True)
#     # zonare_table este preluat dion functia creare_tabel_zonare()
#     # este atributul functiei journal_cables_table
#     # pentru ca zonare table nu purta coloana tip cablu, am adaugat aceasta coloana si va trebui extrasa astfel
#     # incat sa nu mai fie afisata in tabelul cu zonarea.
#     df_only_zones = zonare_table
#     # extrag din fiecare string "Zona " si convertesc valorile ramase in int-uri
#     df_only_zones['NUMAR_ZONA'] = df_only_zones['NUMAR_ZONA'].replace({'Zona ': ''}, regex=True)
#     df_only_zones['NUMAR_ZONA'] = df_only_zones['NUMAR_ZONA'].astype('int')
#
#     no_of_zones = df_only_zones['NUMAR_ZONA'].count()
#     no_of_zones
#     # df_only_zones
#     # print(zonare_table)
#
#     # adaugare CE si ME(modulele de extensie) la seria pana la (se completeaza coloana pana la)
#     # creez un dictionar gol in care voi introduce key =(CE, ME1, ME2, etc) iar ca valori voi asocia lista "zones"
#     intrussion_modules_and_zones = {}
#     count2 = 0
#     count = 1
#     for i in range(len(list_of_modules)):
#         # creez o lista goala in care introduc valorile ce se vor asocia la fiecare modul de extensie in parte 1-8,9-16,17-24 etc
#         zones = []
#         for p in range(0, get_nr_of_zones_per_device(i)):
#             zones.append(count)
#             count += 1
#             # print(zones)
#             if count2 < no_of_zones:
#                 df_cables_journal = df_cables_journal.append(df_only_zones.iloc[count2], ignore_index=True)
#                 count2 += 1
#                 # print(count2)
#             else:
#                 continue
#
#         intrussion_modules_and_zones.update({list_of_modules[i]: zones})
#
#     # afisare cheie si valoare pt dictioanr
#     # intrussion_modules_and_zones.items()
#     # creez o serie din dictionalul intrussion_modules_and_zones
#     series = pd.Series(intrussion_modules_and_zones)
#     # series
#
#     for i in range(len(df_only_zones['NUMAR_ZONA'])):
#         for key, value in intrussion_modules_and_zones.items():
#             if df_only_zones['NUMAR_ZONA'].iloc[i] in value:
#                 serie_pana_la = serie_pana_la.append(pd.Series(key), ignore_index=True)
#
#     #     serie_pana_la
#     #     count2 = 0
#     #     for i in range(len(list_of_modules)):
#     #         for p in range(0, get_nr_of_zones_per_device(i)):
#     #             df_cables_journal = df_cables_journal.append(df_only_zones.iloc[count2], ignore_index=True)
#     #             serie_pana_la = serie_pana_la.append(pd.Series(list_of_modules[i]), ignore_index=True)
#     #             count2 += 1
#
#     df_cables_journal['Pana la'] = serie_pana_la
#     df_cables_journal = df_cables_journal[['NUMAR_ZONA', 'SIMBOL_ECHIPAMENT', 'Pana la', 'Tip cablu']]
#     # print(df_cables_journal)
#
#     # adaunam cele 4 dataframe-uri pentru a avea un tabel final
#     frames = [df_only_power_supplies, df_only_modules, df_only_sirens, df_cables_journal]
#     result = pd.concat(frames)
#     result.reset_index(drop=True, inplace=True)
#     result.index = result.index + 1
#     # creez coloana cu numerotarile cablurilor E1, E2, E2.....cate cabluri sunt in total
#     label_cable = []
#     for i in range(len(result['NUMAR_ZONA'])):
#         label_cable.append('E' + str(i + 1))
#     result['NUMAR_ZONA'] = label_cable
#     result['SIMBOL_ECHIPAMENT'] = result['SIMBOL_ECHIPAMENT'].replace({',': ' prin '}, regex=True)
#     result.rename(columns={'NUMAR_ZONA': 'Cod cablu', 'SIMBOL_ECHIPAMENT': 'De la', 'Pana la': 'Până la'}, inplace=True)
#     result[['Cod cablu', 'De la', 'Până la', 'Tip cablu']]
#     df_result_to_word = pd.DataFrame(result[['Cod cablu', 'De la', 'Până la', 'Tip cablu']])
#     # scriem tabelul zonare in fisierul cu toate informatiile despre efractie
#     result.to_excel(writer, sheet_name='Jurnal cabluri', index=True)
#
#     #creez dictionarul pentru a putea scrie in fisierul word
#     df_result_to_word.reset_index(drop=True, inplace=True)
#     df_result_to_word.index = df_result_to_word.index + 1
#     df_result_to_word['nr_crt'] = df_result_to_word.index
#     df_result_to_word[['nr_crt','Cod cablu', 'De la', 'Până la', 'Tip cablu']]
#     df_result_to_word = df_result_to_word.astype(str)
#     df_result_to_word.rename(columns={'nr_crt': 'efr_jurnal_nr_crt',
#                                     'Cod cablu': 'efr_jurnal_cod_cablu',
#                                     'De la': 'efr_jurnal_de_la',
#                                     'Până la': 'efr_jurnal_pana_la',
#                                     'Tip cablu': 'efr_jurnal_tip_cablu'}, inplace=True)
#     dict_df_result_to_word = df_result_to_word.to_dict('records')
#     #print(dict_df_result_to_word)
#     return dict_df_result_to_word


#if __name__ == '__main__':
#calcul_capacitate_acumulatoare()
#main_capacitate_acumulatoare()
# am bagat functia calcul_capacitate_acumulatoare() si creare_tabele_calcul_consum() sub return_dict_tabel_consum_efr()

    #return_dict_tabel_consum_efr()


#creare_tabel_lista_cantitati() apeleaza functia calcul_capacitate_acumulatoare() care la
#randul ei apeleaza functia creare_tabele_calcul_consum(i, battery, nr_of_battery)

#functia tabele_consum() preia lista de liste de dictionare din lst si o returneaza astfel incat lista de
# liste de dicionare sa fie folosite in modulul main pt a scrie in tabelele de calcul al acumulatoarelor din word
def tabele_consum():
    #lista_echipamente_tabele_consum = list(map(dict, chain.from_iterable(lst)))
    lista_echipamente_tabele_consum = lst
    #print(lst)
    #print(lista_echipamente_tabele_consum)
    return lista_echipamente_tabele_consum

#functia var_surse_alim() aduce lista de dictionare lst_var_SA, o salveaza in variabila lista_var_surse_efr si
# o retuneaza pentru a fi utilizata in modulul main(pt a scrie valorile in fisierul word.
def var_surse_alim():
    #lista_echipamente_tabele_consum = list(map(dict, chain.from_iterable(lst)))
    lista_var_surse_efr = lst_var_SA
    #print(lst)
    #print(lista_var_surse_efr)
    return lista_var_surse_efr

# def efr_coduri_echip_pt_fise_tehnice():
#     lista_coduri_echip_pt_fise_tehnice = lst_coduri_echip_pt_fise_tehnice
#     #print(lista_coduri_echip_pt_fise_tehnice)
#     return lista_coduri_echip_pt_fise_tehnice





if __name__ == '__main__':
    creare_tabel_lista_cantitati()
    #preluare_coduri_echip_din_lista_cantitati_efractie()
    tabele_consum()
    var_surse_alim()
    #efr_coduri_echip_pt_fise_tehnice()
# creare_tabel_zonare()

# writer.save()

#  de vazut ce de poate face la linia 141 pt a nu mai primi atentionare
# linia 141 -> table_calc_int = table_calc.groupby("COD_ECHIPAMENT")["CANTITATE", "CONSUM_VEGHE", "CONSUM_ALARMA"].sum()
# imi afisa atentionare si am bagat lista de coloane in alta lista [["CANTITATE", "CONSUM_VEGHE", "CONSUM_ALARMA"]]
