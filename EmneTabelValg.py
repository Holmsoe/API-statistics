import requests
import json
import pandas as pd

def HentHoved():
  DS_subjects = 'https://api.statbank.dk/v1/subjects'
  r = requests.post(url = DS_subjects)
  HovedEmner = r.text
  d = json.loads(HovedEmner)
  return d

def HentEmner(emner):
  DS_subjects = 'https://api.statbank.dk/v1/subjects'
  Emneliste_kald={"subjects": emner,"includeTables": True}
  r = requests.post(url = DS_subjects,json=Emneliste_kald)
  Emneliste_retur = r.text
  d = json.loads(Emneliste_retur)
  return d  

def HentTabelMetaData(tabelnavn):
    DS_tabelinfo = 'https://api.statbank.dk/v1/tableinfo'
    tabeldata_kald={"table": tabelnavn}
    r = requests.post(url = DS_tabelinfo,json=tabeldata_kald)
    u = r.text
    tabelmetadata = json.loads(u)
    return tabelmetadata
   

HovedEmner=HentHoved()
for emne in HovedEmner:
  print(emne['id'],emne['description'])

niveau1=input("Vælg emne:")
emneliste=[niveau1]

Niveau1Emner=HentEmner(emneliste)
#Vise jasonstruktur af returfil
#print(Niveau1Emner)
#Vise valgt emne
print(Niveau1Emner[0]['id'],Niveau1Emner[0]['description'])
#Vise underemner
for emne in Niveau1Emner[0]['subjects']:
  print(emne['id'],emne['description'])

niveau2=input("Vælg emne:")
emneliste=[niveau2]
Niveau2Emner=HentEmner(emneliste)
#Vise jasonstruktur af returfil
#print(Niveau2Emner)
#Vise valgt emne
print(Niveau2Emner[0]['id'],Niveau2Emner[0]['description'])
#Vise underemner
for emne in Niveau2Emner[0]['subjects']:
  print(emne['id'],emne['description'])

niveau3=input("Vælg emne:")
emneliste=[niveau3]
Niveau3Emner=HentEmner(emneliste)
#Vise tabeller fra jasonstruktur af returfil
#print(Niveau3Emner[0]['tables'])
#Vise hele jasonstruktur
#print(Niveau3Emner)
#Vise valgt emne
print(Niveau3Emner[0]['id'],Niveau3Emner[0]['description'])
#Vise tabelnavne
print('{:10}''{:10}''{:10}''{:<6}''{:30}'.format('id','start','slut','aktiv','text'))
for emne in Niveau3Emner[0]['tables']:
  print('{:10}''{:10}''{:10}''{:<6}''{:30}'.format(emne['id'],emne['firstPeriod'],emne['latestPeriod'],emne['active'],emne['text']))

tabelnavn=input("Vælg tabelnavn:")
tabelmeta=HentTabelMetaData(tabelnavn)
print(tabelmeta.keys())
for variable in tabelmeta['variables']: print('{:15}''{:25}'.format(variable['id'],variable['text']))

for variable in tabelmeta['variables']: 
    print('{:15}''{:25}'.format(variable['id'],variable['text']))
    for item in variable['values']:
        print('{:15}''{:25}'.format(item['id'],item['text']))
    print('')

'''
#Skabelon
DkStat = "https://api.statbank.dk/v1/data"
tabelnavn="xyz"
var1=[]
var2=[]
#
data_kald =  {
        "table": tabelnavn,
        "format": "CSV",
        "delimiter": "Semicolon",
        "allowVariablesInHead": True,
        "variables": [
                {"code": "variable1","values":var1},
                {"code": "variable2","values":lande},
                #
                #
                ] 
        }     
r = requests.post(url = DkStat,json=data_kald)         
r=r.text.split("\r\n")
database=[line.split(";") for line in r]          
print(pd.DataFrame(database[0:100]))
'''


#Eksempel for KN8M rapporten    
DkStat = "https://api.statbank.dk/v1/data"
varenr=["25221000","25222000"]
lande=["SE","NO"]
enhed=["98","99"]
#periode=["2014M01"]
periode=[">=2014M01<=2014M12"]
expimp=["1","2"]
 
datasimple =  {
        "table": tabelnavn,
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
r = requests.post(url = DkStat,json=datasimple)         
r=r.text.split("\r\n")
database=[line.split(";") for line in r]          
print(pd.DataFrame(database[0:100]))


'''
#eksempel for 02 Befolkning og valg/2405 fødsler/10017 Fødsler
DkStat = "https://api.statbank.dk/v1/data"
tabelnavn="fod"
moderalder=[">=10<=64"]
#moderalder=["20"]
barnkoen=["D","P"]
periode=[">=2000<=2010"]
#periode=[">=1973<=2019"]
#
data_kald =  {
        "table": tabelnavn,
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
'''