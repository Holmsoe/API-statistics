itorregistrete bank
import requests
import json

class SwedenMeta():
    def __init(self):
        pass
        
    def MainTables(self):
        SeHoved = 'https://api.scb.se/OV0104/v1/doris/en/ssd'
        r = requests.post(url = SeHoved)
        HovedTabel = r.text
        return HovedTabel
       
    def TradeTables(self):
        # HA er "Trade in goods and services"
        SeUnder = 'https://api.scb.se/OV0104/v1/doris/en/ssd/HA'
        r = requests.post(url = SeUnder)
        UnderTabel = r.text
        return UnderTabel
        
    def ForeignTradeTables(self):
        # HA0201 er "Foreign trade - exports and imports of goods"
        SeForeignTrade = 'https://api.scb.se/OV0104/v1/doris/en/ssd/HA/HA0201'
        r = requests.post(url = SeForeignTrade)
        ForeignTradeTabel = r.text 
        return ForeignTradeTabel
        
    def ForeignTradeKNATables(self):
        # HA0201 er "Foreign trade - exports and imports of goods"
        SeKNA = 'https://api.scb.se/OV0104/v1/doris/en/ssd/HA/HA0201/HA0201B'
        r = requests.post(url = SeKNA)
        KNATabel = r.text
        return KNATabel
    
    def ExpTabelMetaDict(self):
        SEexpmeta = 'https://api.scb.se/OV0104/v1/doris/en/ssd/HA/HA0201/HA0201B/ExpTotalKNMan'
        r = requests.get(SEexpmeta)
        metadata=r.text
        d = json.loads(metadata)
        return d
    
    def ImpTabelMetaDict(self):
        SEimpmeta = 'https://api.scb.se/OV0104/v1/doris/en/ssd/HA/HA0201/HA0201B/ImpTotalKNMan'
        r = requests.get(SEimpmeta)
        metadata=r.text
        d = json.loads(metadata)
        return d
          
    def CountryNameCodeDict(self,d):
        dict_lande=d['variables'][1]
        landekode=dict_lande['values']
        landenavn=dict_lande['valueTexts']
        dict_lande=dict(zip(landenavn,landekode))
        return dict_lande
        
    def CountryCodeNameDict(self,d):
        dict_lande=d['variables'][1]
        landekode=dict_lande['values']
        landenavn=dict_lande['valueTexts']
        dict_lande=dict(zip(landekode,landenavn))
        return dict_lande
        
    def ProductCodeNameDict(self,d):
        dict_varer=d['variables'][0]    #variables: varer, land, exp/imp, år 
        varenumre=dict_varer['values']
        varenavne=dict_varer['valueTexts']
        dict_varer=dict(zip(varenumre,varenavne))
        return dict_varer
        
    def ProductNameCodeDict(self,d):
        dict_varer=d['variables'][0]    #variables: varer, land, exp/imp, år 
        varenumre=dict_varer['values']
        varenavne=dict_varer['valueTexts']
        dict_varer=dict(zip(varenavne,varenumre))
        return dict_varer 
      
#minstat=SwedenMeta()       
#print(minstat.MainTables())
      
#print(minstat.TradeTables())
       
#print(minstat.ForeignTradeTables())
        
#print(minstat.ForeignTradeKNATables())

#exportmeta=minstat.ExpTabelMetaDict() 
#print(exportmeta) 

#print(minstat.CountryCodeNameDict(exportmeta))        
#print(minstat.CountryNameCodeDict(exportmeta))
#print(minstat.ProductCodeNameDict(exportmeta))        
#print(minstat.ProductNameCodeDict(exportmeta))

#importmeta=minstat.ImpTabelMetaDict() 
#print(importmeta) 
#print(minstat.CountryCodeNameDict(importmeta))        
#print(minstat.CountryNameCodeDict(importmeta))
#print(minstat.ProductCodeNameDict(importmeta))        
#print(minstat.ProductNameCodeDict(importmeta))

#Eksempel - Find landekode fra exp register der svarer til landet "Norway"
#exportmeta=minstat.ExpTabelMetaDict() #metatabel
#landetabel=minstat.CountryNameCodeDict(exportmeta)  #lande dict med landenavn som indgangskode
#kode=landetabel["Norway"]
#print("Svaret er:",kode)




