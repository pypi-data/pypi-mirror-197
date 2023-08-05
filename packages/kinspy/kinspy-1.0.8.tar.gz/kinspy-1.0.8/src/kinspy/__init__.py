# Name: kinspy
# Describes: provide convenient functions and constants
# Version: v1.0.7
# Date: 2021-12-16
# Author: Yunxiao Zhang
# E-mail: yunxiao9277@gmail.com

# imports
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import torch as t

"common functions"
from numpy import sqrt, sin, cos, exp, log

"common constants"
from numpy import pi, e
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
red = "\033[31m"
end = "\033[0m"

"03 file related functions"
def skip_nlines(fp,n):
    for i in range(n): fp.readline()

def read_columns(fp,*index,sep = " "):
    y = [[] for i in index]

    for line in fp:
        for i in index:
            y[i].append(float(line.strip().split(sep)[i]))
    return (np.array(y[i]) for i in index)

def read_2columns(fp,i,j,is_csv = False):
    a_list = []
    b_list = []
    for line in fp:
        if is_csv == False:
            line_list = line.strip().split()
        else:
            line_list = line.strip().split(",")
        a_list.append(float(line_list[i]))
        b_list.append(float(line_list[j]))
    return np.array(a_list),np.array(b_list)

def read_3columns(fp,i,j,k,is_csv = False):
    a_list = []
    b_list = []
    c_list = []
    for line in fp:
        if is_csv == False:
            line_list = line.strip().split()
        else:
            line_list = line.strip().split(",")
        a_list.append(float(line_list[i]))
        b_list.append(float(line_list[j]))
        c_list.append(float(line_list[k]))
    return np.array(a_list),np.array(b_list),np.array(c_list)

def generate_image_setting():
    plt.rcParams["font.family"] = "Helvetica"
    plt.rcParams["figure.dpi"] = 300
    plt.rcParams["figure.figsize"] = [6.4,4.8]
    plt.rcParams["font.size"] = 12

def printred(txt):
    print(f"{red}"+txt+f"{end}")
