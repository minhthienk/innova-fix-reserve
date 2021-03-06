import pandas as pd
from pathlib import Path



class Vehicles:
    # Contructor
    def __init__(self, path, sheet_names=['vehicle selection']):
        self.sheets = self.load_dtb(path, sheet_names) # a dict to contain all sheets data frame
    # load dtb from excel or pickle files
    @staticmethod
    def load_dtb(path, sheet_names):
        # create data frames from pickle files if not create pickle files
        sheets = {}
        for sheet_name in sheet_names:
            print('read excel files: ', path)
            sheets[sheet_name] = pd.read_excel(path, 
                                               sheet_name=sheet_name, 
                                               header=0, 
                                               na_values='#### not defined ###', 
                                               keep_default_na=False)
        return sheets



def get_sequences(excel_path='vehicle_selection.xlsx'):
    veh_df = Vehicles(excel_path).sheets['vehicle selection']
    veh_list = list(veh_df['vehicle']) # convert vehicle column to list
    veh_list = list(dict.fromkeys(veh_list)) # remove dups keep the same order3
    veh_list = list(filter(lambda x: x!='',veh_list)) # filter empty rows

    sequences = {}
    for veh in veh_list:
        df = veh_df[veh_df['vehicle']==veh]

        actions = list(df['action'])
        parameters = list(df['parameter'])
        sequences[veh] = list(zip(actions, parameters))

    return sequences

