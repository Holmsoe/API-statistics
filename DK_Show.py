import DkTrade as dk
import pandas as pd
#import DK_Meta as dd

def interval(startyr,startmth,slutyr,slutmth):
    period=[]
    mthrange=["01","02","03","04","05","06","07","08","09","10","11","12"]
    for m in range(startmth-1,12):
        period.append(str(startyr)+"M"+mthrange[m])
    p=[str(yr)+"M"+str(mth) for yr in range(startyr+1,slutyr) for mth in mthrange]
    for item in p: period.append(item)
    for m in range(0,slutmth):
        period.append(str(slutyr)+"M"+mthrange[m])
    return period

def Danmark(periode,vare):
    eksempel=dk.DenmarkTrade(periode,vare)

    tabelnew=eksempel.GetNewTable() # 2016-
    tabelold=eksempel.GetOldTable() # -2015

    udtabelnew=eksempel.MakeTable(tabelnew)
    #print(udtabelnew)
    udtabelold=eksempel.MakeTable(tabelold)
    #print(udtabelold)
    
    #Tabel med alt export og import til/fra DK
    #Alle lande er medtaget også lande uden aktivitet
    #Format: index TID FROM TO TON VALUE
    udtabel=pd.concat([udtabelnew,udtabelold])
    #print(udtabel)
    
    #Fjerner lande separat på import og export hvis sum af tonnage for perioeden er under benchmark
    nytabel=eksempel.CutCountries(udtabel,300)
    #TODO: Styring på limit
    
    #Afrunder til 1 decimal for volumen og 0 decimal for beløb
    skrivtabel=nytabel.round({'TON':1,'VALUE':0})
    
    #print(skrivtabel)
    #skrivtabel.to_csv('DkTotal.csv',index=False)

    #print(nytabel)

    #Beregner årstotaler
    yrtabel=eksempel.Yearly(nytabel)
    #print(yrtabel)

    #Beregn exporttabel per år
    exptabel=eksempel.ShowExportPlot(yrtabel)
    print(exptabel)
    #TODO: Styring på tabel og plot
    
    #Beregn importtabel per år
    imptabel=eksempel.ShowImportPlot(yrtabel)
    print(imptabel)
    #TODO: Styring på tabel og plot

    #TODO: Styring af filgenerering  
    
    #Export
    #vistabel(exptabel)
    #skrivtilexcel(exptabel,'DKexport.xls')
    #skrivtillatex(exptabel,'DKexpTabel.tex')
    #gemplot(exptabel,'DKexpGraf.pdf')
    
    #Import
    #vistabel(imptabel)
    #skrivtilexcel(imptabel,'DKimport.xls')
    #skrivtillatex(imptabel,'DKimpTabel.tex')
    #gemplot(imptabel,'DKimpGraf.pdf')
      
minperiode=interval(2014,1,2019,6)
vare="25221000"  #brændt kalk
#vare="25222000" #hydratkalk
#vare="25182000" #brændt dolomit

#Norge(minperiode,vare)
#Sverige(minperiode,vare)
Danmark(minperiode,vare)

