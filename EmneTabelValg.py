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

#=========Hovedmenu===========================
HovedEmner=HentHoved()
for emne in HovedEmner:
  print(emne['id'],emne['description'])

niveau1=input("Vælg emne:")
emneliste=[niveau1]
#=============================================

#=========Niveau1===========================
Niveau1Emner=HentEmner(emneliste)
#Vise jasonstruktur af returfil
#print(Niveau1Emner)
#Vise valgt emne
print(Niveau1Emner[0]['id'],Niveau1Emner[0]['description'])
#Vise underemner
for emne in Niveau1Emner[0]['subjects']:
  print(emne['id'],emne['description'])
#=============================================

#=========Niveau2===========================
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
#=============================================
  
#=========Niveau3===========================
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
#=============================================
