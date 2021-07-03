import pandas as pd
import sys

df_db_TVCI = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_TVCI.xlsx')
df_TVCI_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\TVCI.txt', delimiter="\t")


# Facem verificarea daca fiecare cod de echipamente din fisierul importat din DWG se regaseste in baza de date.
# In cazul in care nu se regasesc, atunci acestea fie au fost scrise gresit si vor trebui sa fie corectate, fie nu exista in
# baza de date si trebuiesc introduse.
def verific_echip_inainte_de_calcule():
    # creez o lista cu codurile de echipamente de pe coloana 'COD_ECHIPAMENT' din fisierul importat din dwg
    list_equip_codes_from_dwg = list(df_TVCI_dwg['COD_ECHIPAMENT'])
    # creez o lista cu valorile de pe coloana 'COD_ECHIPAMENT' din baza de date
    list_equip_codes_from_db = list(df_db_TVCI['COD_ECHIPAMENT'])
    # creez o lista goala in care voi introduce valorile de pe coloana 'COD_ECHIPAMENT' din fisierul importat din dwg
    # ce nu se regasesc in lista cu codurile de echipamente din baza de date
    list_missing_equip_codes = []
    # itezez lista list_equip_codes_from_dwg si elementele ce nu se regasesc in baza de date sunt adaugate in list_missing_equip_codes
    for item in list_equip_codes_from_dwg:
        if item not in list_equip_codes_from_db:
            list_missing_equip_codes.append(item)
    # in cazul in care unul sau mai multe elemente sunt introduse in list_missing_equip_codes atunci acestea sunt afisate si
    # executia programului este oprita
    if len(list_missing_equip_codes) != 0:
        print(f' Codurile de echipamente {list_missing_equip_codes} nu se regasesc in baza de date!\
 Adaugati echipamentele in baza de date sau verificati ca la atributele alocate in DWG, codurile au fost scrise corect!')
        sys.exit(1)

verific_echip_inainte_de_calcule()

def verificare_simboluri_echipamente():
    lista_simboluri_echipamente_TVCI = list(df_TVCI_dwg['SIMBOL_ECHIPAMENT'])
    #print(lista_simboluri_echipamente_TVCI)
    lista_simboluri_verificate = []
    lista_simboluri_dublate = []
    for item in lista_simboluri_echipamente_TVCI:
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



# creez df_TVCI_equipments_with_attributes in care am toate echipamentele din fisierul exportat din autocad combinate cu baza de date
# pentru toate echipamentele din fisierul df_TVCI_dwg avem si coloanele din baza de date
df_TVCI_equipments_with_attributes = pd.DataFrame(pd.merge(df_TVCI_dwg, df_db_TVCI, on='COD_ECHIPAMENT'))
# creez variabila filt_cameras in care fac sortarea pe coloana rezolutie astfel incat in data frame df_total_cameras_per_recorder
# sa am doar camere, nimic altceva
filt_cameras = (df_TVCI_equipments_with_attributes['Rezolutie_MP'] > 0)
# df_total_cameras_per_recorder = df_TVCI_equipments_with_attributes[['DVR_NVR', 'Cantitate']].groupby(['DVR_NVR']).count()
# aplic filtrul la df_TVCI_equipments_with_attributes si scot numarul de camere pt fiecare DVR in parte
df_total_cameras_per_recorder = pd.DataFrame(
    df_TVCI_equipments_with_attributes.loc[filt_cameras, ['DVR_NVR', 'Cantitate']]).groupby(['DVR_NVR']).count()
# def create_and_add_hdd_to_qty_table(filt):

read_DVR_NVR = list(df_TVCI_equipments_with_attributes["DVR_NVR"].dropna())
list_DVR_NVR_labels = []
for item in read_DVR_NVR:
    if item not in list_DVR_NVR_labels:
        list_DVR_NVR_labels.append(item)
        list_DVR_NVR_labels.sort()
print(list_DVR_NVR_labels)
# filt_UPS = (df_TVCI_equipments_with_attributes['Putere_UPS_VoltAmp'] > 0)
# df_consum_per_UPS = pd.DataFrame(df_TVCI_equipments_with_attributes.loc[filt_UPS,['SIMBOL_ECHIPAMENT', 'Cantitate']])
# df_consum_per_UPS['SIMBOL_ECHIPAMENT']
# list_of_UPS_labels = list(df_consum_per_UPS['SIMBOL_ECHIPAMENT'])
# list_of_UPS_labels.sort()

filt_UPS = df_TVCI_equipments_with_attributes['SWITCH_SURSA_ALIMENTARE'].dropna().str.contains('UPS')
df_consum_per_UPS = pd.DataFrame(
    df_TVCI_equipments_with_attributes.dropna(axis='index', how='all', subset=['SWITCH_SURSA_ALIMENTARE']).loc[
        filt_UPS, ['SWITCH_SURSA_ALIMENTARE', 'Cantitate']])
#df_consum_per_UPS
list_of_UPS = list(df_consum_per_UPS['SWITCH_SURSA_ALIMENTARE'])
list_of_UPS_labels = []
for item in list_of_UPS:
    if item not in list_of_UPS_labels:
        list_of_UPS_labels.append(item)
        list_of_UPS_labels.sort()
#list_of_UPS_labels

# definim o lista goala in care vom introduce dictionarele ce vor contine calculele HDD-urilor pt fiecare NVR
lista_dictionare_calcule_HDD = []


def hdd_calculation_and_add_in_equipments_list():
    #definim o lista goala in care vom introduce dictionarele ce vor contine HDD-urile calculate
    lista_dictionare_HDD = []
    df_HDD_calculate = pd.DataFrame(columns=['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate', 'Producător',
                                                        'Furnizor', 'Document_însoțitor'])



    #verificam daca nu avem camere asociate la DVR/NVR. Daca nu avem, intrerupem executia si afisam o atentionare
    for i in range(len(list_DVR_NVR_labels)):
        try:
            nr_camere_per_DVR = df_total_cameras_per_recorder.iloc[i, 0]
        except IndexError:
            print('''Nu aveti camere asociate la NVR/DVR. Nu se va efectua calculul pentru capacitatea HDD-ului.
Asociati camere la NVR/DVR dupa care executati din nou programul!''')
            break
        nr_frame = 6
        nr_zile_de_inregistrare = 20
        nr_ore_de_inregistrare = 24
        spatiu_ocupat_1280x720 = 0.0927
        spatiu_ocupat_1920x1080 = 0.20857
        spatiu_stocare = spatiu_ocupat_1280x720 * nr_camere_per_DVR * nr_frame * nr_zile_de_inregistrare * nr_ore_de_inregistrare

        # creeez variabilele la care voi atribui valorile ce se vor afisa sub calculele pentru capacitatea HDD-urilor
        TVCI_recorder_label = f'{list_DVR_NVR_labels[i]}'
        TVCI_nr_camere_recorder = f'{nr_camere_per_DVR}'
        TVCI_nr_frame = f'{nr_frame}'
        TVCI_rezolutie_720P = f'{spatiu_ocupat_1280x720:.4f}'
        TVCI_nr_zile_inregistrare = f'{nr_zile_de_inregistrare}'
        TVCI_nr_ore_inregistrare = f'{nr_ore_de_inregistrare}'
        TVCI_spatiu_stocare = f'{spatiu_stocare:.2f}'


        if spatiu_stocare < 2000:
            # cream variabila filt pentru a face verificarea cu baza de date pt codul de HDD
            # !!!! Atentie!!! Daca codul de HDD este schimbat sau sters din baza de date, HDD-ul nu va mai fi alocat la lista de cantitati
            filt = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD20PURX')
            # creem data frame-ul df_HDD pentru HDD-ul al carui cod a fost verificat mai sus
            df_HDD = pd.DataFrame(df_db_TVCI.loc[filt, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate', 'Producător',
                                                        'Furnizor', 'Document_însoțitor']])
            #convertim data frame df_HDD in dictionar de tipul [{column -> value}, … , {column -> value}] (lista dictionare)
            dict_df_hdd = df_HDD.to_dict(orient = 'records')
            copy_of_dict_df_hdd = dict_df_hdd.copy()
            lista_dictionare_HDD.append(copy_of_dict_df_hdd)

            # creez o variabila ce contine capacitatea in GB a HDD-ului calculat
            fitru_HDD = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD20PURX')
            df_capacitate_HDD = df_db_TVCI.loc[fitru_HDD, ['Capacitate_HDD']]
            capacitate_HDD = str(int(df_capacitate_HDD.iloc[0, 0]))
            #print(capacitate_HDD )
            TVCI_capacitate_HDD = capacitate_HDD

            dict_TVCI_calcule_HDD = {}
            dict_TVCI_calcule_HDD.update({'TVCI_denumire_NVR' + str(i) : TVCI_recorder_label,
                                          'TVCI_nr_camere_recorder' + str(i) : TVCI_nr_camere_recorder,
                                          'TVCI_nr_frame' + str(i) : TVCI_nr_frame,
                                          'TVCI_nr_zile_inreg' + str(i) : TVCI_nr_zile_inregistrare,
                                          'TVCI_rezolutie' + str(i) : TVCI_rezolutie_720P,
                                          'TVCI_nr_ore_inreg' + str(i) : TVCI_nr_ore_inregistrare,
                                          'TVCI_spatiu_stocare' + str(i) : TVCI_spatiu_stocare,
                                          'TVCI_capacitate_HDD' + str(i) : TVCI_capacitate_HDD})
            lista_dictionare_calcule_HDD.append(dict_TVCI_calcule_HDD)

#             print(f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
# {spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB')

        else:
            if spatiu_stocare < 4000:
                filt = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD40PURX')
                df_HDD = pd.DataFrame(df_db_TVCI.loc[
                                          filt, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate', 'Producător',
                                                 'Furnizor', 'Document_însoțitor']])
                dict_df_hdd = df_HDD.to_dict(orient='records')
                copy_of_dict_df_hdd = dict_df_hdd.copy()
                lista_dictionare_HDD.append(copy_of_dict_df_hdd)

                # creez o variabila ce contine capacitatea in GB a HDD-ului calculat
                fitru_HDD = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD40PURX')
                df_capacitate_HDD = df_db_TVCI.loc[fitru_HDD, ['Capacitate_HDD']]
                capacitate_HDD = str(int(df_capacitate_HDD.iloc[0, 0]))
                # print(capacitate_HDD )
                TVCI_capacitate_HDD = capacitate_HDD

                dict_TVCI_calcule_HDD = {}
                dict_TVCI_calcule_HDD.update({'TVCI_denumire_NVR' + str(i): TVCI_recorder_label,
                                              'TVCI_nr_camere_recorder' + str(i): TVCI_nr_camere_recorder,
                                              'TVCI_nr_frame' + str(i): TVCI_nr_frame,
                                              'TVCI_nr_zile_inreg' + str(i): TVCI_nr_zile_inregistrare,
                                              'TVCI_rezolutie' + str(i): TVCI_rezolutie_720P,
                                              'TVCI_nr_ore_inreg' + str(i): TVCI_nr_ore_inregistrare,
                                              'TVCI_spatiu_stocare' + str(i): TVCI_spatiu_stocare,
                                              'TVCI_capacitate_HDD' + str(i): TVCI_capacitate_HDD})
                lista_dictionare_calcule_HDD.append(dict_TVCI_calcule_HDD)

#                 print(f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
# {spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB')

            else:
                if spatiu_stocare < 6000:
                    filt = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD60PURX')
                    df_HDD = pd.DataFrame(df_db_TVCI.loc[
                                              filt, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate', 'Producător',
                                                     'Furnizor', 'Document_însoțitor']])
                    dict_df_hdd = df_HDD.to_dict(orient = 'records')
                    copy_of_dict_df_hdd = dict_df_hdd.copy()
                    lista_dictionare_HDD.append(copy_of_dict_df_hdd)

                    # creez o variabila ce contine capacitatea in GB a HDD-ului calculat
                    fitru_HDD = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD60PURX')
                    df_capacitate_HDD = df_db_TVCI.loc[fitru_HDD, ['Capacitate_HDD']]
                    capacitate_HDD = str(int(df_capacitate_HDD.iloc[0, 0]))
                    # print(capacitate_HDD )
                    TVCI_capacitate_HDD = capacitate_HDD

                    dict_TVCI_calcule_HDD = {}
                    dict_TVCI_calcule_HDD.update({'TVCI_denumire_NVR' + str(i): TVCI_recorder_label,
                                                  'TVCI_nr_camere_recorder' + str(i): TVCI_nr_camere_recorder,
                                                  'TVCI_nr_frame' + str(i): TVCI_nr_frame,
                                                  'TVCI_nr_zile_inreg' + str(i): TVCI_nr_zile_inregistrare,
                                                  'TVCI_rezolutie' + str(i): TVCI_rezolutie_720P,
                                                  'TVCI_nr_ore_inreg' + str(i): TVCI_nr_ore_inregistrare,
                                                  'TVCI_spatiu_stocare' + str(i): TVCI_spatiu_stocare,
                                                  'TVCI_capacitate_HDD' + str(i): TVCI_capacitate_HDD})
                    lista_dictionare_calcule_HDD.append(dict_TVCI_calcule_HDD)


#                     print(f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
# {spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB')

                else:
                    if spatiu_stocare < 8000:
                        # trebuie creat dictionar pt hard disk de 2TB
                        # trebuie apelata functia care adauga hard disk-ul la lista de cantitati
                        filt = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD80PURX')
                        df_HDD = pd.DataFrame(df_db_TVCI.loc[filt, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate',
                                                                    'Producător', 'Furnizor', 'Document_însoțitor']])
                        dict_df_hdd = df_HDD.to_dict(orient='records')
                        copy_of_dict_df_hdd = dict_df_hdd.copy()
                        lista_dictionare_HDD.append(copy_of_dict_df_hdd)

                        # creez o variabila ce contine capacitatea in GB a HDD-ului calculat
                        fitru_HDD = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD80PURX')
                        df_capacitate_HDD = df_db_TVCI.loc[fitru_HDD, ['Capacitate_HDD']]
                        capacitate_HDD = str(int(df_capacitate_HDD.iloc[0, 0]))
                        # print(capacitate_HDD )
                        TVCI_capacitate_HDD = capacitate_HDD

                        dict_TVCI_calcule_HDD = {}
                        dict_TVCI_calcule_HDD.update({'TVCI_denumire_NVR' + str(i): TVCI_recorder_label,
                                                      'TVCI_nr_camere_recorder' + str(i): TVCI_nr_camere_recorder,
                                                      'TVCI_nr_frame' + str(i): TVCI_nr_frame,
                                                      'TVCI_nr_zile_inreg' + str(i): TVCI_nr_zile_inregistrare,
                                                      'TVCI_rezolutie' + str(i): TVCI_rezolutie_720P,
                                                      'TVCI_nr_ore_inreg' + str(i): TVCI_nr_ore_inregistrare,
                                                      'TVCI_spatiu_stocare' + str(i): TVCI_spatiu_stocare,
                                                      'TVCI_capacitate_HDD' + str(i): TVCI_capacitate_HDD})
                        lista_dictionare_calcule_HDD.append(dict_TVCI_calcule_HDD)


#                         print(f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
# {spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB')

                    else:
                        if spatiu_stocare < 10000:
                            filt = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD100PURZ')

                            df_HDD = pd.DataFrame(df_db_TVCI.loc[
                                                      filt, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate',
                                                             'Producător', 'Furnizor', 'Document_însoțitor']])
                            dict_df_hdd = df_HDD.to_dict(orient='records')
                            copy_of_dict_df_hdd = dict_df_hdd.copy()
                            lista_dictionare_HDD.append(copy_of_dict_df_hdd)

                        # creez o variabila ce contine capacitatea in GB a HDD-ului calculat
                        fitru_HDD = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD100PURZ')
                        df_capacitate_HDD = df_db_TVCI.loc[fitru_HDD, ['Capacitate_HDD']]
                        capacitate_HDD = str(int(df_capacitate_HDD.iloc[0, 0]))
                        # print(capacitate_HDD )
                        TVCI_capacitate_HDD = capacitate_HDD

                        dict_TVCI_calcule_HDD = {}
                        dict_TVCI_calcule_HDD.update({'TVCI_denumire_NVR' + str(i): TVCI_recorder_label,
                                                      'TVCI_nr_camere_recorder' + str(i): TVCI_nr_camere_recorder,
                                                      'TVCI_nr_frame' + str(i): TVCI_nr_frame,
                                                      'TVCI_nr_zile_inreg' + str(i): TVCI_nr_zile_inregistrare,
                                                      'TVCI_rezolutie' + str(i): TVCI_rezolutie_720P,
                                                      'TVCI_nr_ore_inreg' + str(i): TVCI_nr_ore_inregistrare,
                                                      'TVCI_spatiu_stocare' + str(i): TVCI_spatiu_stocare,
                                                      'TVCI_capacitate_HDD' + str(i): TVCI_capacitate_HDD})
                        lista_dictionare_calcule_HDD.append(dict_TVCI_calcule_HDD)


#                            print(
#                                f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
#{spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB')

                    continue
    return lista_dictionare_HDD
#hdd_calculation_and_add_in_equipments_list()


#functia calcule_HDD_TVCI() aduce lista de dictionare lista_dictionare_calcule_HDD, o salveaza in variabila lista_calcule_HDD_TVCI si
# o retuneaza pentru a fi utilizata in modulul main pentru a scrie calculele HDD-urilor pt fiecare NVR TVCI.
def calcule_HDD_TVCI():
    lista_calcule_HDD_TVCI = lista_dictionare_calcule_HDD
    return lista_calcule_HDD_TVCI





#functia hdd_calculation_and_add_in_equipments_list() returneaza o lista de liste de dictionare, dictionarele continand valorile
#HDD-urilor reiesite din calcule
#apelam functia hdd_calculation_and_add_in_equipments_list() prin atribuirea acesteia la variabila lista_hdd_calculate
#variabila va fi egala cu lista de liste de dictionare returnate de functie
lista_hdd_calculate = hdd_calculation_and_add_in_equipments_list()

#pentru a putea crea dataframe, avem nevoie ca lista_hdd_calculate sa fie o lista de dictionare, nu o lista de liste de dictionare
#pentru a avea ca rezultat o lista de dictionare dintr-o lista de liste de dictionare, folosim nested for de mai jos
# flatten_matrix = []
# for sublist in lista_hdd_calculate:
#     for val in sublist:
#         flatten_matrix.append(val)

#print(flatten_matrix)
#dataframe df_hdd_calculate se va adauga in functia de calcul a listei de cantitati echipamente TVCI
# df_hdd_calculate = pd.DataFrame(flatten_matrix)
# print(df_hdd_calculate)

if __name__ == '__main__':
    calcule_HDD_TVCI()