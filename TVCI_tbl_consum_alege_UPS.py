#rolul acestui modul este de a:
# 1. calcula capacitatea UPS-urilor si de a le returna catre modulul lista_cantitati
# 2. prin functia tabele_consum_TVCI() returneaza catre main valorile necesare pt tabelele de consum electric la TVCI
# 3. returneaza valorile necesare calculului capacitatii UPS-urilor ce se scriu sub tabelele de consum electric

import pandas as pd
df_db_TVCI = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_TVCI.xlsx')
df_TVCI_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\TVCI.txt', delimiter="\t")
df_TVCI_equipments_with_attributes = pd.DataFrame(pd.merge(df_TVCI_dwg, df_db_TVCI, on='COD_ECHIPAMENT'))

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

#creez o lista goala in care voi introduce dictionarele cu UPS-urile rezultate din calcul care ulterior vor fi
#importate in modulul care creeaza lista de cantitati
lst_UPS_calculate = []

#creez o lista goala in care voi stoca valorile tabelelor de consum curent de la TVCI
lst_tabele_consum = []

#creez o lista goala in care voi stoca valorile variabilelor ce se vor scrie sub tabelele de consum TVCI (calcule UPS-uri)
lst_calcule_UPS = []

#creez o lista goala in care voi stoca valorilein volt Amperi a UPS-urilor calculate
lst_p_aparenta_UPS = []


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
    df_UPS_consum_table['nr_crt'] = df_UPS_consum_table.index
    # redenumesc coloanele
    # df_UPS_consum_table.rename(columns={'SIMBOL_ECHIPAMENT': 'Simbol echipament',
    #                                     'Denumire_element': 'Denumire echipament',
    #                                     'COD_ECHIPAMENT': 'Cod echipament'}, inplace=True)
    # creez o serie pe care o denumesc Total si care este egala cu suma coloanei 'Consum total (W)'
    Total = df_UPS_consum_table['Consum total (W)'].sum()
    # setez 'Total' ca index pt linia de Total si pentru toate coloanele vom avea NaN doar pentru coloana 'Consum total (W)' vom avea totalul
    df_UPS_consum_table.loc['Total'] = pd.Series(df_UPS_consum_table['Consum total (W)'].sum(),
                                                 index=['Consum total (W)'])
    # pt ca functia sa poata returna un data frame creez acest data frame
    df_UPS_consum_table = pd.DataFrame(df_UPS_consum_table)
    #print(df_UPS_consum_table.columns)


    df_TVCI_UPS_consum_table = df_UPS_consum_table
    #df_TVCI_UPS_consum_table['nr_crt'] = df_UPS_consum_table['nr_crt'].astype(int)
    df_TVCI_UPS_consum_table = df_TVCI_UPS_consum_table.fillna(0)
    df_TVCI_UPS_consum_table[['nr_crt','Cantitate']] = df_TVCI_UPS_consum_table[['nr_crt', 'Cantitate']].astype(int)
    df_TVCI_UPS_consum_table = df_TVCI_UPS_consum_table.astype(str)
    #df_TVCI_UPS_consum_table[['nr_crt', 'Cantitate']] = df_TVCI_UPS_consum_table[['nr_crt', 'Cantitate']].astype(str)
    #print(df_TVCI_UPS_consum_table)
    df_TVCI_UPS_consum_table.rename(columns={'nr_crt': 'TVCI_consum_nr_crt' + str(i),
                                             'SIMBOL_ECHIPAMENT': 'TVCI_consum_simbol_element' + str(i),
                                             'Denumire_element': 'TVCI_consum_denumire_element' + str(i),
                                             'COD_ECHIPAMENT': 'TVCI_consum_tip_element' + str(i),
                                             'Cantitate': 'TVCI_consum_cantitate' + str(i),
                                             'Consum/buc.(W)': 'TVCI_consum_buc' + str(i),
                                             'Consum total (W)': 'TVCI_consum_total' + str(i)}, inplace=True)

    dict_df_TVCI_UPS_consum_table = df_TVCI_UPS_consum_table.to_dict('records')
    lst_tabele_consum.append(dict_df_TVCI_UPS_consum_table)
    #print(dict_df_TVCI_UPS_consum_table)


    return df_UPS_consum_table


'''
aceasta functie creeaza o variabila de verificare, care in baza valorii total_consumption_VA alege un UPS din baza de date a 
carui putere este mai mare sau egala cu puterea calculata(total_consumption_VA) dupa care il adaug UPS-ul selectat se va 
adauga la lista de cantitati TVCI

'''


def choose_UPS_from_db_TVCI(total_consumption_VA, i_din_write_consumption_tables_in_excel):
    list_of_ups_values = list(df_db_TVCI['Putere_UPS_VoltAmp'])
    for item in list_of_ups_values:
        if item >= total_consumption_VA:
            total_consumption_VA = item
            break
    #returnez un df cu UPS-ul calculat
    filt_UPS = (df_db_TVCI['Putere_UPS_VoltAmp'] == total_consumption_VA)
    df_UPS = df_db_TVCI.loc[
        filt_UPS, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate', 'Producător', 'Furnizor', 'Document_însoțitor']]
    #df_TVCI_equipments_with_attributes = df_TVCI_equipments_with_attributes.append(df_UPS, ignore_index=True)
    dict_df_UPS = df_UPS.to_dict(orient='records')
    copy_of_dict_df_UPS = dict_df_UPS.copy()
    lst_UPS_calculate.append(copy_of_dict_df_UPS)
    #print('a rulat functia care face append')
    #return print(dict_df_UPS)

    #creez o variabila pe care o voi salva sub forma de dictionar ce contine puterea in VA a UPS-urilor calculate
    p_aparenta_UPS = (df_db_TVCI['Putere_UPS_VoltAmp'] == total_consumption_VA)
    df_p_aparenta_UPS = df_db_TVCI.loc[p_aparenta_UPS, ['Putere_UPS_VoltAmp']]
    putere_aparenta_UPS = str(int(df_p_aparenta_UPS.iloc[0,0]))
    print(putere_aparenta_UPS)
    dict_p_aparenta_UPS = {}
    dict_p_aparenta_UPS.update({'putere_UPS' + str(i_din_write_consumption_tables_in_excel) : putere_aparenta_UPS})

    lst_p_aparenta_UPS.append(dict_p_aparenta_UPS)

    return lst_UPS_calculate
    # dict_df_p_aparenta_UPS = df_p_aparenta_UPS(orient='records')
    # copy_of_dict_df_p_aparenta_UPS = dict_df_p_aparenta_UPS.copy()
    # lst_p_aparenta_UPS.append(copy_of_dict_df_p_aparenta_UPS)



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

        # am nevoie de i din instructiunea for in functia  pentru functia "choose_UPS_from_db_TVCI
        # valoarea lui i o stochez in variabila i_din_write_consumption_tables_in_excel, pe care o
        # o voi folosi ca atribut la functia choose_UPS_from_db_TVCI
        i_din_write_consumption_tables_in_excel = i

        # apelez functia care introduce UPS-ul in lista de cantitati si care creeaza dictionatul cu capacitatile UPS-urilor
        #calculate, capacitati care vor fi scrise in fisierul word la calculul UPS-urilor putere_aparenta_UPS
        choose_UPS_from_db_TVCI(total_consumption_VA, i_din_write_consumption_tables_in_excel)

        #creez variabilele la care voi atribui valorile ce se vor afisa sub tabelul de calcul consum TVCI(calcul UPS-uri)
        denumire_UPS = str(list_of_UPS_labels[i])
        consum_total_Watt = f'{total_consumption:.2f}'
        consum_UPS = f'{total_consumption_VA:.2f}'

        # creare dictionar cu valori ce se afiseaza in descrierea calculelor de sub tabelul de consum curent TVCI(calcul UPS-uri)
        dict_val_calcul_UPS_TVCI = {}
        dict_val_calcul_UPS_TVCI.update({'denumire_UPS' + str(i) : denumire_UPS,
                                         'consum_total_Watt' + str(i) : consum_total_Watt,
                                         'consum_UPS' + str(i) : consum_UPS})

        lst_calcule_UPS.append(dict_val_calcul_UPS_TVCI)



#functia ups_calculate() aduce lista de dictionare lst_UPS_calculate, o salveaza in variabila list_UPS_calculate si
# o retuneaza pentru a fi utilizata in modulul TVCI_lista echipamente pentru a adauga UPS-urile in lista de echipamente.
def ups_calculate():
    #lista_echipamente_tabele_consum = list(map(dict, chain.from_iterable(lst)))
    list_UPS_calculate = lst_UPS_calculate
    #print(lst)
    #print(list_UPS_calculate)
    return list_UPS_calculate

#functia tabele_consum_TVCI() aduce lista de dictionare lst_tabele_consum, o salveaza in variabila lista_tabele_consum_TVCI si
# o retuneaza pentru a fi utilizata in modulul main pentru a scrie tabelele de consum TVCI.
def tabele_consum_TVCI():
    lista_tabele_consum_TVCI = lst_tabele_consum
    return lista_tabele_consum_TVCI

#functia tabele_consum_TVCI() aduce lista de dictionare lst_tabele_consum, o salveaza in variabila lista_tabele_consum_TVCI si
# o retuneaza pentru a fi utilizata in modulul main pentru a scrie tabelele de consum TVCI.
def calcule_UPS_TVCI():
    lista_calcule_UPS_TVCI = lst_calcule_UPS
    return lista_calcule_UPS_TVCI

def putere_aparenta_UPS_calculate():
    lista_putere_aparenta_UPS_calculate = lst_p_aparenta_UPS
    return lista_putere_aparenta_UPS_calculate

#!!!F important, de retinut ca modulul TVCI_tbl_consum_alege_UPS sa ruleze inainte de a rula modulul TVCI_lista_echipamente, altfel
#UPS-urile nu vor fi scrise in lista de cantitati

if __name__ == '__main__':
    write_consumption_tables_in_excel()
    ups_calculate()
    tabele_consum_TVCI()
    calcule_UPS_TVCI()
    putere_aparenta_UPS_calculate()