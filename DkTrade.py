import DK_Meta as dd
import requests
import pandas as pd
import matplotlib.pyplot as plt
              
class DenmarkTrade():

    def __init__(self,periode,vare):
        self.periode=periode
        self.vare=[vare]
        #self.countries=["SE","NO","FI"]    
        self.countries=["*"]
   

    def GetOldTable(self):
        
        period=[month for month in self.periode if int(month[:4])<2016]
        statTabel="kn8m"
        
        gammeltabel=self.GetTable(period,statTabel)
        return gammeltabel
        
    
    def GetNewTable(self):
        
        period=[month for month in self.periode if int(month[:4])>=2016]
        statTabel="kn8mest"
        nytabel=self.GetTable(period,statTabel)
        return nytabel
    
    
    def GetTable(self,period,statTabel):
        
        enhed=["98","99"]
        expimp=["1","2"]

        DkStat = "https://api.statbank.dk/v1/data"
    
        data =  {
                "table": statTabel,
                "format": "CSV",
                "delimiter": "Semicolon",
                "allowVariablesInHead": True,
                "variables": [
                {"code": "vare","values": self.vare},
                {"code": "land","values":self.countries},
                {"code": "enhed","values": enhed},
                {"code": "tid","values": period},
                {"code": "indud","values":expimp},
                ] 
                }
        
        r = requests.post(url = DkStat,json=data)         
        r=r.text.split("\r\n")
        d=[line.split(";") for line in r]          
        return d
        
    
    def MakeTable(self,d):
        
        df=pd.DataFrame(d)

        #Change header to first line
        new_header = df.iloc[0] 
        df = df[1:]
        df.columns = ["VARE","LAND","ENHED","TID","INDUD","INDHOLD"]
        df = df[df.astype(str).ne('None').all(1)]

        #Metadata indeholder lister med koder og navne for ex. lande ('SE'='Sverige') og produkter ('varenummer' =>varenavn)
        #Vi laver en instance af metadataklasse
        minstat=dd.DenmarkMeta()  
        #Vi henter hele tabellen
        self.metadata=minstat.ForeignTradeMetaDict()
        #Vi trækker data for lande ud
        self.lande=minstat.CountryNameCodeDict(self.metadata)
        #Vi trækker data for varer ud
        #self.varer=minstat.ProductNameCodeDict(self.metadata)      
       
        def landekode(x):
            try:
                kode=self.lande[x]
            except:
                kode="fejl"              
            return kode  
        '''        
        def varekode(x):
            try:
                kode=self.varer[x]
            except:
                kode="ugh"              
            return kode 
        '''
        #Vi skifter landenavn ud med kode
        df['LAND']=df['LAND'].apply(landekode)
        #df['VARE']=df['VARE'].apply(varekode)
        #print(df)
        
        df[["INDHOLD"]] = df[["INDHOLD"]].apply(pd.to_numeric, errors='coerce')
        df = pd.pivot_table(df, values='INDHOLD',index=['INDUD','LAND','TID'],columns=['ENHED'])
        df.reset_index(level=['INDUD','LAND','TID'], inplace=True)
        df.columns=['INDUD','LAND','TID','TON','VALUE']
        
        df[["TON"]] = df[["TON"]].apply(pd.to_numeric, errors='coerce')
        df[["VALUE"]] = df[["VALUE"]].apply(pd.to_numeric, errors='coerce')
        #print(df)
        df.loc[df['INDUD'] == 'Eksport','FROM'] = 'DK'
        df.loc[df['INDUD'] == 'Import','FROM'] = df['LAND']
        df.loc[df['INDUD'] == 'Eksport','TO'] = df['LAND']
        df.loc[df['INDUD'] == 'Import','TO'] = 'DK'
        df['TON']=df['TON']/1000
        df['VALUE']=df['VALUE']
        df=df[["TID","FROM","TO","TON","VALUE"]]
        
        
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
        exptabel=db.loc[(db['TO'].isin(countrylist)) & (db['FROM']=='DK')]
        
        #import
        df=db.groupby("FROM")
        df=df["TON"].sum()
        df=df.to_frame()
        df=df.loc[df["TON"]>limit]    
        df=df.reset_index()
        #print(df)
        countrylist=df['FROM'].tolist()
        #print(countrylist)
        imptabel=db.loc[(db['FROM'].isin(countrylist)) & (db['TO']=='DK')]
        
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
        try:
            df=df.loc[(df['FROM']=='DK') & (df['TO']!='TOT')]
            df=df.round({'TON':1,'VALUE':0})
            dfplot=df.pivot(index='AAR', columns='TO', values='TON')
            
            '''
            dfplot.to_excel('DKexport.xls')
            print(dfplot)

            latextabel=dfplot.to_latex(index=False)
            with open('DKexpTabel.tex', 'w') as f: 
                f.write(latextabel)

            fig, ax = plt.subplots()
            ax.plot(dfplot)            
            fig.savefig('DKexpGraf.pdf')
            '''
            return dfplot
        except:
            pass
        
    def ShowImportPlot(self,df):
        try:
            df=df.loc[(df['TO']=='DK')  & (df['FROM']!='TOT')]
            df=df.round({'TON':1,'VALUE':0})
            dfplot=df.pivot(index='AAR',columns='FROM', values='TON')
            
            
            dfplot.to_excel('DKimport.xls')
            print(dfplot)
        
            latextabel=dfplot.to_latex(index=False)
            with open('DKimpTabel.tex', 'w') as f: 
                f.write(latextabel)

            fig, ax = plt.subplots()
            ax.plot(dfplot)            
            fig.savefig('DKimpGraf.pdf') 
        except:
            pass
