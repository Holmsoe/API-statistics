import requests
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

class SwedenTrade():
    
    def __init__(self,periode,vare):
        self.periode=periode
        self.vare=[vare]
        #self.countries=["NO","DK","FI"]
        self.countries=["*"]
                
    
    def GetExportTable(self):
        Expenhed=["HA0201H1","HA0201H2"] #"HA0201H1"=tons,"HA0201H2"=1000 SEK
        SeExpStat = 'https://api.scb.se/OV0104/v1/doris/en/ssd/HA/HA0201/HA0201B/ExpTotalKNMan'
        ExpQuery = {  
                "query": 
                    [
                    {"code": "VarugruppKN","selection": {"filter": "item","values": self.vare}},
                    {"code": "Handelspartner","selection": {"filter": "all","values": self.countries}},
                    {"code": "ContentsCode","selection": {"filter": "item","values": Expenhed}},
                    {"code": "Tid","selection": {"filter": "item","values": self.periode}},   
                    ],  
                    "response": {"format": "json"}}
        r = requests.post(SeExpStat,json=ExpQuery)
        d = json.loads(r.content.decode('utf-8-sig'))
        return d
        
    def GetImportTable(self): 

        Impenhed=["HA0201N1","HA0201N2"]  #"HA0201N1"=tons,"HA0201N2"=1000 SEK
        SeImpStat = 'https://api.scb.se/OV0104/v1/doris/en/ssd/HA/HA0201/HA0201B/ImpTotalKNMan'            
        ImpQuery = {  
                "query": 
                    [
                    {"code": "VarugruppKN","selection": {"filter": "item","values": self.vare}},
                    {"code": "Handelspartner","selection": {"filter": "all","values": self.countries}},
                    {"code": "ContentsCode","selection": {"filter": "item","values": Impenhed}},
                    {"code": "Tid","selection": {"filter": "item","values": self.periode}},   
                    ],  
                    "response": {"format": "json"}} 
            
        r = requests.post(SeImpStat,json=ImpQuery)
        d = json.loads(r.content.decode('utf-8-sig'))
        return d
    
    
    def MakeExportTable(self,d):
        
        df=[]
        for line in d["data"]:
            keylist=line['key']
            for value in line["values"]:
                keylist.append(value)
            df.append(keylist)

        df=pd.DataFrame(df)
        df=df.replace(np.nan,0)
        
        #specielt for export
        df.columns=["VARE","TO","TID","TON","VALUE"]
        df["FROM"]="SE"
        #===================  
        
        df=df[["TID","FROM","TO","TON","VALUE"]]
        df[["TON"]] = df[["TON"]].apply(pd.to_numeric, errors='coerce')
        df[["VALUE"]] = df[["VALUE"]].apply(pd.to_numeric, errors='coerce')

        return df
    
    def MakeImportTable(self,d):
        
        df=[]
        for line in d["data"]:
            keylist=line['key']
            for value in line["values"]:
                keylist.append(value)
            df.append(keylist)
        df=pd.DataFrame(df)
        df=df.replace(np.nan,0)
        
        #specielt for import
        df.columns=["VARE","FROM","TID","TON","VALUE"]
        df["TO"]="SE"
        #=================== 
            
        df=df[["TID","FROM","TO","TON","VALUE"]]
        df[["TON"]] = df[["TON"]].apply(pd.to_numeric, errors='coerce')
        df[["VALUE"]] = df[["VALUE"]].apply(pd.to_numeric, errors='coerce')

        return df
    
    def CutCountries(self,db,limit):
        #eksport
        df=db.groupby("TO")
        df=df["TON"].sum()
        df=df.to_frame()
        df=df.loc[df["TON"]>limit]    
        df=df.reset_index()
        #print(df)
        countrylist=df['TO'].tolist()
        exptabel=db.loc[(db['TO'].isin(countrylist)) & (db['FROM']=='SE')]
        
        #import
        df=db.groupby("FROM")
        df=df["TON"].sum()
        df=df.to_frame()
        df=df.loc[df["TON"]>limit]    
        df=df.reset_index()
        #print(df)
        countrylist=df['FROM'].tolist()
        #print(countrylist)
        imptabel=db.loc[(db['FROM'].isin(countrylist)) & (db['TO']=='SE')]
        
        nytabel=pd.concat([exptabel,imptabel])
        return nytabel
        
    def Yearly(self,df):
        def aar(x):
            return x[0:4]
        df['AAR']=df['TID'].apply(aar)
        #print(nytabel)
        aartabel=df.groupby(['AAR','FROM','TO'])[['TON','VALUE']].sum()
        aartabel.reset_index(level=['AAR','FROM','TO'], inplace=True)
        return aartabel
    
    def ShowExportPlot(self,df):
        df=df.loc[(df['FROM']=='SE') & (df['TO']!='TOT')]
        df=df.round({'TON':1,'VALUE':0})
        dfplot=df.pivot(index='AAR', columns='TO', values='TON')
        dfplot.to_excel('SEexport.xls')
        print(dfplot)

        latextabel=dfplot.to_latex(index=False)
        with open('SEexpTabel.tex', 'w') as f: 
            f.write(latextabel)

        fig, ax = plt.subplots()
        ax.plot(dfplot)            
        fig.savefig('SEexpGraf.pdf')
        
        
    def ShowImportPlot(self,df):
        df=df.loc[(df['TO']=='SE') & (df['FROM']!='TOT')]
        df=df.round({'TON':1,'VALUE':0})
        dfplot=df.pivot(index='AAR',columns='FROM', values='TON')
        dfplot.to_excel('SEimport.xls')
        print(dfplot)
        
        latextabel=dfplot.to_latex(index=False)
        with open('SEimpTabel.tex', 'w') as f: 
            f.write(latextabel)

        fig, ax = plt.subplots()
        ax.plot(dfplot)            
        fig.savefig('SEimpGraf.pdf')

