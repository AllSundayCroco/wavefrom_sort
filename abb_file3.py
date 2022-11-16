
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 18:08:39 2022

@author: NML-CID003158
"""

import pandas as pd
from pathlib import Path
import glob

class AbbFile:
    
    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__file_name = Path(file_path).stem
        self.__machine_num = self.__file_name.split('_')[0]
        self.__step_num = self.__file_name.split('_')[1]
        self.__data_list = pd.read_csv(self.__file_path).columns.values
        self.__date = self.__file_name.split('_')[2]
    
    @property
    def file_name(self) -> str:
        return self.__file_name
    @property
    def machine_num(self) -> str:
        return self.__machine_num
    @property
    def step_num(self) -> str:
        return self.__step_num
    @property
    def data_list(self) -> list:
        return self.__data_list
    @property
    def date(self) -> str:
        return self.__date
    
    def get_data(self) -> pd.DataFrame:
        return pd.read_csv(self.__file_path, 
                          index_col=None, 
                           header=0, 
                           skiprows=1, 
                           names = self.__data_list)

    def data(self) -> pd.DataFrame:
        return pd.read_csv(self.__file_path)
        


if __name__ == '__main__':
    
    file_path = r'C:\Users\admin\Desktop\tdxabb_3\input'# demo
    for machine in sorted(glob.glob(file_path + '/*')):
        abb_file = AbbFile(machine)
        print(abb_file.machine_num)
        print(abb_file.get_data())
    
       # print(abb_file.machine_num)
       # print(abb_file.step_num)

 
    #print(abb_file.file_name)
    #print(abb_file.machine_num)
    #print(abb_file.step_num)
    #print(abb_file.data_list)
    #print(abb_file.get_data())
    