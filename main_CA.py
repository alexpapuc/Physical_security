from __future__ import print_function
from mailmerge import MailMerge
import pandas as pd

from CA_tabele_consum_energetic import tabele_consum_energetic_CA




#creare fisier template in care se vor scrie toate valorile rezultate prin rularea modulelor python
template = (r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\doc_IP_cam.docx')

'''Crarea variabile in care stocam dictionarele cu key si val pt tabelele antiefractie'''
dict_CA_tabele_consum_energetic_CA = tabele_consum_energetic_CA()
print(dict_CA_tabele_consum_energetic_CA)



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




word_document.write('C:\\Users\\alexa\\Desktop\\Proiecte PyCharm\\Pandas Safe World Design\\doc_IP_cam_1.docx')