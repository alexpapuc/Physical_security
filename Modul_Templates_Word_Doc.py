temp10 = (r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\\'
            'Pandas Docx Merge Safe World Design\Word_Doc_Templates\Templ10_Crf_Expr_Low_Cost_2SA_4CA_simplu.docx')
temp11 = (r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\\'
            'Pandas Docx Merge Safe World Design\Word_Doc_Templates\Templ11_Crf_Artima_2SA_4CA_simplu.docx')
temp12 = (r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\\'
            'Pandas Docx Merge Safe World Design\Word_Doc_Templates\Templ12_Crf_Artima_2SA_4CA_2ETAJE.docx')
temp20 = (r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\\'
            'Pandas Docx Merge Safe World Design\Word_Doc_Templates\Templ20_Profi_analogCE 1FCA.docx')
temp21 = (r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\\'
            'Pandas Docx Merge Safe World Design\Word_Doc_Templates\Templ21_Profi_IP_CE 2FCA.docx')
temp22 = (r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\\'
            'Pandas Docx Merge Safe World Design\Word_Doc_Templates\Templ22_Profi_IP_2SA_3UPS_4DVR.docx')
temp99 = (r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\\'
            'Pandas Docx Merge Safe World Design\Word_Doc_Templates\Templ99_ 8SA 12SC 3UPS 4DVR.docx')


dict_denumiri_fisiere_template = {
    "1" : temp10,
    "2" : temp11,
    "3" : temp12,
    "4" : temp20,
    "5" : temp21,
    "6" : temp22,
    "9" : temp99
}

def fisiere_template():
    for key, value in dict_denumiri_fisiere_template.items():
        print(f'{key} ==> {value}')

def selecteaza_fisier():
    fisiere_template()
    fisier_word = int(input(f'Introdu valoarea corespunzatoare fiserului dorit: '))
    lista_chei_dict = dict_denumiri_fisiere_template.keys()
    if str(fisier_word) in lista_chei_dict:
        #print(dict_denumiri_fisiere_template.get(str(fisier_word)))
        return dict_denumiri_fisiere_template.get(str(fisier_word))
    else:
        print('Numarul tasatat nu se afla printe optiunile afisate. Tastati unul din numerele afisate!')


# fisiere_template()
# selecteaza_fisier()