import pandas as pd
df_db = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_efractie.xlsx')
df_intrussion_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\zonare.txt',
                                delimiter="\t")

print(df_db.columns)
print(df_intrussion_dwg.columns)



#caracteristici_tehnice_echipamente = []
# for item in list(df_intrussion_dwg['COD_ECHIPAMENT']):
#     filter = df_db['COD_ECHIPAMENT'] == item
#     caracteristici_tehnice_echipamente.append(df_db.loc[filter,'Caracteristici tehnice'])
#
# print(caracteristici_tehnice_echipamente)

def fct_ce_printez():
    caracteristici_tehnice_echipamente = list(df_db['Caracteristici tehnice'])
    lista_dict = []
    #print(caracteristici_tehnice_echipamente)
    ce_printez = caracteristici_tehnice_echipamente[0]
    ce_printez_1 = caracteristici_tehnice_echipamente[1]
    dict_ce_printez = {'var1': ce_printez, 'var2' : ce_printez_1}
    lista_dict.append(dict_ce_printez)
    return lista_dict
fct_ce_printez()

if __name__ == '__main__':
    fct_ce_printez()