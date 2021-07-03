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

# filt_UPS = (df_TVCI_equipments_with_attributes['Putere_UPS_VoltAmp'] > 0)
# df_consum_per_UPS = pd.DataFrame(df_TVCI_equipments_with_attributes.loc[filt_UPS,['SIMBOL_ECHIPAMENT', 'Cantitate']])
# df_consum_per_UPS['SIMBOL_ECHIPAMENT']
# list_of_UPS_labels = list(df_consum_per_UPS['SIMBOL_ECHIPAMENT'])
# list_of_UPS_labels.sort()

filt_UPS = df_TVCI_equipments_with_attributes['SWITCH_SURSA_ALIMENTARE'].dropna().str.contains('UPS')
df_consum_per_UPS = pd.DataFrame(
    df_TVCI_equipments_with_attributes.dropna(axis='index', how='all', subset=['SWITCH_SURSA_ALIMENTARE']).loc[
        filt_UPS, ['SWITCH_SURSA_ALIMENTARE', 'Cantitate']])
df_consum_per_UPS
list_of_UPS = list(df_consum_per_UPS['SWITCH_SURSA_ALIMENTARE'])
list_of_UPS_labels = []
for item in list_of_UPS:
    if item not in list_of_UPS_labels:
        list_of_UPS_labels.append(item)
        list_of_UPS_labels.sort()
list_of_UPS_labels

writer = pd.ExcelWriter('C:\\Users\\alexa\\Desktop\\TVCI.xlsx', engine='xlsxwriter')
workbook = writer.book
worksheet = workbook.add_worksheet('Consum curent')
writer.sheets['Consum curent'] = worksheet


# afisate tabel de descriere a zonelor protejate subsistem televiziune cu circuit închis
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
    df_keep_only_cameras.rename(
        columns={'SIMBOL_ECHIPAMENT': 'Simbol echipament', 'Denumire_element': 'Denumire element',
                 'COD_ECHIPAMENT': 'Cod echipament', 'Modul_de_programare': 'Modul de programare',
                 'SPATIUL_SUPRAVEGHEAT': 'Spațiul supravegheat'}, inplace=True)
    df_keep_only_cameras.to_excel(writer, sheet_name='Amplasare camere', index=True)
    return df_keep_only_cameras


TVCI_camera_labels()


def hdd_calculation_and_add_in_equipments_list():
    #     definim df_TVCI_equipments_with_attributes ca fiind variabila globala
    global df_TVCI_equipments_with_attributes
    #     creem workbook si worksheet penru a putea sa scriem textul cu calculele HDD-urilor in sheet-ul Calcul HDD
    workbook = writer.book
    worksheet = workbook.add_worksheet('Calcul HDD')
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
        spatiu_stocare = spatiu_ocupat_1920x1080 * nr_camere_per_DVR * nr_frame * nr_zile_de_inregistrare * nr_ore_de_inregistrare

        if spatiu_stocare < 2000:
            # cream variabila filt pentru a face verificarea cu baza de date pt codul de HDD
            # !!!! Atentie!!! Daca codul de HDD este schimbat sau sters din baza de date, HDD-ul nu va mai fi alocat la lista de cantitati
            filt = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD20PURX')
            # creem data frame-ul df_HDD pentru HDD-ul al carui cod a fost verificat mai sus
            df_HDD = pd.DataFrame(df_db_TVCI.loc[filt, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate', 'Producător',
                                                        'Furnizor', 'Document_însoțitor']])
            # adaugam in variablia globala df_TVCI_equipments_with_attributes linia aferenta HDD-ului pentru care s-a creat data frame-ul df_HDD
            df_TVCI_equipments_with_attributes = df_TVCI_equipments_with_attributes.append(df_HDD, ignore_index=True)
            # afisam ce valori s-au calculat si pt ce DVR
            text = (f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
{spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB.\
 {list_DVR_NVR_labels[i]} va fi echipat cu un HDD ce are o capacitate de 2000 Gb. Acesta asigură o perioadă de arhivare de cel puțin de 20 zile conform normelor în vigoare. Se recomandă ca înregistratorul digital să fie setat, astfel încât fiecare cameră să înregistreze la detecție mișcare(motion detection).')
            #                 scriem in fisierul exportat in sheet 'Calcul HDD'
            worksheet.write(i, 0, text)
            print(f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
{spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB')

        else:
            if spatiu_stocare < 4000:
                # trebuie creat dictionar pt hard disk de 2TB
                # trebuie apelata functia care adauga hard disk-ul la lista de cantitati
                filt = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD40PURX')
                df_HDD = pd.DataFrame(df_db_TVCI.loc[
                                          filt, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate', 'Producător',
                                                 'Furnizor', 'Document_însoțitor']])
                df_TVCI_equipments_with_attributes = df_TVCI_equipments_with_attributes.append(df_HDD,
                                                                                               ignore_index=True)  # create_and_add_hdd_to_qty_table(filt)
                # creez variablia text pentru a printa
                text = (f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
{spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB.\
 {list_DVR_NVR_labels[i]} va fi echipat cu un HDD ce are o capacitate de 4000 Gb. Acesta asigură o perioadă de arhivare de cel puțin de 20 zile conform normelor în vigoare. Se recomandă ca înregistratorul digital să fie setat, astfel încât fiecare cameră să înregistreze la detecție mișcare(motion detection).')
                worksheet.write(i, 0, text)
                print(f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
{spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB')

            else:
                if spatiu_stocare < 6000:
                    # trebuie creat dictionar pt hard disk de 2TB
                    # trebuie apelata functia care adauga hard disk-ul la lista de cantitati
                    filt = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD60PURX')
                    df_HDD = pd.DataFrame(df_db_TVCI.loc[
                                              filt, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate', 'Producător',
                                                     'Furnizor', 'Document_însoțitor']])
                    df_TVCI_equipments_with_attributes = df_TVCI_equipments_with_attributes.append(df_HDD,
                                                                                                   ignore_index=True)
                    text = (f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
{spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB.\
 {list_DVR_NVR_labels[i]} va fi echipat cu un HDD ce are o capacitate de 6000 Gb. Acesta asigură o perioadă de arhivare de cel puțin de 20 zile conform normelor în vigoare. Se recomandă ca înregistratorul digital să fie setat, astfel încât fiecare cameră să înregistreze la detecție mișcare(motion detection).')
                    worksheet.write(i, 0, text)
                    print(f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
{spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB')

                else:
                    if spatiu_stocare < 8000:
                        # trebuie creat dictionar pt hard disk de 2TB
                        # trebuie apelata functia care adauga hard disk-ul la lista de cantitati
                        filt = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD80PURX')
                        df_HDD = pd.DataFrame(df_db_TVCI.loc[filt, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate',
                                                                    'Producător', 'Furnizor', 'Document_însoțitor']])
                        df_TVCI_equipments_with_attributes = df_TVCI_equipments_with_attributes.append(df_HDD,
                                                                                                       ignore_index=True)
                        text = (
                            f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
{spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB.\
 {list_DVR_NVR_labels[i]} va fi echipat cu un HDD ce are o capacitate de 8000 Gb. Acesta asigură o perioadă de arhivare de cel puțin de 20 zile conform normelor în vigoare. Se recomandă ca înregistratorul digital să fie setat, astfel încât fiecare cameră să înregistreze la detecție mișcare(motion detection).')
                        worksheet.write(i, 0, text)
                        print(f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
{spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB')

                    else:
                        if spatiu_stocare < 10000:
                            # trebuie creat dictionar pt hard disk de 2TB
                            # trebuie apelata functia care adauga hard disk-ul la lista de cantitati
                            filt = (df_db_TVCI['COD_ECHIPAMENT'] == 'WD100PURX')
                            df_HDD = pd.DataFrame(df_db_TVCI.loc[
                                                      filt, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate',
                                                             'Producător', 'Furnizor', 'Document_însoțitor']])
                            df_TVCI_equipments_with_attributes = df_TVCI_equipments_with_attributes.append(df_HDD,
                                                                                                           ignore_index=True)
                            text = (
                                f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
{spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB.\
 {list_DVR_NVR_labels[i]} va fi echipat cu un HDD ce are o capacitate de 10000 Gb. Acesta asigură o perioadă de arhivare de cel puțin de 20 zile conform normelor în vigoare. Se recomandă ca înregistratorul digital să fie setat, astfel încât fiecare cameră să înregistreze la detecție mișcare(motion detection).')
                            worksheet.write(i, 0, text)
                            print(
                                f'Pentru {list_DVR_NVR_labels[i]} cu {nr_camere_per_DVR} camere video setate la {nr_frame} fps, în 20 zile, rezultă un volum de date de: \
{spatiu_ocupat_1280x720:.4f} x {nr_camere_per_DVR} x {nr_frame} x {nr_zile_de_inregistrare} x {nr_ore_de_inregistrare} = {spatiu_stocare:.2f} GB')

                    continue


hdd_calculation_and_add_in_equipments_list()


def add_video_balun_to_list_of_qty():
    global df_TVCI_equipments_with_attributes
    # bazat pe codurile camerelor exportate din dwg filtrez camerele analogice
    filt_analog_cameras = (df_TVCI_equipments_with_attributes['Tehnologie'] == 'ANALOG')
    # creez dataframe-ul cu camerele analogice
    df_analog_cameras = pd.DataFrame(df_TVCI_equipments_with_attributes.loc[filt_analog_cameras,
                                                                            ['SIMBOL_ECHIPAMENT',
                                                                             'Cantitate',
                                                                             'COD_ECHIPAMENT',
                                                                             'Nr. Crt']]).sort_values(by='Nr. Crt',
                                                                                                      ascending=True)
    # creez o variabila in care stochez numarul total de camere analogice
    no_of_analog_cameras = df_analog_cameras['Cantitate'].count()
    while no_of_analog_cameras == 0:
        break
    else:
        # creez o noua variabila in care stochez numarul de video balun-uri ce vor trebui adaugate in lista de cantitati
        no_of_video_balun = no_of_analog_cameras
        no_of_video_balun
        # creez o variabila cu ajutorul careia selectez(in baza codului de produs definit aici) din baza de date video balun-ul
        filt_video_balun = (df_db_TVCI['COD_ECHIPAMENT'] == 'DS-1H18S')
        # creez un dataframe cu video balunul selectat in linia de mai sus
        df_video_balun = pd.DataFrame(df_db_TVCI.loc[
                                          filt_video_balun, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate',
                                                             'Producător', 'Furnizor', 'Document_însoțitor']])
        # setez cantitatea de video balun-uri ce vo trebui adaugate in lista de echipamente
        df_video_balun['Cantitate'] = no_of_video_balun
        # adaug video balun-urile in df_TVCI_equipments_with_attributes care sta la baza altgoritmului de creare a listei de cantitati
        df_TVCI_equipments_with_attributes = df_TVCI_equipments_with_attributes.append(df_video_balun,
                                                                                       ignore_index=True)


add_video_balun_to_list_of_qty()


def crt_consumption_table(i):
    # creez variabila filt_using_UPS_label prin care filtrez din df_TVCI_equipments_with_attributes elementele care au atribuite
    # simbolul aferent list_of_UPS_labels[i]
    filt_using_UPS_label = (df_TVCI_equipments_with_attributes['SWITCH_SURSA_ALIMENTARE'] == list_of_UPS_labels[i])
    # creez un data frame pt tabelul cu cosumatorii de pe UPS-ul respectiv si il sortez in fct de nr crt din baza de date
    df_UPS_consum_table = pd.DataFrame(df_TVCI_equipments_with_attributes.loc[filt_using_UPS_label,
                                                                              ['SIMBOL_ECHIPAMENT', 'Denumire_element',
                                                                               'COD_ECHIPAMENT', 'Cantitate',
                                                                               'Consum/buc.(W)',
                                                                               'Nr. Crt']]).sort_values(by='Nr. Crt',
                                                                                                        ascending=True)
    # creez dataframe cu coloanele de care sunt interesat sa le afisez la final
    df_UPS_consum_table = df_UPS_consum_table[
        ['SIMBOL_ECHIPAMENT', 'Denumire_element', 'COD_ECHIPAMENT', 'Cantitate', 'Consum/buc.(W)']]
    df_UPS_consum_table.sort_values(by='SIMBOL_ECHIPAMENT', ascending=True, inplace=True)
    # creez coloana 'Consum total (W)' la df_UPS_consum_table
    df_UPS_consum_table['Consum total (W)'] = df_UPS_consum_table['Cantitate'] * df_UPS_consum_table['Consum/buc.(W)']
    # resetez index-ul
    df_UPS_consum_table.reset_index(drop=True, inplace=True)
    # setez index-ul sa inceapa de la 1
    df_UPS_consum_table.index = df_UPS_consum_table.index + 1
    # redenumesc coloanele
    df_UPS_consum_table.rename(columns={'SIMBOL_ECHIPAMENT': 'Simbol echipament',
                                        'Denumire_element': 'Denumire echipament',
                                        'COD_ECHIPAMENT': 'Cod echipament'}, inplace=True)
    # creez o serie pe care o denumesc Total si care este egala cu suma coloanei 'Consum total (W)'
    Total = df_UPS_consum_table['Consum total (W)'].sum()
    # setez 'Total' ca index pt linia de Total si pentru toate coloanele vom avea NaN doar pentru coloana 'Consum total (W)' vom avea totalul
    df_UPS_consum_table.loc['Total'] = pd.Series(df_UPS_consum_table['Consum total (W)'].sum(),
                                                 index=['Consum total (W)'])
    # pt ca functia sa poata returna un data frame creez acest data frame
    df_UPS_consum_table = pd.DataFrame(df_UPS_consum_table)
    return df_UPS_consum_table


'''
aceasta functie creeaza o variabila de verificare, care in baza valorii total_consumption_VA alege un UPS din baza de date a 
carui putere este mai mare sau egala cu puterea calculata(total_consumption_VA) dupa care il adaug UPS-ul selectat se va 
adauga la lista de cantitati TVCI

'''


def choose_UPS_from_db_TVCI(total_consumption_VA):
    global df_TVCI_equipments_with_attributes
    list_of_ups_values = list(df_db_TVCI['Putere_UPS_VoltAmp'])
    for item in list_of_ups_values:
        if item >= total_consumption_VA:
            total_consumption_VA = item
            break
    filt_UPS = (df_db_TVCI['Putere_UPS_VoltAmp'] == total_consumption_VA)
    df_UPS = df_db_TVCI.loc[
        filt_UPS, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate', 'Producător', 'Furnizor', 'Document_însoțitor']]
    df_TVCI_equipments_with_attributes = df_TVCI_equipments_with_attributes.append(df_UPS, ignore_index=True)


'''
aceasta functie scrie in excelul atasat in sheet-ul 'Consum curent' tabelele cu consumatorii pentru fiecare UPS in parte
totodata aici se fac calculele pentru puterea UPS-urilor si bazat pe variabila total_consumption_VA prin apelarea
functiei choose_UPS_from_db_TVCI(total_consumption_VA) se alege UPS-ul/UPS-urile ce se vor introduce in lista de cantitati
din baza de date

'''


def write_consumption_tables_in_excel():
    for i in range(len(list_of_UPS_labels)):
        # creez variabila total_consumption pt a scoate din functia crt_consumption_table() valoarea consumului pt un UPS.
        # Imi este necesar pt a calcula puterea UPS-ului in Volt Amperi
        total_consumption = crt_consumption_table(i).loc['Total', 'Consum total (W)']
        # formula de calcul pentru a calcula puterea UPS-ului in Volt Amperi
        total_consumption_VA = total_consumption / 0.55
        # apelez functia care introduce UPS-ul in lista de cantitati
        choose_UPS_from_db_TVCI(total_consumption_VA)
        # urmatoarea conditie If Else scrie tabelele de consum in sheet-ul 'Consum curent' din excel si sub fiecare tabel afiseaza informatia
        # cu privire la puterea calculata in Volt Amperi pe care UPS-ul o va avea
        # incepem prin a scrie de pe linia 0 se vor scrie succesiv toate tabelele cu 1 linie libera intre ele
        if i == 0:
            crt_consumption_table(i).to_excel(writer, sheet_name='Consum curent', startrow=0, startcol=0, index=True)
            text_UPS = (f' Consumul energetic al subsistemului de televiziune cu circuit închis ce este alimentat prin \
    {list_of_UPS_labels[i]} este {total_consumption:.2f}W.\
     Echipamentele UPS au puterea exprimată în Volt-Amperi(VA). Relaţia dintre puterea reală (W) şi cea aparentă (VA) \
    este dată de formula  KVA = KW/PF  unde, PF – defazajul dintre cele 2 puteri sau factorul de putere. În mod normal,\
     PF este considerat 0,55.\
     Prin urmare rezultă:\
        PUPS = {total_consumption:.2f}/0,55 => PUPS = {total_consumption_VA:.2f}VA')
            # setez linia de scriere pentru infomrtiile cu privire la UPS in fct de nr liniilor din tabelul creat + 1
            # shape() afiseaza nr de linii si nr de coloane din tabel sub forma de tuple. Daca indexam tuplul[0] obtinem nr de linii din tabel
            write_starting_row = crt_consumption_table(i).shape[0] + 1
            worksheet.write(write_starting_row, 0, text_UPS)
            write_starting_row += 2
            # print(write_starting_row)
        else:
            crt_consumption_table(i).to_excel(writer, sheet_name='Consum curent', startrow=write_starting_row,
                                              startcol=0, index=True)
            text_UPS = (f' Consumul energetic al subsistemului de televiziune cu circuit închis ce este alimentat prin\
    {list_of_UPS_labels[i]} este {total_consumption:.2f}W.\
     Echipamentele UPS au puterea exprimată în Volt-Amperi(VA). Relaţia dintre puterea reală (W) şi cea aparentă (VA) \
    este dată de formula  KVA = KW/PF  unde, PF – defazajul dintre cele 2 puteri sau factorul de putere. În mod normal,\
     PF este considerat 0,55.\
     Prin urmare rezultă:\
        PUPS = {total_consumption:.2f}/0,55 => PUPS = {total_consumption_VA:.2f}VA')
            write_starting_row = write_starting_row + crt_consumption_table(i).shape[0] + 1
            worksheet.write(write_starting_row, 0, text_UPS)
            write_starting_row = write_starting_row + 2

    # trebuie sa returnez din aceasta functie total_consumption_VA pt a alege un UPS din baza de date


write_consumption_tables_in_excel()


# functia jurnal_cabluri_TVCI se apeleaza in functia TVCI_equipment_qty_table
def jurnal_cabluri_TVCI(video_balun_code, cable_type_video):
    df_TVCI_equipments_with_attributes = pd.DataFrame(pd.merge(df_TVCI_dwg, df_db_TVCI, on='COD_ECHIPAMENT'))
    # setezca index coloana SIMBOL_ECHIPAMENT din df_TVCI_equipments_with_attributes
    df_TVCI_equipments_with_attributes.sort_values(by=['SIMBOL_ECHIPAMENT'], inplace=True)
    df_TVCI_equipments_with_attributes.index = df_TVCI_equipments_with_attributes.SIMBOL_ECHIPAMENT
    df_TVCI_equipments_with_attributes

    # cream serie de la
    serie_de_la_camere = df_TVCI_equipments_with_attributes['SIMBOL_ECHIPAMENT']
    serie_de_la_camere

    # cream seria pana la
    # serie_de_la_map = df_TVCI_equipments_with_attributes['SIMBOL_ECHIPAMENT']
    def serie_pana_la_map(x):
        if x == 0:
            return ('-')
        elif x != 0:
            return (x)
            # print(df_TVCI_equipments_with_attributes['DVR_NVR'])

    serie_pana_la = df_TVCI_equipments_with_attributes['DVR_NVR'].fillna(0)
    serie_pana_la = serie_pana_la.map(serie_pana_la_map)
    serie_pana_la

    # cream seria prin
    def prin_video_map(x):
        if df_TVCI_equipments_with_attributes.loc[x, ['Tehnologie']][0] == 'ANALOG':
            if (('utp') or ('ftp')) in cable_type_video.lower():
                return (video_balun_code)
            else:
                return ('-')
        elif df_TVCI_equipments_with_attributes.loc[x, ['Tehnologie']][0] == 'IP':
            return (df_TVCI_equipments_with_attributes.loc[x, ['SWITCH_SURSA_ALIMENTARE']][0])

    serie_prin = df_TVCI_equipments_with_attributes['SIMBOL_ECHIPAMENT'].map(prin_video_map)
    serie_prin = serie_prin.fillna(0)
    serie_prin.replace(0, '-', inplace=True)
    serie_prin

    # cream seria tip_cablu_video
    def tip_cablu_video(x):
        if df_TVCI_equipments_with_attributes.loc[x, ['Tehnologie']][0] == 'ANALOG':
            return (cable_type_video)

        elif df_TVCI_equipments_with_attributes.loc[x, ['Tehnologie']][0] == 'IP':
            return (cable_type_video)

        elif 'mon' in x.lower():
            return ('VGA')

    serie_tip_cablu_video = df_TVCI_equipments_with_attributes['SIMBOL_ECHIPAMENT'].map(tip_cablu_video)
    serie_tip_cablu_video = serie_tip_cablu_video.fillna(0)
    serie_tip_cablu_video.replace(0, '-', inplace=True)
    serie_tip_cablu_video

    # cream seria pana la alimentare
    def pana_la_alimentare(x):
        if df_TVCI_equipments_with_attributes.loc[x, ['Tehnologie']][0] == 'ANALOG':
            return (df_TVCI_equipments_with_attributes.loc[x, ['SWITCH_SURSA_ALIMENTARE']][0])

        elif df_TVCI_equipments_with_attributes.loc[x, ['Tehnologie']][0] == 'IP':
            return (df_TVCI_equipments_with_attributes.loc[x, ['SWITCH_SURSA_ALIMENTARE']][0])

            # (df_TVCI_equipments_with_attributes['Consum/buc.(W)'] > 8) & (df_TVCI_equipments_with_attributes['Modul_de_programare'] != 'înregistrare la mişcare'))
        elif ((df_TVCI_equipments_with_attributes.loc[x, ['Consum/buc.(W)']][0]) > 0) & (
        (df_TVCI_equipments_with_attributes.loc[x, ['Modul_de_programare']][0] != 'înregistrare la mişcare')):
            return (df_TVCI_equipments_with_attributes.loc[x, ['SWITCH_SURSA_ALIMENTARE']][0])

    serie_pana_la_alimentare = df_TVCI_equipments_with_attributes['SIMBOL_ECHIPAMENT'].map(pana_la_alimentare)
    serie_pana_la_alimentare

    # cream seria tip_cablu_alimentare
    # Am setat manual sa returneze MYYM2x0,75 pana cand gasesc o solutie la tipul de cablu pt camere
    def tip_cablu_alimentare(x):
        if df_TVCI_equipments_with_attributes.loc[x, ['Tehnologie']][0] == 'ANALOG':
            item_sursa_alimentare = df_TVCI_equipments_with_attributes.loc[x, ['SWITCH_SURSA_ALIMENTARE']][0]
            # return(df_TVCI_equipments_with_attributes.loc[item_sursa_alimentare,['Cablu_alimentare']][0])
            return ('MYYM2x0,75')

        elif df_TVCI_equipments_with_attributes.loc[x, ['Tehnologie']][0] == 'IP':
            # item_sursa_alimentare = df_TVCI_equipments_with_attributes.loc[x,['SWITCH_SURSA_ALIMENTARE']][0]
            # return(df_TVCI_equipments_with_attributes.loc[item_sursa_alimentare,['Cablu_alimentare']][0])
            return (cable_type_video)

        elif ((df_TVCI_equipments_with_attributes.loc[x, ['Consum/buc.(W)']][0]) > 0) & (
        (df_TVCI_equipments_with_attributes.loc[x, ['Modul_de_programare']][0] != 'înregistrare la mişcare')):
            return (df_TVCI_equipments_with_attributes.loc[x, ['Cablu_alimentare']][0])

    serie_tip_cablu_alimentare = df_TVCI_equipments_with_attributes['SIMBOL_ECHIPAMENT'].map(tip_cablu_alimentare)
    serie_tip_cablu_alimentare

    # se creeaza dataframe-ul final cu toate seriile de mai sus care va reprezenta jurnalul de cabluri
    df_jurnal_cabluri_camere = pd.DataFrame({'De la': serie_de_la_camere.values,
                                             'Prin': serie_prin.values,
                                             'Pana la': serie_pana_la.values,
                                             'Tip cablu': serie_tip_cablu_video.values,
                                             'Pana la alimentare': serie_pana_la_alimentare.values,
                                             'Tip cablu alimentare': serie_tip_cablu_alimentare.values})
    # print(df_jurnal_cabluri_camere)
    df_jurnal_cabluri_camere.to_excel(writer, sheet_name='Jurnal cabluri', index=True)


def TVCI_equipment_qty_table():
    # df_TVCI_equipments_with_attributes = pd.DataFrame(pd.merge(df_TVCI_dwg, df_db_TVCI, on = 'COD_ECHIPAMENT'))
    # creez data frame df_TVCI_list_of_qty pt a grupa echipamentele in functie de 'COD_ECHIPAMENT' si facem count pt cantitate
    df_TVCI_list_of_qty = df_TVCI_equipments_with_attributes.groupby(['COD_ECHIPAMENT'])[['Cantitate']].sum()
    # combinam f_TVCI_list_of_qty cu baza de date pt a avea toate caracteristicile echipamentelor(adaugam toate coloanele din db)
    # !!!!!!de avut grija pentru ca odata cu combinarea df_TVCI_list_of_qty cu baza de date apare o noua coloana pt cantitate 'Cantitate_x'
    # odata cu combinarea dataframeurilor apare o noua coloana Cantitate_x pt ca avem cantitate atat in db cat si in frame-ul df_TVCI_list_of_qty
    # ne intereseaza cantitatile de pe coloana Cantitate_x
    df_TVCI_list_of_qty = pd.merge(df_TVCI_list_of_qty, df_db_TVCI, on='COD_ECHIPAMENT')
    # creem tabelul cu lista de cantitati, asa cum vrem sa fie afisata in dataframe/fisierul ce se va crea
    df_TVCI_list_of_qty[
        ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate_x', 'Producător', 'Furnizor', 'Document_însoțitor', ]]
    # creez un dataframe cu informatiile pe care vreau sa le export(tabelul de cantitati)
    df_TVCI_list_of_qty = pd.DataFrame(df_TVCI_list_of_qty[
                                           ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate_x', 'Producător',
                                            'Furnizor', 'Document_însoțitor', 'Nr. Crt']]).sort_values(by=['Nr. Crt'],
                                                                                                       ascending=True)
    df_TVCI_list_of_qty = pd.DataFrame(df_TVCI_list_of_qty[
                                           ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate_x', 'Producător',
                                            'Furnizor', 'Document_însoțitor']])

    # liniile de mai jos filtreaza cablul UTP din lista de cantitati si il returneaza
    # pt a fi utilizat in functia care creeaza jurnalul de cabluri
    #     filter_for_cable = df_TVCI_list_of_qty['COD_ECHIPAMENT'].str.contains('UTP')
    #     df_cable_type = df_TVCI_list_of_qty.loc[filter_for_cable,['COD_ECHIPAMENT']]
    #     if len(df_cable_type) > 0:
    #         #cable_type = df_cable_type.iloc[0,0]
    #         filter_for_video_balun = df_TVCI_list_of_qty['Denumire_element'].str.contains('Adaptor pasiv')
    #         df_for_video_balun = df_TVCI_list_of_qty.loc[filter_for_video_balun,['Denumire_element','COD_ECHIPAMENT']]
    #         #print(df_for_video_balun['COD_ECHIPAMENT'].iloc[0])
    #         cable_type = df_for_video_balun['COD_ECHIPAMENT'].iloc[0]
    #     else:
    #         #print('nimic')
    #         cable_type = 0
    # df_TVCI_list_of_qty.index = df_TVCI_list_of_qty['Denumire_element']
    # filt = df_TVCI_list_of_qty.index.str.contains('UTP')
    # filtrez video balonul din lista de cantitati si il stochez in variabila video_balun_code pe care o vor folosi in
    # functia jurnal de cabluri
    # de creat un If aici pt camerele analogice

    # liniile de mai jos verifica daca avem video balun in lista de cantitati
    # Daca acesta exista, atunci se va crea variabila video_balun_code ce va stoca codul de produs pt video balun
    # Altfel, variabilei video_balun_code i se va aloca string-ul '-'
    # tipul de cablu este introdus este setat manual
    # cele 2 variabile vor fi folosite de jurnal_cabluri_TVCI(video_balun_code, cable_type_video) pt a crea jurnalul de cabluri
    # de gasit o solutie pt a prelua din lista de cantitati cablul folosit la cablarea camerlor(UTP sau RG)
    filt_video_balun = list(df_TVCI_list_of_qty['Denumire_element'].str.contains('Adaptor pasiv'))
    if True in filt_video_balun:
        video_balun_code = df_TVCI_list_of_qty.loc[filt_video_balun, ['COD_ECHIPAMENT']].iloc[0, 0]
        cable_type_video = 'UTPcat6'
    else:
        video_balun_code = '-'
        cable_type_video = 'UTP cat6'

    # redenumesc coloanele asa cum vreau sa fie afisate in fisierul ce se va crea
    df_TVCI_list_of_qty.rename(
        columns={'Denumire_element': 'Denumire element', 'COD_ECHIPAMENT': 'Cod echipament', 'Cantitate_x': 'Cantitate',
                 'Document_însoțitor': 'Document însoțitor'}, inplace=True)
    # resetez index-ul si salvam
    df_TVCI_list_of_qty.reset_index(drop=True, inplace=True)
    # numerotam index-ul incepand de la 1
    df_TVCI_list_of_qty.index = df_TVCI_list_of_qty.index + 1
    # scriem data frame-ul in sheet 'Lista cantitati' din fisieul excel creat
    df_TVCI_list_of_qty.to_excel(writer, sheet_name='Lista cantitati', index=True)
    # din functia care genereaza lista de cantitati returnam tipul cablului utilizat pt cablarea camerelor. In cazul in care
    # camerele sunt analogice, se va returna si codul video balun-ului utilizat.
    # Acestea vor fi utilizate in functia care creeaza jurnalul de cabluri.
    jurnal_cabluri_TVCI(video_balun_code, cable_type_video)
    # return video_balun_code, cable_type_video

    # print(df_TVCI_list_of_qty)
    # print(cable_type)


TVCI_equipment_qty_table()

writer.save()

#  NU ADAUGA HDD IN LITSA DE CANTITATI DACA ESTE MAI MARE DE 8 TB?? DE VERIFICAT
# !!!!!de afisat eroare atunci cand unul sau mai multe NVR-uri nu au camere asociate la ele
# vezi functia hdd_calculation_and_add_in_equipments_list()