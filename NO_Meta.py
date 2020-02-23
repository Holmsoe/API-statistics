import requests
import json


class NorwayMeta():
    def __init(self):
        pass
        
    def MainTables(self):
        Hoved = 'https://data.ssb.no/api/v0/en/table/'
        r = requests.post(url = Hoved)
        HovedTabel = r.text
        return HovedTabel
       
    def TradeTables(self):
        Under = 'https://data.ssb.no/api/v0/en/table/ut'
        r = requests.post(url = Under)
        UnderTabel = r.text
        return UnderTabel
        
    def ForeignTradeTables(self):
        ForeignTrade = 'https://data.ssb.no/api/v0/en/table/ut/ut02/muh'
        r = requests.post(url = ForeignTrade)
        ForeignTradeTabel = r.text 
        return ForeignTradeTabel
        
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
      
minstat=NorwayMeta()    
  
#print(minstat.MainTables())      
#print(minstat.TradeTables())       
#print(minstat.ForeignTradeTables())
        
metadata=minstat.ForeignTradeMetaDict()

#level1.   key,variables
#Level2.1   metadata['variables'][0] - products: code,text,values,valueTexts,elimination
#Level2.2   metadata['variables'][1] - import/export: code,text,values,valueTexts
#Level2.3   metadata['variables'][2] - country: code,text,values,valueTexts,elimination
#Level2.4   metadata['variables'][3] - time: code,text,values,valueTexts


 
#print(minstat.CountryCodeNameDict(metadata))        
#print(minstat.CountryNameCodeDict(metadata))
#print(minstat.ProductCodeNameDict(metadata))        
#print(minstat.ProductNameCodeDict(metadata))

#Example
#landetabel=minstat.CountryCodeNameDict(metadata)
#print(landetabel["DE"])
#produkttabel=minstat.ProductCodeNameDict(metadata)
#print(produkttabel["25221000"])
#print(produkttabel["25222000"])
#print(produkttabel["25182000"])









