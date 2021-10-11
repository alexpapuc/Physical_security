FCA = ['FCA1', 'FCA2', 'FCA3']
dict_de_la_pana_la_CA = {}
lista_emg_BU = []
lista = ['a', 'b', 'c', 'd']
for filtru in FCA:

    for i in range(len(lista)):
        cheie = lista[i]
        val_conectare_la = 'MCA1'
        lista_emg_BU.append(cheie)

        dict_de_la_pana_la_CA.update({cheie: val_conectare_la})
        lista_emg_BU.clear()

print(dict_de_la_pana_la_CA)
print(lista_emg_BU)


# str = ['E1.1-E1.2','BI1','E2-BU2']
# target_letter = '-'
# lst=[]
# for item in str:
#     if target_letter in item :
#         new_item = item
#         index_position = new_item.index(target_letter)
#         index_position = int(index_position)
#         str_target = item[:index_position]
#         lst.append(str_target)
#     else:
#         lst.append(item)
# print(lst)