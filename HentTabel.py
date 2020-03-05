import requests
import json
import pandas as pd

def HentTabelMetaData(tabelnavn):
    DS_tabelinfo = 'https://api.statbank.dk/v1/tableinfo'
    tabeldata_kald={"table": tabelnavn}
    r = requests.post(url = DS_tabelinfo,json=tabeldata_kald)
    u = r.text
    tabelmetadata = json.loads(u)
    return tabelmetadata

def VisMetaData(metatabel):
    print(tabelmeta.keys())
    print("")
    for variable in tabelmeta['variables']: print('{:15}''{:25}'.format(variable['id'],variable['text']))
    print("")
    for variable in tabelmeta['variables']:
        print('{:15}''{:25}'.format(variable['id'],variable['text']))
        for nr,item in enumerate(variable['values']):
            if nr<10:
                print('{:15}''{:25}'.format(item['id'],item['text']))
        print('')

def kn8m_tabel(varenr,lande,enhed,periode,expimp):
    DkStat = "https://api.statbank.dk/v1/data"

    data_kald =  {
            "table": "kn8m",
            "format": "CSV",
            "delimiter": "Semicolon",
            "allowVariablesInHead": True,
            "variables": [
                    {"code": "vare","values":varenr},
                    {"code": "land","values":lande},
                    {"code": "enhed","values": enhed},
                    {"code": "tid","values": periode},
                    {"code": "indud","values":expimp},
                    ] 
            }     
    r = requests.post(url = DkStat,json=data_kald)         
    r=r.text.split("\r\n")
    database=[line.split(";") for line in r]          
    print(pd.DataFrame(database[0:100]))
    
def fod_tabel(moderalder,barnkoen,periode):
    #eksempel for 02 Befolkning og valg/2405 fødsler/10017 Fødsler
    DkStat = "https://api.statbank.dk/v1/data"
    
    data_kald =  {
            "table": "fod",
            "format": "CSV",
            "delimiter": "Semicolon",
            "allowVariablesInHead": True,
            "variables": [
                    {"code": "MODERSALDER","values":moderalder},
                    {"code": "BARNKON","values":barnkoen},
                    {"code": "TID","values":periode},
                    ] 
            }     
    r = requests.post(url = DkStat,json=data_kald)         
    r=r.text.split("\r\n")
    database=[line.split(";") for line in r]          
    print(pd.DataFrame(database[0:100]))
    
    
def skabelon_tabel(var1,var2,var3):
    DkStat = "https://api.statbank.dk/v1/data"
    
    data_kald =  {
            "table": "==input=tabelnavn",
            "format": "CSV",
            "delimiter": "Semicolon",
            "allowVariablesInHead": True,
            "variables": [
                    {"code": "==input=navn var1","values":var1},
                    {"code": "==input=navn var2","values":var2},
                    {"code": "==input=navn var3","values":var3},
                    ] 
            }     
    r = requests.post(url = DkStat,json=data_kald)         
    r=r.text.split("\r\n")
    database=[line.split(";") for line in r]          
    print(pd.DataFrame(database[0:100]))    
    


tabelnavn=input("Vælg tabelnavn:")
tabelmeta=HentTabelMetaData(tabelnavn)

VisMetaData(tabelmeta)

#=====================================================
#kn8M
varenr=["25221000","25222000"]
lande=["SE","NO"]
enhed=["98","99"]
#periode=["2014M01"]
periode=[">=2014M01<=2014M12"]
expimp=["1","2"]

kn8m_tabel(varenr,lande,enhed,periode,expimp)
#=====================================================


#=====================================================
#fod
moderalder=[">=10<=64"]
#moderalder=["20"]
barnkoen=["D","P"]
periode=[">=2000<=2010"]
#periode=[">=1973<=2019"]
    
#fod_tabel(moderalder,barnkoen,periode)
#=====================================================


#=====================================================
#Skabelon
var1=["",""]
var2=["",""]
var3=["",""]

#skabelon_tabel(var1,var2,var3)
#=====================================================
