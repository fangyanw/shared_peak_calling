#put this script with the same dictionar of your peakAnn file
#run this script using python, output should be in the same dictionay

import os
import numpy as np
import pandas as pd

def pos_list(start_num,motif_str):
    motif_pos_lst=[]
    if type(motif_str) is str:
        motif_lst=motif_str.split("),")
        for motif in motif_lst:
            motif_disseq=motif.split("(")
            motif_pos_lst.append(start_num+int(motif_disseq[0]))
    return motif_pos_lst

def compare_motif(motif_loc,data_df):
    inter = []
    for n in data_df["motif_pos"]:
        inter.extend([_ for _ in n if _ in motif_loc])
    if len(inter) > 0:
        return inter
    else:
        return np.nan


path=os.getcwd()
files=os.listdir(path)
file_csv=[f for f in files if f[-3:] == 'xls']
name_c=input("Enter the sample you want to compare with:")
for f in file_csv:
    if f[:6] == name_c:
        data_c=pd.read_csv(f,delimiter="\t")
for f in file_csv:
    if f[:6] != name_c:
        data_c=pd.read_csv(f,delimiter="\t")
        data_o=pd.read_csv(f,delimiter="\t")
        data_c.rename(columns={"STAT6N3 Distance From Peak(sequence,strand,conservation)":"STAT6N3","STAT6N4 Distance From Peak(sequence,strand,conservation)":"STAT6N4"},inplace=True)
        data_o.rename(columns={"STAT6N3 Distance From Peak(sequence,strand,conservation)":"STAT6N3","STAT6N4 Distance From Peak(sequence,strand,conservation)":"STAT6N4"},inplace=True)
        data_c["motif_pos"]=data_c[["Start","STAT6N3","STAT6N4"]].apply(lambda x: pos_list(x[0],x[1])+pos_list(x[0],x[2]), axis=1)
        data_o["motif_pos"]=data_o[["Start","STAT6N3","STAT6N4"]].apply(lambda x: pos_list(x[0],x[1])+pos_list(x[0],x[2]), axis=1)
        data_o["Motif_loc_also_in_"+name_c]=data_o["motif_pos"].apply(compare_motif, data_df=data_c)
        data_o=data_o.drop(columns=["motif_pos"])
        data_o.to_csv("compare_"+f[:-4]+".csv")
