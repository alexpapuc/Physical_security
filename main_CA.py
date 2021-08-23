from __future__ import print_function
from mailmerge import MailMerge
import pandas as pd

from CA_tabele_consum_energetic import valori_tabele_consum_energetic_CA
from CA_tabele_consum_energetic import valori_calcule_surse_alim_CA
from CA_tabel_zone_supravegheate import CA_tabel_zone_supravegheate



#creare fisier template in care se vor scrie toate valorile rezultate prin rularea modulelor python
template = (r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\doc_IP_cam.docx')

'''Crerea variabile in care stocam dictionarele cu key si val pt tabelele control acces'''
dict_CA_tabele_consum_energetic_CA = valori_tabele_consum_energetic_CA()
dict_CA_valori_calcule_surse_alim_CA = valori_calcule_surse_alim_CA()
dict_CA_valori_tabel_zone_supravegheate = CA_tabel_zone_supravegheate()

#print(dict_CA_tabele_consum_energetic_CA)



'''Citim fisierul template'''
word_document = MailMerge(template)
print(word_document.get_merge_fields())




print('scrie tabele calcul acumulatoare control acces')
''' instructiunea de mai jos scrie tabelele de calcul al acumulatoarelor de la control acces'''
# prin functia tabele consum importam o lista de dictionare
# variabila dict_antiefractie_creare_tabel_calcul_acumulator_efractie contine o lista de dictionare
for i in range(len(dict_CA_tabele_consum_energetic_CA)):
    print(i)
    word_document.merge_templates([{'CA_consum_nr_crt'+str(i) : dict_CA_tabele_consum_energetic_CA[i]
                                    },], separator='page_break')


print('scrie tabele cantitati, zonare, jurnal CA')
''' instructiunea de mai jos scrie tabelele: lista cantitati, zonare, jurnal cabluri de la CA'''
#pt a scrie cu succes in tabelul din word folosim ca si cheie, denumirea variabilei primei coloane din stanga a
#tabelului din word(vezi ex de mai jos)
# scriem valorile in tabelele de calcul a capacitatii acumulatoarelor pentru susrsele de alimentare de la antiefractie
word_document.merge_templates([{'CA_zonare_nr_crt': dict_CA_valori_tabel_zone_supravegheate,
                                },
                               ], separator='page_break')




print('scrie rezultate calcule sub tabele CA')
''' instructiunea de mai jos scrie elementele de sub tabelele de calcul al acumulatoarelor de la CA'''
# variabila dict_CA_valori_calcule_surse_alim_CA contine o lista de dictionare
# functia de scriere a variabilelor in word ia ca argument valori in urmatorul mod document.merge(var1 = 'text1', var2 = 'text2', etc)
# pentru ca am o lista de dictionare, iterez lista si prin (**dict_CA_valori_calcule_surse_alim_CA[i]) convertesc dictionarul
# in valori de tipul (var1 = 'text1', var2 = 'text2', etc) astfel incat sa poata fi scrise in fisierul word.
#print(dict_CA_valori_calcule_surse_alim_CA)
for i in range(len(dict_CA_valori_calcule_surse_alim_CA)):
    word_document.merge(**dict_CA_valori_calcule_surse_alim_CA[i])

from CA_tabel_lista_cantitati import dict_SA_CA
print(dict_SA_CA)

word_document.write('C:\\Users\\alexa\\Desktop\\Proiecte PyCharm\\Pandas Safe World Design\\doc_IP_cam_1.docx')

#de vazut daca pot face "- în stare de acţionare: 12Ah / 0.0A = nu există consum pe sursa de alimentare SC4."
# sa fie o singura variabila astfel incat atunci cand am consum 0 sa se afiseze
# - în stare de acţionare: nu există consum pe sursa de alimentare SC4.
# sa o fac o singura variabila iar la conditia else, sa ramana doar fraza - în stare de acţionare: nu există consum pe sursa de alimentare SC4.
# fara alte variabile


# de completat variabilele pentru tabelul lista cantitati in fisierul template word si de
# creat dictionarul pentru scrierea informatiilor in tabelul word.