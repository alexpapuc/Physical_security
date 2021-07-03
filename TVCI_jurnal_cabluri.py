import pandas as pd

df_db_TVCI = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_TVCI.xlsx')
df_TVCI_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\TVCI.txt', delimiter="\t")
df_TVCI_equipments_with_attributes = pd.DataFrame(pd.merge(df_TVCI_dwg, df_db_TVCI, on='COD_ECHIPAMENT'))

# import variabilele video_balun_code si cable_type_video din modulul TVCI_lista_echipamente
from TVCI_lista_echipamente import TVCI_equipment_qty_table
from TVCI_lista_echipamente import return_pn_video_balun_cablu
TVCI_equipment_qty_table()

dict_coduri_video_balun_cablu = return_pn_video_balun_cablu()
video_balun_code = dict_coduri_video_balun_cablu.get('cod_video_balun')
cable_type_video = dict_coduri_video_balun_cablu.get('cod_cablu_TVCI')
#print(video_balun_code,cable_type_video)

# functia jurnal_cabluri_TVCI se apeleaza in functia TVCI_equipment_qty_table
def jurnal_cabluri_TVCI(video_balun_code, cable_type_video):
    df_TVCI_equipments_with_attributes = pd.DataFrame(pd.merge(df_TVCI_dwg, df_db_TVCI, on='COD_ECHIPAMENT'))
    # setezca index coloana SIMBOL_ECHIPAMENT din df_TVCI_equipments_with_attributes
    df_TVCI_equipments_with_attributes.sort_values(by=['SIMBOL_ECHIPAMENT'], inplace=True)
    df_TVCI_equipments_with_attributes.index = df_TVCI_equipments_with_attributes.SIMBOL_ECHIPAMENT
    #df_TVCI_equipments_with_attributes

    # cream serie de la
    serie_de_la_camere = df_TVCI_equipments_with_attributes['SIMBOL_ECHIPAMENT']
    #serie_de_la_camere

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
    #serie_pana_la

    # cream seria prin
    def prin_video_map(x):
        #print(df_TVCI_equipments_with_attributes['Tehnologie'])
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
    #serie_prin

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
    #serie_tip_cablu_video

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
    #serie_pana_la_alimentare

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
    #serie_tip_cablu_alimentare



    # se creeaza dataframe-ul final cu toate seriile de mai sus care va reprezenta jurnalul de cabluri
    df_jurnal_cabluri_camere = pd.DataFrame({'De la': serie_de_la_camere.values,
                                             'Prin': serie_prin.values,
                                             'Pana la': serie_pana_la.values,
                                             'Tip cablu': serie_tip_cablu_video.values,
                                             'Pana la alimentare': serie_pana_la_alimentare.values,
                                             'Tip cablu alimentare': serie_tip_cablu_alimentare.values})

    # resetez index-ul si salvam
    df_jurnal_cabluri_camere.reset_index(drop=True, inplace=True)
    # numerotam index-ul incepand de la 1
    df_jurnal_cabluri_camere.index = df_jurnal_cabluri_camere.index + 1
    df_jurnal_cabluri_camere['nr_crt'] = df_jurnal_cabluri_camere.index
    lista_cod_cablu_TVCI = []
    for i in range(len(df_jurnal_cabluri_camere['nr_crt'])):
        lista_cod_cablu_TVCI.append('T'+ str(i+1))
    df_jurnal_cabluri_camere['cod_cablu'] = lista_cod_cablu_TVCI
    print(df_jurnal_cabluri_camere)
    df_jurnal_cabluri_camere = df_jurnal_cabluri_camere.astype(str)
    df_jurnal_cabluri_camere.rename(columns={'nr_crt' : 'TVCI_jurnal_nr_crt',
                                             'cod_cablu' : 'TVCI_jurnal_cod_cablu',
                                             'De la': 'TVCI_jurnal_de_la',
                                             'Pana la': 'TVCI_jurnal_video_pana_la',
                                             'Prin': 'TVCI_jurnal_video_de_la',
                                             'Tip cablu' : 'TVCI_jurnal_video_tip_cablu',
                                             'Pana la alimentare' : 'TVCI_jurnal_alim_pana_la',
                                             'Tip cablu alimentare' : 'TVCI_jurnal_alim_tip_cablu'}, inplace = True)
    dict_jurnal_cabluri_TVCI = df_jurnal_cabluri_camere.to_dict('records')
    print(dict_jurnal_cabluri_TVCI)
    return dict_jurnal_cabluri_TVCI


if __name__ == '__main__':
    jurnal_cabluri_TVCI(video_balun_code, cable_type_video)

