#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 20:39:59 2019

@author: longzhan
"""

import pickle as pkl
import re
import argparse

def loadData(filename):
    data = []
    origin_data = []
    p = re.compile(r"[^A-Za-z]+")
    with open(filename) as f:
        for line in f:
            x = p.split(line.strip())
            for item in x:
                if item == '':
                    x.remove(item)
            data.append(x)   
            origin_data.append(line.strip())
    return data, origin_data

def getSeuil(l):
    return 1

def match(word, bk): 
    l = len(word)
    seuil = getSeuil(l)
    if l > 1:
        word = word.lower() 
    flag = -1 

    if (len(word)<=2):
        flag = 0
        return word,flag
    
    d,word_ = bk.search(seuil, word)
    if d <= seuil:
        if d==0:
            flag = 0
        else:
            flag = 1
        return word_, flag
            
    return word,flag

def rebuild(origin_data, corrected_data):
    p = re.compile(r"[^A-Za-z]+")
    reconstruct = []
    for i in range(len(origin_data)):
        w = ''
        word = corrected_data[i]
        conn = p.findall(origin_data[i])
        check = p.split(origin_data[i])
        new_name = ''
        min_len = min(len(word), len(conn))
        if check[0] == '':
            for k in range(min_len):
                new_name = new_name + conn[k] + word[k]
            if len(conn) > len(word):
                new_name = new_name + conn[min_len]
        else:
            for k in range(min_len):
                new_name = new_name + word[k] + conn[k]
            if len(word) > len(conn):
                new_name = new_name + word[min_len]
        w = new_name
        reconstruct.append(w)
    return reconstruct

def run(data, bk):
    corrected_data = []
    for x in data:
        corrected_x = []
        for word in x:
            corrected_word, flag = match(word, bk)
            corrected_x.append(corrected_word)
        corrected_data.append(corrected_x)
    return corrected_data

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    
    args = parser.parse_args()
    
    with open("bkTree.pkl",'rb') as f:
        bka = pkl.load(f)
    data, origin_data = loadData(args.input)
    corrected_data = run(data, bka)
    reconstruct = rebuild(origin_data, corrected_data)
    with open(args.output,"w") as f:
        f.write('\n'.join(reconstruct))

