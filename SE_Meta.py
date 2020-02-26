import requests
import json

class SwedenMeta():
    def __init(self):
        pass
        
    def MainTables(self):
        SeHoved = 'https://api.scb.se/OV0104/v1/doris/en/ssd'
        r = requests.post(url = SeHoved)
        HovedTabel = r.text
        d = json.loads(HovedTabel)
        return d
       
    def TradeTables(self):
        # HA er "Trade in goods and services"
        SeUnder = 'https://api.scb.se/OV0104/v1/doris/en/ssd/HA'
        r = requests.post(url = SeUnder)
        UnderTabel = r.text
        d = json.loads(UnderTabel)
        return d
        
    def ForeignTradeTables(self):
        # HA0201 er "Foreign trade - exports and imports of goods"
        SeForeignTrade = 'https://api.scb.se/OV0104/v1/doris/en/ssd/HA/HA0201'
        r = requests.post(url = SeForeignTrade)
        ForeignTradeTabel = r.text 
        d = json.loads(ForeignTradeTabel)
        return d
        
    def ForeignTradeKNATables(self):
        # HA0201 er "Foreign trade - exports and imports of goods"
        SeKNA = 'https://api.scb.se/OV0104/v1/doris/en/ssd/HA/HA0201/HA0201B'
        r = requests.post(url = SeKNA)
        KNATabel = r.text
        d = json.loads(KNATabel)
        return d
    
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

'''
#Main tables      
minstat=SwedenMeta()       
mintabel=minstat.MainTables()
for item in mintabel: print('\n',item['id'],item['text'])
'''

#============================================================

'''
#Trade tables      
# use id=HA fra MainTables
minstat=SwedenMeta()       
mintabel=minstat.TradeTables()
for item in mintabel: print('\n',item['id'],item['text'])
'''

#============================================================

'''
#Foreign Trade tables      
# use id=HA0201 fra TradeTable
minstat=SwedenMeta()       
mintabel=minstat.ForeignTradeTables()
for item in mintabel: print('\n',item['id'],item['text'])
'''

#============================================================

'''
#Foreign Trade tables combined nomenclature      
# use id=HA0201B fra ForeignTradeTable
minstat=SwedenMeta()       
mintabel=minstat.ForeignTradeKNATables()
for item in mintabel: print('\n',item['id'],item['text'])
'''

#============================================================

'''
#Export 8 digit commodity code 
#variabel oversigt     
# use id= ExpTotalKNMan fra TradeTable combined nomenclature
minstat=SwedenMeta()       
mintabel=minstat.ExpTabelMetaDict()
for item in mintabel['variables']: print('\n',item['code'])
'''

#============================================================

'''
#Variabel export indhold
minstat=SwedenMeta()       
mintabel=minstat.ExpTabelMetaDict()
# VarugruppKN (varegruppe) Handelspartner (land) ContentsCode (enhed) Tid (årmåned)

#VarugruppKN
#print(mintabel['variables'][0])
#'values' = varekode
#'valueTexts' = varenavn

#Handelspartner
#print(mintabel['variables'][1])
#'values' = landekode
#'valueTexts' = land

#Enhed
#print(mintabel['variables'][2])
#values     valueTexts
#HA0201H1 = 1000 kg
#HA0201H2 = 1000 sek
#HA0201H3 = supplementary unit 

#Månedår
#print(mintabel['variables'][3])
#'values' = månedkode
#'valueTexts' = måned (samme som månedkode)
'''

#============================================================

'''
#Import 8 digit commodity code 
#variabel oversigt     
# use id= ImpTotalKNMan fra TradeTable combined nomenclature
minstat=SwedenMeta()       
mintabel=minstat.ImpTabelMetaDict()
for item in mintabel['variables']: print('\n',item['code'])
'''

#============================================================

'''
#Variabel import indhold
minstat=SwedenMeta()       
mintabel=minstat.ImpTabelMetaDict()
# VarugruppKN (varegruppe) Handelspartner (land) ContentsCode (enhed) Tid (årmåned)

#VarugruppKN
#print(mintabel['variables'][0])
#'values' = varekode
#'valueTexts' = varenavn

#Handelspartner=land
#print(mintabel['variables'][1])
#'values' = landekode
#'valueTexts' = land

#Enhed
#print(mintabel['variables'][2])
#values     valueTexts
#HA0201H1 = 1000 kg
#HA0201H2 = 1000 sek
#HA0201H3 = supplementary unit 

#Månedår
#print(mintabel['variables'][3])
#'values' = månedkode
#'valueTexts' = måned (samme som månedkode)
'''

#============================================================

'''
#Export Country/Product dictionaries 
minstat=SwedenMeta()
exportmeta=minstat.ExpTabelMetaDict() 

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
'''


'''
#Eksempel - Find landekode fra exp register der svarer til landet "Norway"
minstat=SwedenMeta()
exportmeta=minstat.ExpTabelMetaDict() #metatabel
landetabel=minstat.CountryNameCodeDict(exportmeta)  #lande dict med landenavn som indgangskode
kode=landetabel["Norway"]
print("Svaret er:",kode)
'''



