import requests
import json

class DenmarkMeta():
    def __init(self):
        pass
        
    def MainTables(self):
        Hoved = 'https://api.statbank.dk/v1/subjects'
        r = requests.post(url = Hoved)
        HovedTabel = r.text
        return HovedTabel
       
    def TradeTables(self):
        Under = 'https://api.statbank.dk/v1/subjects'
        Undertabeldata={"subjects": ["13"],"includeTables": True,"recursive": True}
        r = requests.post(url = Under,json=Undertabeldata)
        UnderTabel = r.text
        return UnderTabel       
       
    def ForeignTradeMetaDict(self):
        DkStat = "http://api.statbank.dk/v1/tableinfo"
        DkData= {"table": "kn8y"}
        r = requests.post(url = DkStat,json=DkData)
        KNATabel = r.text
        d = json.loads(KNATabel)
        return d 
         
    def CountryNameCodeDict(self,d):
        list_lande=d['variables'][2]['values']
        landekode=[]
        landenavn=[]
        for item in list_lande:
            landekode.append(item['id'])
            landenavn.append(item['text'])
        dict_lande=dict(zip(landenavn,landekode))
        return dict_lande
        
    def CountryCodeNameDict(self,d):
        list_lande=d['variables'][2]['values']
        landekode=[]
        landenavn=[]
        for item in list_lande:
            landekode.append(item['id'])
            landenavn.append(item['text'])
        dict_lande=dict(zip(landekode,landenavn))
        return dict_lande
        
    def ProductCodeNameDict(self,d):
        list_varer=d['variables'][1]['values']    
        varekode=[]
        varenavn=[]
        for item in list_varer:
            varekode.append(item['id'])
            varenavn.append(item['text'])
        dict_varer=dict(zip(varekode,varenavn))
        return dict_varer
        
    def ProductNameCodeDict(self,d):
        list_varer=d['variables'][1]['values']    
        varekode=[]
        varenavn=[]
        for item in list_varer:
            varekode.append(item['id'])
            varenavn.append(item['text'])
        dict_varer=dict(zip(varenavn,varekode))
        return dict_varer 
'''      
minstat=DenmarkMeta()    
metadata=minstat.ForeignTradeMetaDict()
lande=minstat.CountryCodeNameDict(metadata)
print(lande["DE"])
varer=minstat.ProductCodeNameDict(metadata)
print(varer['25221000'])
'''








