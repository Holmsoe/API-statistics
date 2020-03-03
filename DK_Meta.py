import requests
import json

class DenmarkMeta():
    def __init(self):
        pass
        
    def MainTables(self):
        '''Vi henter liste over hovedstatistikker
        
        Tabellen er en liste af dictionaries per hovedstatstik
        Keys i dictionary er: 'id','description','active',hasSubjects','subjects'
        'id' er nummer af hovedstatistik
        'description er navn/beskrivelse
        
        d[0]['id'] er id nummer for første statistik
        d[0]['description'] er navn for første statistik
        '''
        
        Hoved = 'https://api.statbank.dk/v1/subjects'
        r = requests.post(url = Hoved)
        HovedTabel = r.text
        d = json.loads(HovedTabel)
        return d
       
    def TradeTables(self):
        '''Vi henter liste over understatistikker i hovedstatistik 13 = udenrigshandel
        Der er et element i tabellen        d[0]
        
        Der er to undertabeller. udenrigshandel og betalingsbalance
        d[0]['subjects'][0] er udenrigshandel
        d[0]['subjects'][1] er betalingsbalance
        
        Der er to undertabeller. udenrigshandel med varer og udenrigshandel med tjenester
        d[0]['subjects'][0]['subjects'][0] er varer
        d[0]['subjects'][0]['subjects'][1] er tjenester
        
        Liste over tabeller med udenrigshandel for varer
        d[0]['subjects'][0]['subjects'][0]['tables'] 
        
        #Liste med tabelnummer og navn
        d[0]['subjects'][0]['subjects'][0]['tables']['id']
        d[0]['subjects'][0]['subjects'][0]['tables']['text']
        
        '''
        
        Under = 'https://api.statbank.dk/v1/subjects'
        Undertabeldata={"subjects": ["13"],"includeTables": True,"recursive": True}
        r = requests.post(url = Under,json=Undertabeldata)
        UnderTabel = r.text
        d = json.loads(UnderTabel)
        return d       
       
    def ForeignTradeMetaDict(self):
        ''' Vi henter tabelinfo fra tabellen kn8y
        
        Her beskrives strukturen i tabellen og hvordan data hentes.
        Tabelstruktur er et dictionary der først indeholder tabeloplysninger
        Herefter en Liste med dictionaries per kolonne
        Per kolonne dictionary består af en infodictionary og under key "values" en liste med dictionaries per kategori
        
        {tabelinfo ID,text,desciption,suppresseddatavalue,updated,contacts,documentation,footnote,variables 
          [
          {dict indud info:id,text,elimination,time,values[{dict for INDUD:id,text}]}, 
          {dict vare info:id,text,elimination,time,values[{dict for varer: id,text}], 
          {dict land:id,text,elimination,time,values[{dict for land: id,text}]}, 
          {dict enhed:id,text,elimination,time,values[{dict for enhed: id,text}]}, 
          {dict tid:id,text,elimination,time,values[{dict for tid: id,text}]}
          ]
          }
        
         d["id"] er tabellens navn
         d["variables"] er listen med tabelkolonneinfo - ialt 5: indud,vare,land,enhed,tid
         d["variables"][0] er alt info i første liste: indud
         d["variables"][0]["values"] er oversigt over indud dict (id=1 import, id=2 eksport)
         d["variables"][0]["values"][0] er først dict nemlig id=1 og text=import
         d["variables"][0]["values"][0]["id"] og d["variables"][0]["values"][0]["text"] er hhv key og text
        '''
        
        DkStat = "http://api.statbank.dk/v1/tableinfo"
        DkData= {"table": "kn8y"}
        r = requests.post(url = DkStat,json=DkData)
        KNATabel = r.text
        d = json.loads(KNATabel)
        return d 
         
    def CountryNameCodeDict(self,d):
        '''Laver landedictionary med name som key og kode som value
        #d er udgangstabel fra ForeignTradeMetaDict
        Se parametre her: ForeignTradeMetaDict
        '''
        
        list_lande=d['variables'][2]['values']
        landekode=[]
        landenavn=[]
        for item in list_lande:
            landekode.append(item['id'])
            landenavn.append(item['text'])
        dict_lande=dict(zip(landenavn,landekode))
        return dict_lande
        
    def CountryCodeNameDict(self,d):
        '''Laver landedictionary med kode som key og country som value
        #d er udgangstabel fra ForeignTradeMetaDict
        Se parametre her: ForeignTradeMetaDict
        '''
        
        list_lande=d['variables'][2]['values']
        landekode=[]
        landenavn=[]
        for item in list_lande:
            landekode.append(item['id'])
            landenavn.append(item['text'])
        dict_lande=dict(zip(landekode,landenavn))
        return dict_lande
        
    def ProductCodeNameDict(self,d):
        '''Laver productdictionary med code som key og name som value
        #d er udgangstabel fra ForeignTradeMetaDict
        Se parametre her: ForeignTradeMetaDict
        '''
        
        list_varer=d['variables'][1]['values']    
        varekode=[]
        varenavn=[]
        for item in list_varer:
            varekode.append(item['id'])
            varenavn.append(item['text'])
        dict_varer=dict(zip(varekode,varenavn))
        return dict_varer
        
    def ProductNameCodeDict(self,d):
        '''Laver productdictionary med name som key og kode som value
        #d er udgangstabel fra ForeignTradeMetaDict
        Se parametre her: ForeignTradeMetaDict
        '''
        
        list_varer=d['variables'][1]['values']    
        varekode=[]
        varenavn=[]
        for item in list_varer:
            varekode.append(item['id'])
            varenavn.append(item['text'])
        dict_varer=dict(zip(varenavn,varekode))
        return dict_varer 


#MainTable example
#=======================================
#Id nummer skal bruges ved valg af tabel for næste niveau
#Her ancvender vi kun tabel '13' tradetabeller.
minstat=DenmarkMeta()
mintabel=minstat.MainTables()
#Hele liste
#for item in mintabel: print(item)
#id og text for alle linier
#print('')
#print('Hele liste')


'''
#Trade tables example
#=======================================
#id=13 fra Maintables
#Tabel id bruges ved næste niveau. Her bruger vi kun kn8y i ForeignTradeMetaDict
minstat=DenmarkMeta()
mintabel=minstat.TradeTables()
#Der er et element i tabellen
#print(mintabel[0])

#Der er to undertabeller. udenrigshandel og betalingsbalance
#mintabel[0]['subjects'][0] er udenrigshandel
#mintabel[0]['subjects'][1] er betalingsbalance
#for item in mintabel[0]['subjects']: print('\n',item)

#Er kategorier for udenrigshandel mintabel[0]['subjects'][0]
#Der er to undertabeller. udenrigshandel med varer og udenrigshandel med tjenester
#mintabel[0]['subjects'][0]['subjects'][0] er varer
#mintabel[0]['subjects'][0]['subjects'][1] er tjenester
#for item in mintabel[0]['subjects'][0]['subjects']: print('\n',item)

#Liste over tabeller med udenrigshandel for varer
#for item in mintabel[0]['subjects'][0]['subjects'][0]['tables'] : print('\n',item)

#Liste med tabelnummer og navn
#for item in mintabel[0]['subjects'][0]['subjects'][0]['tables'] : print('\n',item['id'],item['text'])
'''     

'''
#Trade tables example
#=======================================
#id kn8y fra Trade tables
minstat=DenmarkMeta()
mintabel=minstat.ForeignTradeMetaDict()
print(mintabel['id'],mintabel['text'])
#mintabel["variables"] er listen med tabelkolonneinfo - ialt 5: 0=indud,1=vare,2=land,3=enhed,4=tid
for item in mintabel["variables"]:print('\n',item['id'])
#mintabel["variables"][0] er alt info i første liste: indud. Values giver valgmuligheder
#for item in mintabel["variables"][0]['values']: print(item)  #print('\n',item['id'],item['text'])
#Varer
#for item in mintabel["variables"][1]['values']: print(item)
#Land
for item in mintabel["variables"][2]['values']: print(item)
#Enhed
#for item in mintabel["variables"][3]['values']: print(item)
#Tid
#for item in mintabel["variables"][4]['values']: print(item)
'''

'''
#Country code and product code example
#=======================================
#Vi bruger udgangstabel fra ForeignTradeMetaDict
minstat=DenmarkMeta()
metadata=minstat.ForeignTradeMetaDict()
lande=minstat.CountryCodeNameDict(metadata)
print(lande["DE"])
varer=minstat.ProductCodeNameDict(metadata)
print(varer['25221000'])
'''








