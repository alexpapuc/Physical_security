import pandas as pd
df_db_TVCI = pd.read_excel(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\db_TVCI.xlsx')
df_TVCI_dwg = pd.read_csv(r'C:\Users\alexa\Desktop\Proiecte PyCharm\Pandas Safe World Design\TVCI.txt', delimiter="\t")
df_TVCI_equipments_with_attributes = pd.DataFrame(pd.merge(df_TVCI_dwg, df_db_TVCI, on='COD_ECHIPAMENT'))

def add_video_balun_to_list_of_qty():
    #global df_TVCI_equipments_with_attributes
    # bazat pe codurile camerelor exportate din dwg filtrez camerele analogice
    filt_analog_cameras = (df_TVCI_equipments_with_attributes['Tehnologie'] == 'ANALOG')
    # creez dataframe-ul cu camerele analogice
    df_analog_cameras = pd.DataFrame(df_TVCI_equipments_with_attributes.loc[filt_analog_cameras,
                                                                            ['SIMBOL_ECHIPAMENT',
                                                                             'Cantitate',
                                                                             'COD_ECHIPAMENT',
                                                                             'Nr. Crt']]).sort_values(by='Nr. Crt',
                                                                                                      ascending=True)
    # creez o variabila in care stochez numarul total de camere analogice
    no_of_analog_cameras = df_analog_cameras['Cantitate'].count()
    while no_of_analog_cameras == 0:
        break
    else:
        # creez o noua variabila in care stochez numarul de video balun-uri ce vor trebui adaugate in lista de cantitati
        no_of_video_balun = no_of_analog_cameras
        no_of_video_balun
        # creez o variabila cu ajutorul careia selectez(in baza codului de produs definit aici) din baza de date video balun-ul
        filt_video_balun = (df_db_TVCI['COD_ECHIPAMENT'] == 'DS-1H18S')
        # creez un dataframe cu video balunul selectat in linia de mai sus
        df_video_balun = pd.DataFrame(df_db_TVCI.loc[
                                          filt_video_balun, ['Denumire_element', 'COD_ECHIPAMENT', 'Cantitate',
                                                             'Producător', 'Furnizor', 'Document_însoțitor']])
        # setez cantitatea de video balun-uri ce vo trebui adaugate in lista de echipamente
        df_video_balun['Cantitate'] = no_of_video_balun
        # adaug video balun-urile in df_TVCI_equipments_with_attributes care sta la baza altgoritmului de creare a listei de cantitati
        #df_TVCI_equipments_with_attributes = df_TVCI_equipments_with_attributes.append(df_video_balun, ignore_index=True)
        dict_df_video_balun = df_video_balun.to_dict(orient='records')
        return dict_df_video_balun

if __name__ == '__main__':
    add_video_balun_to_list_of_qty()

#add_video_balun_to_list_of_qty()