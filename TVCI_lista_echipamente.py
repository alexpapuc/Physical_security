#In aceasta functie aducem rezultatele din modulele
#   - TVCI_calcul_capacit_HDD
#   - add_video_balun_to_list_of_qty



import pandas as pd
from TVCI_calcul_capacit_HDD import hdd_calculation_and_add_in_equipments_list
from TVCI_Video_Balun import add_video_balun_to_list_of_qty
from TVCI_tbl_consum_alege_UPS import ups_calculate

df_db_TVCI = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_TVCI.xlsx')
df_TVCI_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\TVCI.txt', delimiter="\t")
df_TVCI_equipments_with_attributes = pd.DataFrame(pd.merge(df_TVCI_dwg, df_db_TVCI, on='COD_ECHIPAMENT'))

########################
#transformam lista de dictionare importata din modulul TVCI_calcul_capacit_HDD intr-un dataframe
#functia hdd_calculation_and_add_in_equipments_list() returneaza o lista de liste de dictionare, dictionarele continand valorile
#HDD-urilor reiesite din calcule
#apelam functia hdd_calculation_and_add_in_equipments_list() prin atribuirea acesteia la variabila lista_hdd_calculate
#variabila va fi egala cu lista de liste de dictionare returnate de functie
lista_hdd_calculate = hdd_calculation_and_add_in_equipments_list()

#pentru a putea crea dataframe, avem nevoie ca lista_hdd_calculate sa fie o lista de dictionare, nu o lista de liste de dictionare
#pentru a avea ca rezultat o lista de dictionare dintr-o lista de liste de dictionare, folosim nested for de mai jos
flatten_matrix = []
for sublist in lista_hdd_calculate:
    for val in sublist:
        flatten_matrix.append(val)

#print(flatten_matrix)
#dataframe df_hdd_calculate se va adauga in functia de calcul a listei de cantitati echipamente TVCI
df_hdd_calculate = pd.DataFrame(flatten_matrix)
#print(df_hdd_calculate)
########################

########################
#import dictionarul cu video balunurile din modulul TVCI_Video_Balun
dict_video_balun = add_video_balun_to_list_of_qty()
df_video_balun = pd.DataFrame(dict_video_balun)
#print(df_video_balun)
########################

########################
lista_UPS_calculate = ups_calculate()
#pentru a putea crea dataframe pt UPS, avem nevoie ca list dict_UPS sa fie o lista de dictionare, nu o lista de liste de dictionare
#pentru a avea ca rezultat o lista de dictionare dintr-o lista de liste de dictionare, folosim nested for de mai jos
lista_simpla = []
for sublist in lista_UPS_calculate:
    for val in sublist:
        lista_simpla.append(val)

#import dictionarul cu UPS-uri calculate din modulul TVCI_tbl_consum_alege_UPS
df_UPS = pd.DataFrame(lista_simpla)
#print(df_UPS)
########################

#creez un dictionar care va contine ca valori codul video balunului si tipul cablului utilizat in proiect
#lista_coduri = []
dict_pn_video_balun_cablu = {}


def TVCI_equipment_qty_table():
    #adaugam dataframe-urile df_hdd_calculate,df_video_balun la dataframe-ul df_TVCI_equipments_with_attributes
    df_result = df_TVCI_equipments_with_attributes.append([df_hdd_calculate,df_video_balun, df_UPS])
    # creez data frame df_TVCI_list_of_qty pt a grupa echipamentele in functie de 'COD_ECHIPAMENT' si facem count pt cantitate
    df_TVCI_list_of_qty = df_result.groupby(['COD_ECHIPAMENT'])[['Cantitate']].sum()
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
        cable_type_video = 'UTP cat6'
    else:
        video_balun_code = '-'
        cable_type_video = 'UTP cat6'

    # adaug la dictionarul dict_pn_video_balun_cablu codul video balunului si tipul cablului utilizat in proiect
    dict_pn_video_balun_cablu.update({'cod_video_balun' : video_balun_code, 'cod_cablu_TVCI' : cable_type_video})


    # redenumesc coloanele asa cum vreau sa fie afisate in fisierul ce se va crea
    # df_TVCI_list_of_qty.rename(
    #     columns={'Denumire_element': 'Denumire element', 'COD_ECHIPAMENT': 'Cod echipament', 'Cantitate_x': 'Cantitate',
    #              'Document_însoțitor': 'Document însoțitor'}, inplace=True)
    # resetez index-ul si salvam
    df_TVCI_list_of_qty.reset_index(drop=True, inplace=True)
    # numerotam index-ul incepand de la 1
    df_TVCI_list_of_qty.index = df_TVCI_list_of_qty.index + 1
    # scriem data frame-ul in sheet 'Lista cantitati' din fisieul excel creat
    #df_TVCI_list_of_qty.to_excel(writer, sheet_name='Lista cantitati', index=True)
    # din functia care genereaza lista de cantitati returnam tipul cablului utilizat pt cablarea camerelor. In cazul in care
    # camerele sunt analogice, se va returna si codul video balun-ului utilizat.
    # Acestea vor fi utilizate in functia care creeaza jurnalul de cabluri.
    #jurnal_cabluri_TVCI(video_balun_code, cable_type_video)
    # return video_balun_code, cable_type_video

    df_TVCI_list_of_qty['nr_crt'] = df_TVCI_list_of_qty.index.astype(str)
    df_TVCI_list_of_qty = df_TVCI_list_of_qty.astype(str)
    df_TVCI_list_of_qty.rename(columns={'nr_crt' : 'TVCI_qty_nr_crt',
                                        'Denumire_element': 'TVCI_qty_denumire_element',
                                        'COD_ECHIPAMENT' : 'TVCI_qty_tip_element',
                                        'Cantitate_x' : 'TVCI_qty_cantitate',
                                        'Producător' : 'TVCI_qty_producator',
                                        'Furnizor' : 'TVCI_qty_furnizor',
                                        'Document_însoțitor' : 'TVCI_qty_CE'}, inplace=True)
    df_TVCI_list_of_qty = df_TVCI_list_of_qty.to_dict('records')



    #print(dict_pn_video_balun_cablu)
    #print(df_TVCI_list_of_qty)
    return df_TVCI_list_of_qty
    # print(cable_type)

# functia return_pn_video_balun_cablu stocheaza dictionarul dict_pn_video_balun_cablu in coduri_video_balun_cablu
# si il returneaza atunci cand este apelat
def return_pn_video_balun_cablu():
    coduri_video_balun_cablu = dict_pn_video_balun_cablu.copy()
    return coduri_video_balun_cablu


if __name__ == '__main__':
    TVCI_equipment_qty_table()
    return_pn_video_balun_cablu()

# TVCI_equipment_qty_table()


#!!!F important, de retinut ca modulul TVCI_tbl_consum_alege_UPS sa ruleze inainte de a rula modulul TVCI_lista_echipamente, altfel
#UPS-urile nu vor fi scrise in lista de cantitati
#de vazut ce alte functii vor trebui sa returneze dictionare pentru acest modul
#de vazut cum le organiezez astfel incat modulele sa fie apelate in ordine din modulul main
