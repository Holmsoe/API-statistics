import requests
import json


class NorwayMeta():
    def __init(self):
        pass

    def MainTables(self):
        Hoved = 'https://data.ssb.no/api/v0/en/table/'
        r = requests.get(url = Hoved)
        HovedTabel = r.text
        d = json.loads(HovedTabel)
        return d      
      
    def TradeTables(self):
        Under = 'https://data.ssb.no/api/v0/en/table/ut'
        r = requests.get(url = Under)
        UnderTabel = r.text
        d = json.loads(UnderTabel)
        return d
        
    def ForeignTradeTables(self):
        ForeignTrade = 'https://data.ssb.no/api/v0/en/table/ut/ut02/muh'
        r = requests.get(url = ForeignTrade)
        ForeignTradeTabel = r.text 
        d = json.loads(ForeignTradeTabel)
        return d
        
    def ForeignTradeMetaDict(self):
        # NBNB samme format som data query. men bruget get istedet for post
        KNA = 'https://data.ssb.no/api/v0/en/table/08799'
        r = requests.get(url = KNA)
        KNATabel = r.text
        d = json.loads(KNATabel)
        return d   
         
    def CountryNameCodeDict(self,d):
        dict_lande=d['variables'][2]
        landekode=dict_lande['values']
        landenavn=dict_lande['valueTexts']
        dict_lande=dict(zip(landenavn,landekode))
        return dict_lande
        
    def CountryCodeNameDict(self,d):
        dict_lande=d['variables'][2]
        landekode=dict_lande['values']
        landenavn=dict_lande['valueTexts']
        dict_lande=dict(zip(landekode,landenavn))
        return dict_lande
        
    def ProductCodeNameDict(self,d):
        dict_varer=d['variables'][0]     
        varenumre=dict_varer['values']
        varenavne=dict_varer['valueTexts']
        dict_varer=dict(zip(varenumre,varenavne))
        return dict_varer
        
    def ProductNameCodeDict(self,d):
        dict_varer=d['variables'][0]   
        varenumre=dict_varer['values']
        varenavne=dict_varer['valueTexts']
        dict_varer=dict(zip(varenavne,varenumre))
        return dict_varer 
      

'''
#MainTables
minstat=NorwayMeta()  
mintabel=minstat.MainTables()  
#Tabeloversigt med tabelkode og navn
for item in mintabel: print('\n',item['id'],item['text']) 
'''

'''
#Trade tables
#kode 'ut' fra MainTables
minstat=NorwayMeta()  
mintabel=minstat.TradeTables()  
#Tabeloversigt med tabelkode og navn
for item in mintabel: print('\n',item['id'],item['text']) 
'''

'''
#Foreign trade tables
#kode 'ut02' fra TradeTables
minstat=NorwayMeta()  
mintabel=minstat.ForeignTradeTables()  
#Tabeloversigt med tabelkode og navn
for item in mintabel: print('\n',item['id'],item['text']) 
'''

'''
#Foreign trade external trade
#kode '08799' fra TradeTables
minstat=NorwayMeta()  
mintabel=minstat.ForeignTradeMetaDict() 
 
#Tabeloversigt med produktkode og navn
#Level2.1   mintabel['variables'][0] - products: code,text,values,valueTexts,elimination
#print(mintabel['variables'][0])
#print(mintabel['variables'][0]['values'])
#print(mintabel['variables'][0]['valueTexts'])

#Tabeloversigt med importkode, navn og eksportkode og navn
#Level2.2   mintabel['variables'][1] - import/export: code,text,values,valueTexts
#print(mintabel['variables'][1])
#print(mintabel['variables'][1]['values'])
#print(mintabel['variables'][1]['valueTexts'])

#Tabeloversigt med landekode og navn
#Level2.3   mintabel['variables'][2] - country: code,text,values,valueTexts,elimination
#print(mintabel['variables'][2])
#print(mintabel['variables'][2]['values'])
#print(mintabel['variables'][2]['valueTexts'])

#Tabeloversigt med tidkode og navn
#Level2.4   mintabel['variables'][3] - enhed: code,text,values,valueTexts
#print(mintabel['variables'][3])
#print(mintabel['variables'][3]['values'])
#print(mintabel['variables'][3]['valueTexts'])
'''

 
#print(minstat.CountryCodeNameDict(mintabel))        
#print(minstat.CountryNameCodeDict(mintabel))
#print(minstat.ProductCodeNameDict(mintabel))        
#print(minstat.ProductNameCodeDict(mintabel))

#Example
#landetabel=minstat.CountryCodeNameDict(metadata)
#print(landetabel["DE"])
#produkttabel=minstat.ProductCodeNameDict(metadata)
#print(produkttabel["25221000"])
#print(produkttabel["25222000"])
#print(produkttabel["25182000"])









