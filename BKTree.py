#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 22:28:22 2018

@author: longzhan
"""

#treelib的每个节点id和tag都是单词的字符串，data是该词与父节点间的编辑距离
from treelib import Tree
import Levenshtein

class BKT(object):
    def __init__(self,wordlist):  #初始化，输入字典
        self.wordlist=wordlist
        self.BKtree=Tree()
        self.BKtree.create_node(self.wordlist[0],self.wordlist[0]) 
        self.result=[] #储存候选正确词
        self.result_dist=[] #储存距离
        
    def buildBK(self): #建树
        for i in range(1,len(self.wordlist)):
            currentFather=self.BKtree.get_node(self.wordlist[0])  #以根节点作为初始父节点
            self.insert(self.wordlist[i],currentFather)    
            
    def insert(self,word,currentFather):  #插入新词
        #print(currentFather.identifier)
        dist=Levenshtein.distance(word,currentFather.identifier)
        mark=0 
        for ID in currentFather.fpointer: 
            if self.BKtree.get_node(ID).data==dist:
                father=self.BKtree.get_node(ID)
                mark=1
                self.insert(word,father)
        if mark==0: #mark为0，说明没有子树与当前父节点的距离为插入词到父节点的距离，要创造新节点
            try:  #如果插入词已经存在，这步会报错，所以这里用了try结构
                self.BKtree.create_node(word,word,parent=currentFather,data=dist)
            except:
                pass
            
            
    def search(self,n,word): #搜索
        self.result=[] #先将候选集清空
        self.result_dist=[]
        currentFather=self.BKtree.get_node(self.wordlist[0])
        self.find(n,word,currentFather)
        if(len(self.result))>0:
            d = min(self.result_dist)
            index = self.result_dist.index(d)
            word = self.result[index]
            return d,word
        else:
            return len(word),word
        
    
        
    def find(self,n,word,currentFather):
        dist=Levenshtein.distance(word,currentFather.identifier)
        if dist<=n: #判断父节点是不是与错词的编辑距离小于n，是的话就加入候选集
            self.result.append(currentFather.identifier) 
            self.result_dist.append(dist)
            
        for ID in currentFather.fpointer:
            if (self.BKtree.get_node(ID).data<=dist+n) and (self.BKtree.get_node(ID).data>=dist-n):
                father=self.BKtree.get_node(ID)
                self.find(n,word,father)  #一步步往下走，直到叶节点停止