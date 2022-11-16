# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 10:30:56 2022

@author: admin
"""

import pandas as pd
import statistics
from abb_file3 import AbbFile
import glob
import shutil
import os
from datetime import datetime
import time



def insert_units(df,i,df_add):
    df1 = df.iloc[:i,:]
    df2 = df.iloc[i:,:]
    df_new = pd.concat([df1,df_add,df2],ignore_index=True)
    return df_new


if __name__ == '__main__':
    
    try:
        while True:
            print('{} => file check...'.format(datetime.now()))
            

            file_path = r'C:\Users\admin\Desktop\tdxabb_3\input'
            pathexcel = r'.\Setting4.xlsx'
            book = pd.ExcelFile(pathexcel)
            df = book.parse('ファイル仕分け設定').set_index('INDEX')
            df_2 = book.parse('共通設定').set_index('設定名称')
            path_2 = {
                'input':  df_2.at['入力フォルダ','設定値'],
                'output': df_2.at['出力フォルダ','設定値'],
                'trash1':  df_2.at['仕分け後廃棄フォルダ','設定値'],
                'trash2': df_2.at['先頭合わせ廃棄フォルダ','設定値'],
                'backup': df_2.at['バックアップ' ,'設定値']

                }
            
            interval_sec = df_2.at['ファイルチェック周期' ,'設定値']
            #print(df)
            t=len([entry for entry in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, entry))])
            if t != 0:
                print('{} files are found.'.format(t))
            for machine_name in sorted(glob.glob(file_path+ '/*')):

                op_num = AbbFile(machine_name).machine_num
                step = AbbFile(machine_name).step_num
                date = AbbFile(machine_name).date
                for i in range(len(df)):            
                    op_data = df.iloc[i]
                    #print(op_data)
                    set_op_num = op_data[0]   #OP number
                    set_op_step = op_data[1]  #Step number
                    set_op_pos = op_data[2]   #position number
                    set_op_value1 = op_data[5]   #step 1 value
                    set_op_channel = op_data[6]
                    set_op_value2 = op_data[7]   #step 2 value
                    set_op_lineback = op_data[8]  # number for lineback
                    set_op_need = op_data[9]   #number for list
                    if op_num == set_op_num and step == set_op_step:               
                        print('op_value',set_op_value1)
                        #print('set_op_value',set_op_value1)
                        data = AbbFile(machine_name).get_data()
                        data_loc = set_op_pos
                        data_channel = set_op_channel
                        data_max = max(data.loc[:,data_loc])
                        data_max_channel = max(data.loc[:,data_channel])
                        data_min = min(data.loc[:,data_loc])
                        data_min_channel = min(data.loc[:,data_channel])
                        if set_op_value1 <= data_max:
                            if set_op_value2 <= data_max_channel and set_op_value2 >= data_min_channel:
                                list_data = data.loc[:,data_channel].astype(float) 
                                hits = list_data[list_data >= set_op_value2].index.tolist()
                                #print(hits)
                                drop_line = hits[0] - set_op_lineback
                               # print(drop_line)
                                if drop_line < 0:
                                    dst_trash2 = op_num + '\\' + 'trash2' 
                                    if not os.path.exists(dst_trash2):
                                        os.makedirs(dst_trash2)  
                                    dst_trash2 = machine_name.replace(path_2['input'] + '\\', dst_trash2 + '\\')                       
                                    shutil.move(machine_name, dst_trash2)
                                    continue             
                                    
                                data = data.drop(axis=0,index=(range(0, drop_line)))   # 不要な行を削除
                                data = data[:set_op_need]                  # 必要な行数だけ取出し
                                data = data.reset_index(drop=True)      # index振直し
                                #print(data)                            
                                                               
                        else:
                            dst_trash = op_num + '\\' + 'trash1' 
                            if not os.path.exists(dst_trash):
                                os.makedirs(dst_trash)  
                            dst_trash = machine_name.replace(path_2['input'] + '\\', dst_trash+'\\')
                            shutil.move(machine_name, dst_trash)
                            continue
                        
                        
                        dst = 'output'
                        output = machine_name.replace(path_2['input'] + '\\',dst + '\\' + 'A_')
                        #print(output)
                        #print(output)
                        data = data.drop(['Unnamed: 13',
                                                          'Unnamed: 14','Unnamed: 15',
                                                          'Unnamed: 16','Unnamed: 17'],axis=1)                   
                        if not os.path.exists(dst):
                            os.makedirs(dst)
                        cols = list(data)
                        cols.insert(0,'DATE')
                        aligned_data = data.reindex(columns=cols, fill_value = date[:4]+'/'+date[4:6]+'/'+date[6:8])
                        add_df = pd.DataFrame({'DATE':['DATE'],'TIME':['TIME'],'1軸_トルクコマンド':['%'],'2軸_トルクコマンド':['%'],'3軸_トルクコマンド':['%']
                                               ,'4軸_トルクコマンド':['%'],'5軸_トルクコマンド':['%'],'6軸_トルクコマンド':['%'],
                                               '1軸_ポジション':['degree'],'2軸_ポジション':['degree'],'3軸_ポジション':['degree'],
                                               '4軸_ポジション':['degree'],'5軸_ポジション':['degree'],'6軸_ポジション':['degree']})
                        aligned_data = insert_units(aligned_data, 0, add_df)
                        aligned_data.to_csv(output, index = False, encoding = 'shift-jis')
                        #aligned_data.to_csv(path_2['output'], index = False, encoding = 'shift-jis')
                        time.sleep(5)
                        
                        dst_backup = op_num + '\\' + 'backup'
                        print(dst_backup)
                        if not os.path.exists(dst_backup):
                             os.makedirs(dst_backup)  
                             
                        dst_backup = machine_name.replace('input' + '\\' , dst_backup + '\\')
                        shutil.move(machine_name,dst_backup)
                        #os.remove(machine_name)
                    else:
                        pass
            time.sleep(interval_sec)          
    except KeyboardInterrupt:
        print('プログラムを終了します')