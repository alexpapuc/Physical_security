from __future__ import print_function
from mailmerge import MailMerge
import pandas as pd

'''Importare module, functii antiefractie'''
from antiefractie import tabele_consum
from antiefractie import creare_tabel_lista_cantitati
from antiefractie import var_surse_alim
from antiefractie_tabel_zonare import creare_tabel_zonare
from antiefractie_jurnal_cabluri import *


'''Importare module, functii TVCI'''
from TVCI_Tabel_Amplasament_Camere import TVCI_camera_labels
from TVCI_tbl_consum_alege_UPS import write_consumption_tables_in_excel
from TVCI_tbl_consum_alege_UPS import calcule_UPS_TVCI
from TVCI_tbl_consum_alege_UPS import putere_aparenta_UPS_calculate
from TVCI_tbl_consum_alege_UPS import tabele_consum_TVCI
from TVCI_lista_echipamente import TVCI_equipment_qty_table
from TVCI_jurnal_cabluri import *
from TVCI_calcul_capacit_HDD import calcule_HDD_TVCI



#creare fisier template in care se vor scrie toate valorile rezultate prin rularea modulelor python
template = (r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\doc_IP_cam.docx')

'''Crarea variabile in care stocam dictionarele cu key si val pt tabelele antiefractie'''
dict_antiefractie_creare_tabel_lista_cantitati = creare_tabel_lista_cantitati()
dict_antiefractie_creare_tabel_calcul_acumulator_efractie = tabele_consum()
dict_antiefractie_var_surse_alimentare = var_surse_alim()
dict_antiefractie_creare_tabel_zonare = creare_tabel_zonare()
dict_antiefractie_creare_tabel_jurnal_cabluri = journal_cables_table(zonare_table)

'''Crarea variabile in care stocam dictionarele cu key si val pt tabelele TVCI'''
dict_TVCI_tabel_amplasare_camere = TVCI_camera_labels()
#dict_run_modul_TVCI_tbl_consum_alege_UPS = write_consumption_tables_in_excel()
dict_TVCI_calcule_UPS = calcule_UPS_TVCI()
dict_TVCI_capacitate_UPS = putere_aparenta_UPS_calculate()
dict_TVCI_tabel_consum_electric = tabele_consum_TVCI()
dict_TVCI_tabel_lista_cantitati = TVCI_equipment_qty_table() # de avut in vedere ca acest modul sa ruleze dupa TVCI_tbl_consum_alege_UPS
dict_TVCI_tabel_jurnal_cabluri = jurnal_cabluri_TVCI(video_balun_code, cable_type_video)
dict_TVCI_calcule_HDD = calcule_HDD_TVCI()


'''Citim fisierul template'''
word_document = MailMerge(template)
print(word_document.get_merge_fields())


print('scrie tabele cantitati, zonare, jurnal efr si TVCI')
''' instructiunea de mai jos scrie tabelele: lista cantitati, zonare, jurnal cabluri  de la antiefractie, TVCI'''
#pt a scrie cu succes in tabelul din word folosim ca si cheie, denumirea variabilei primei coloane din stanga a
#tabelului din word(vezi ex de mai jos)
# scriem valorile in tabelele de calcul a capacitatii acumulatoarelor pentru susrsele de alimentare de la antiefractie
word_document.merge_templates([{'efr_cantitati_nr_crt': dict_antiefractie_creare_tabel_lista_cantitati,
                                'TVCI_qty_nr_crt' : dict_TVCI_tabel_lista_cantitati,
                                'efr_zonare_nr_crt': dict_antiefractie_creare_tabel_zonare,
                                'TVCI_zonare_nr_crt':dict_TVCI_tabel_amplasare_camere,
                                'efr_jurnal_nr_crt': dict_antiefractie_creare_tabel_jurnal_cabluri,
                                'TVCI_jurnal_nr_crt' : dict_TVCI_tabel_jurnal_cabluri
                                },
                               ], separator='page_break')

print('scrie tabele calcul acumulatoare efractie')
''' instructiunea de mai jos scrie tabelele de calcul al acumulatoarelor de la antiefractie'''
# prin functia tabele consum importam o lista de dictionare
# variabila dict_antiefractie_creare_tabel_calcul_acumulator_efractie contine o lista de dictionare
for i in range(len(dict_antiefractie_creare_tabel_calcul_acumulator_efractie)):
    word_document.merge_templates([{'efr_consum_nr_crt'+str(i) : dict_antiefractie_creare_tabel_calcul_acumulator_efractie[i]
                                    },], separator='page_break')

print('scrie rezultate calcule sub tabele efractie')
''' instructiunea de mai jos scrie elementele de sub tabelele de calcul al acumulatoarelor de la antiefractie'''
# variabila dict_antiefractie_var_surse_alimentare = var_surse_alim() contine o lista de dictionare
# functia de scriere a variabilelor in word ia ca argument valori in urmatorul mod document.merge(var1 = 'text1', var2 = 'text2', etc)
# pentru ca am o lista de dictionare, iterez lista si prin (**dict_antiefractie_var_surse_alimentare[i]) convertesc dictionarul
# in valori de tipul (var1 = 'text1', var2 = 'text2', etc) astfel incat sa poata fi scrise in fisierul word.
for i in range(len(dict_antiefractie_var_surse_alimentare)):
    word_document.merge(**dict_antiefractie_var_surse_alimentare[i])

print('scrie tabelele de calcul consum curent de la TVCI')
print(dict_TVCI_tabel_consum_electric)
''' instructiunea de mai jos scrie tabelele de calcul consum curent de la TVCI'''
# prin functia tabele_consum_TVCI() importam o lista de dictionare
# variabila dict_TVCI_tabel_consum_electric contine o lista de dictionare
for i in range(len(dict_TVCI_tabel_consum_electric)):
    print(i)
    word_document.merge_templates([{'TVCI_consum_nr_crt'+str(i) : dict_TVCI_tabel_consum_electric[i]
                                    },], separator='page_break')

print('scrie elementele de sub tabelele de calcul consum curent de la TVCI')
''' instructiunea de mai jos scrie elementele de sub tabelele de calcul consum curent de la TVCI'''
# variabila dict_TVCI_calcule_UPS = calcule_UPS_TVCI() contine o lista de dictionare
# functia de scriere a variabilelor in word ia ca argument valori in urmatorul mod document.merge(var1 = 'text1', var2 = 'text2', etc)
# pentru ca am o lista de dictionare, iterez lista si prin (**dict_TVCI_calcule_UPS[i]) convertesc dictionarul
# in valori de tipul (var1 = 'text1', var2 = 'text2', etc) astfel incat sa poata fi scrise in fisierul word.
for i in range(len(dict_TVCI_calcule_UPS)):
    word_document.merge(**dict_TVCI_calcule_UPS[i])

print('scrie puterea aparenta a UPS-urilor(VA) in calculele pt capacitatea UPS-urilor TVCI')
''' instructiunea de mai jos scrie puterea aparenta a UPS-urilor(VA) in calculele pt capacitatea UPS-urilor TVCI'''
# variabila dict_TVCI_capacitate_UPS = putere_aparenta_UPS_calculate() contine o lista de dictionare
# functia de scriere a variabilelor in word ia ca argument valori in urmatorul mod document.merge(var1 = 'text1', var2 = 'text2', etc)
# pentru ca am o lista de dictionare, iterez lista si prin (**dict_TVCI_capacitate_UPS[i]) convertesc dictionarul
# in valori de tipul (var1 = 'text1', var2 = 'text2', etc) astfel incat sa poata fi scrise in fisierul word.
for i in range(len(dict_TVCI_capacitate_UPS)):
    word_document.merge(**dict_TVCI_capacitate_UPS[i])

print('scrie elementele de sub calculele capacitatii HDD-urilor pt fiecare HDD')
''' instructiunea de mai jos scrie elementele de sub calculele capacitatii HDD-urilor pt fiecare HDD'''
# variabila dict_TVCI_calcule_HDD = calcule_HDD_TVCI() contine o lista de dictionare
# functia de scriere a variabilelor in word ia ca argument valori in urmatorul mod document.merge(var1 = 'text1', var2 = 'text2', etc)
# pentru ca am o lista de dictionare, iterez lista si prin (**dict_TVCI_calcule_HDD[i]) convertesc dictionarul
# in valori de tipul (var1 = 'text1', var2 = 'text2', etc) astfel incat sa poata fi scrise in fisierul word.
for i in range(len(dict_TVCI_calcule_HDD)):
    word_document.merge(**dict_TVCI_calcule_HDD[i])


'''Importare module de test'''
from Test_upload_many_lines import variabile_caracteristic_tehnice
dict_printare_caract_tehnice = variabile_caracteristic_tehnice()


''' instructiunea de mai jos scrie caracteristicile tehnice ale echipamentelor de la efractie, TVCI'''
for i in range(len(dict_printare_caract_tehnice)):
    word_document.merge(**dict_printare_caract_tehnice[i])



#word_document.merge(efr_consum_SA0='CE', efr_i_veghe_SA0='0.5345', efr_i_alarma_SA0='0.8658', efr_acc_SA0 = '18', efr_nr_acc_SA0 = '0.92', efr_acc_rounded_SA0 = '1', efr_consum_SA1 = 'SA1', efr_i_veghe_SA1 = '0.0480', efr_i_alarma_SA1 = '0.0720', efr_acc_SA1 = '7', efr_nr_acc_SA1 = '0.21', efr_acc_rounded_SA1 = '1', efr_consum_SA2 = 'SA2', efr_i_veghe_SA2 = '0.0480', efr_i_alarma_SA2 = '0.0720', efr_acc_SA2 = '7', efr_nr_acc_SA2 = '0.21', efr_acc_rounded_SA2 = '1', efr_consum_SA3 = 'SA3', efr_i_veghe_SA3 = '0.0720', efr_i_alarma_SA3 = '0.1080', efr_acc_SA3 = '7', efr_nr_acc_SA3 = '0.32', efr_acc_rounded_SA3 = '1', efr_consum_SA4 = 'SA4', efr_i_veghe_SA4 = '0.0960', efr_i_alarma_SA4 = '0.1440', efr_acc_SA4 = '7', efr_nr_acc_SA4 = '0.42', efr_acc_rounded_SA4 = '1')




# word_document.merge_templates([{'efr_cantitati_nr_crt': dict_antiefractie_creare_tabel_lista_cantitati,
#                                 'efr_zonare_nr_crt': dict_antiefractie_creare_tabel_zonare,
#                                 'efr_jurnal_nr_crt': dict_antiefractie_creare_tabel_jurnal_cabluri,
#                                 'efr_consum_nr_crt0': dict_antiefractie_creare_tabel_calcul_acumulator_efractie,
#                                 }
#                                ], separator='page_break')

#print(dict_antiefractie_creare_tabel_calcul_acumulator_efractie)



word_document.write('C:\\Users\\alexa\\Desktop\\Proiecte PyCharm\\Pandas Safe World Design\\doc_IP_cam_1.docx')




# de verificat de ce nu este activa linia 19 din acest modul from TVCI_lista_echipamente import TVCI_equipment_qty_table
#de verificat codul pe proiecte deja intocmite si de vazut daca sunt scapari
# de creat cate un template pentru proiecte Profi si proiecte Artima
# de setat variabilele pentru scrierea calculelor capacitatii HDD-urilor


#!!!FFF important, de retinut ca modulul TVCI_tbl_consum_alege_UPS sa ruleze inainte de a rula
# modulul TVCI_lista_echipamente, altfel UPS-urile nu vor fi scrise in lista de cantitati

#06.07
#de verificat de ce nu mai imi adauga UPS-ul in lista de cantitati de la TVCI