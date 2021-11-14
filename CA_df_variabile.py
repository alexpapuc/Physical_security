from CA_functii import *
#verificare daca codurile de echipamente exportate din dwg se regasesc in baza de date
check_items()

#verificare daca un simbol de echipament apare de mai multe ori(de ex: PIR1 de mai multe ori)
verificare_simboluri_echipamente()

#verificare daca vreun echipament din dwg nu are sursa atribuita
verificare_elemente_ce_nu_au_sursa_atribuita()

#verificare daca vreun echipament din dwg nu are simbol atribuit
verificare_elemente_fara_simbol_atribuit()

#stochez lista cu sursele de alimentare din dwg intr-o variabila
lista_surse_alimentare_CA = lista_surse_alimentare_CA()

#stochez capacitatea acumulatorului(introdus de la tastatura) in variabila capacitate_acc_SA_CA
capacitate_acc_SA_CA = citire_valoare_capacitate_acc_CA()

#stochez lista ce contine dictionarele acumulatoarelor surselor de alimentare CA in var
lista_dict_acc_surse_alimentare_CA = creare_dictionar_acc_surse_CA(capacitate_acc_SA_CA, lista_surse_alimentare_CA)

################ - se importa in main
#stochez lista cu liste de dictionare ce contin valorile ce trebuiesc scrise in tabelele de consumuri energetice pt CA
lista_dict_valori_tabele_consum_energetic_CA = tabele_consum_energetic_CA(lista_surse_alimentare_CA)
#print(lista_dict_valori_tabele_consum_energetic_CA)

################ - se importa in main
#stochez lista cu dictionare ce contin valorile ce trebuiesc scrise sub tabelele de consumuri energetice pt CA
lista_dict_valori_sub_tabele_consum_energetic_CA = \
    valori_calcule_sub_tabele_consum_energetic_CA(capacitate_acc_SA_CA, lista_surse_alimentare_CA)
#print(lista_dict_valori_sub_tabele_consum_energetic_CA)

################ - se importa in main
#stochez lista cu dictionare ce contin valorile ce trebuiesc scrise in tabelul cu zonele supravegheate de la CA
dict_tabel_zone_supravegheate_CA = CA_tabel_zone_supravegheate()
#print(dict_tabel_zone_supravegheate_CA)

#creez dataframe-ul ce contine acumulatoarele aferente surselor de alimentare din sistemul de CA
#acest df se va adauga la dataframe-ul cu restul echipamentelor din sistemul de CA si va forma lista de cantitati pt CA
df_acc_SA_CA = creare_df_acc_SA_CA(lista_dict_acc_surse_alimentare_CA)

################ - se importa in main
#stochez lista cu dictionare ce contin valorile ce trebuiesc scrise in tabelul cu listele de cantitati pentru CA
dict_tabel_lista_cantitati_CA = CA_lista_cantitati(df_acc_SA_CA)
#print(dict_tabel_lista_cantitati_CA)

"""Se creaza dictionarul cu caracteristicile tehnice ale echipamentelor sistemului de CA"""
dict_caracteristici_tehnice = caracteristici_tehnice_CA(dict_tabel_lista_cantitati_CA)


"""Se creaza dataframe cu echipamentele ce vor fi incluse in junrnalul de cabluri"""
df_echip_pt_jurnal_cabluri = creare_df_echip_jurnal_cabluri_CA()

"""Identificam filtrele de control acces componente in sistem(FCA1, FCA2, FCA3, .....)"""
lista_filtre_de_CA = identificare_FCA(df_echip_pt_jurnal_cabluri)

"""Creez un dictionar ce contine key = simbolurile ce vor reprezenta coloana DE LA din jurnalul de cabluri;
values = simbolurile ce vor reprezenta coloana Pana la in jurnalul de cabluri"""
dict_elem_CA_de_la_pana_la = dict_elemente_de_la_pana_la_CA(df_echip_pt_jurnal_cabluri, lista_filtre_de_CA)
#print(dict_elem_CA_de_la_pana_la)

"""creez seriile de la si pana la din dict dict_elem_CA_de_la_pana_la"""
serie_de_la_CA = serie_de_la_jurnal_cabluri_CA(dict_elem_CA_de_la_pana_la)
serie_pana_la_CA = serie_pana_la_jurnal_cabluri_CA(dict_elem_CA_de_la_pana_la)

"""Pentru ca in coloana DE LA din jurnalul de cabluri o sa avem simboluri/string de tipul E1.1-E1.2-BU1-MCU1, va 
trebui sa scot  din string, primul simbol pana in caracterul '-' (in cazul nostru E1.1) astfel incat in baza acestuia 
sa se poata face maparea simbolurilor pentru identificarea tipurilor de cabluri (coloana tip cablu) corespunzatoare
fiecarui simbol din coloana DE LA """
lista_simboluri_pt_tip_cablu = scoate_primul_simbol_din_echip_inseriate(dict_elem_CA_de_la_pana_la)
print(lista_simboluri_pt_tip_cablu)

serie_tip_cabluri_CA = serie_tip_cabluri_jurnal_CA(df_echip_pt_jurnal_cabluri, lista_simboluri_pt_tip_cablu)

"""Creare data frame jurnal cabluri CA"""
df_jurnal_cabluri_CA = df_jurnal_cabluri(serie_de_la_CA, serie_pana_la_CA, serie_tip_cabluri_CA)

"""Creare dictionar cu valorile pt jurnal cabluri control acces"""
dict_tabel_jurnal_cabluri_CA = creare_dict_jurnal_cabluri_CA(df_jurnal_cabluri_CA)

"""Creare dictionar cu valorile de vor scrie in fisierul word caracteristicile echipamentelor de control acces 
extrase din lista de cantitati echipamente de control acces"""







#de identificat de ce la E1.2-E1.1-BU1-MCU1 apare MCU1 la pana la in loc de SC1