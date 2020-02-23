import NO_Meta as nn
import requests
import pandas as pd
from pyjstat import pyjstat
import matplotlib.pyplot as plt
       
class NorwayTrade():
    
    def __init__(self,periode,vare):
        self.periode=periode
        self.vare=[vare]
        #self.countries=["SE","DK","FI"]
        self.countries=["*"]
        
    def GetTable(self):
       
        impexp=["1","2"]
        countries=['DK',"SE"]
        enhed=["Mengde1","Verdi"]        
        
        NOstat = 'https://data.ssb.no/api/v0/en/table/08799'

        #API query
        data = {  "query": [    
                {"code": "Varekoder","selection": {"filter": "item","values": self.vare}},
                {"code": "ImpEks","selection": {"filter": "item","values": impexp}}, #2 = export
                {"code": "Land","selection": {"filter": "all","values": self.countries}},
                {"code": "ContentsCode","selection": {"filter": "item","values": enhed}},
                {"code": "Tid","selection": {"filter": "item","values": self.periode}}
                ],
            "response": {"format": "json-stat2"}
                }


        resultat = requests.post(NOstat, json = data)
        #print(resultat.text)

        dataset = pyjstat.Dataset.read(resultat.text)
        df = dataset.write('dataframe')
        
        return df
    
    
    def MakeTable(self,df):
        
        #for col in df.columns: 
        #    print(col) 
       
        #df=df[["month","country","value","contents"]]  
        #print(df)
        
        #Change header to first line
        new_header = df.iloc[0] 
        df = df[1:]
        df.columns = ["VARE","EXPIMP","LAND","ENHED","TID","VALUE"]
        df = df[df.astype(str).ne('None').all(1)]
        #print(df)
        
        minstat=nn.NorwayMeta()    
        self.metadata=minstat.ForeignTradeMetaDict()
        self.lande=minstat.CountryNameCodeDict(self.metadata)
        self.varer=minstat.ProductNameCodeDict(self.metadata)
        
        #print(self.lande['Finland'])
        
        
        def landekode(x):
            try:
                kode=self.lande[x]
            except:
                kode="ugh"              
            return kode  
        
        def varekode(x):
            try:
                kode=self.varer[x]
            except:
                kode="ugh"              
            return kode 
        
        df['LAND']=df['LAND'].apply(landekode)
        #df['VARE']=df['VARE'].apply(varekode)
        #print(df)
        
        df[["VALUE"]] = df[["VALUE"]].apply(pd.to_numeric, errors='coerce')
        df = pd.pivot_table(df, values='VALUE',index=['EXPIMP','LAND','TID'],columns=['ENHED'])
        df.reset_index(level=['EXPIMP','LAND','TID'], inplace=True)
        #print(df)
        df.columns=['EXPIMP','LAND','TID','TON','VALUE']
        df[["TON"]] = df[["TON"]].apply(pd.to_numeric, errors='coerce')
        df[["VALUE"]] = df[["VALUE"]].apply(pd.to_numeric, errors='coerce')
        df.loc[df['EXPIMP'] == 'Exports','FROM'] = 'NO'
        df.loc[df['EXPIMP'] == 'Imports','FROM'] = df['LAND']
        df.loc[df['EXPIMP'] == 'Exports','TO'] = df['LAND']
        df.loc[df['EXPIMP'] == 'Imports','TO'] = 'NO'
        df['TON']=df['TON']/1000
        df['VALUE']=df['VALUE']/1000
        df=df[["TID","FROM","TO","TON","VALUE"]]
        #print(df)   
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
        exptabel=db.loc[(db['TO'].isin(countrylist)) & (db['FROM']=='NO')]
        
        #import
        df=db.groupby("FROM")
        df=df["TON"].sum()
        df=df.to_frame()
        df=df.loc[df["TON"]>limit]    
        df=df.reset_index()
        #print(df)
        countrylist=df['FROM'].tolist()
        #print(countrylist)
        imptabel=db.loc[(db['FROM'].isin(countrylist)) & (db['TO']=='NO')]
        
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
        df=df.loc[df['FROM']=='NO']
        df=df.round({'TON':1,'VALUE':0})
        dfplot=df.pivot(index='AAR', columns='TO', values='TON')
        dfplot.to_excel('NOexport.xls')
        print(dfplot)
        
        latextabel=dfplot.to_latex(index=False)
        with open('NOexpTabel.tex', 'w') as f: 
            f.write(latextabel)

        fig, ax = plt.subplots()
        ax.plot(dfplot)            
        fig.savefig('NOexpGraf.pdf')

        
    def ShowImportPlot(self,df):
        df=df.loc[df['TO']=='NO']
        df=df.round({'TON':1,'VALUE':0})
        dfplot=df.pivot(index='AAR',columns='FROM', values='TON')
        dfplot.to_excel('NOimport.xls')
        print(dfplot)
        
        latextabel=dfplot.to_latex(index=False)
        with open('NOimpTabel.tex', 'w') as f: 
            f.write(latextabel)

        fig, ax = plt.subplots()
        ax.plot(dfplot)            
        fig.savefig('NOimpGraf.pdf')


