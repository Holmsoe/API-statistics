import DkTrade as dk
import SeTrade as se
import NoTrade as no
import requests
import pandas as pd
import json
import numpy as np
from pyjstat import pyjstat

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

def vistabel(db):
    print(db)    

def skrivtilexcel(db,navn):
    db.to_excel(navn)   

def skrivtillatex(db,navn):
    latextabel=db.to_latex(index=False)
    with open(navn, 'w') as f: 
        f.write(latextabel)

def gemplot(db,navn):
    fig, ax = plt.subplots()
    ax.plot(db)            
    fig.savefig(navn)
    
    
def Norge(periode,vare):
    eksempel=no.NorwayTrade(periode,vare)

    tabel=eksempel.GetTable()
    udtabel=eksempel.MakeTable(tabel)

    nytabel=eksempel.CutCountries(udtabel,100)
    skrivtabel=nytabel.round({'TON':1,'VALUE':0})
    #skrivtabel.to_csv('NoTotal.csv',index=False)
    #print(nytabel)

    yrtabel=eksempel.Yearly(nytabel)
    #print(yrtabel)

    eksempel.ShowExportPlot(yrtabel)
    eksempel.ShowImportPlot(yrtabel)

def Sverige(periode,vare):

    eksempel=se.SwedenTrade(periode,vare)

    exporttabel=eksempel.GetExportTable()
    udexptabel=eksempel.MakeExportTable(exporttabel)
    #print(udexptabel)

    importtabel=eksempel.GetImportTable()
    udimptabel=eksempel.MakeImportTable(importtabel)
    #print(udimptabel)

    udtabel=pd.concat([udexptabel,udimptabel])
    
    nytabel=eksempel.CutCountries(udtabel,300)
    skrivtabel=nytabel.round({'TON':1,'VALUE':0})
    #skrivtabel.to_csv('SeTotal.csv',index=False)

    yrtabel=eksempel.Yearly(nytabel)
    #print(yrtabel)

    #eksempel.ShowExportPlot(yrtabel)

    eksempel.ShowImportPlot(yrtabel)
    eksempel.ShowExportPlot(yrtabel)

def Danmark(periode,vare):
    eksempel=dk.DenmarkTrade(periode,vare)

    tabelnew=eksempel.GetNewTable() # 2016-
    tabelold=eksempel.GetOldTable() # -2015

    udtabelnew=eksempel.MakeTable(tabelnew)
    #print(udtabelnew)
    udtabelold=eksempel.MakeTable(tabelold)
    #print(udtabelold)
    udtabel=pd.concat([udtabelnew,udtabelold])
    #print(udtabel)
    
    nytabel=eksempel.CutCountries(udtabel,300)
    skrivtabel=nytabel.round({'TON':1,'VALUE':0})
    #skrivtabel.to_csv('DkTotal.csv',index=False)

    #print(nytabel)

    yrtabel=eksempel.Yearly(nytabel)
    #print(yrtabel)

    
    exptabel=eksempel.ShowExportPlot(yrtabel)
    vistabel(exptabel)
    skrivtilexcel(exptabel,'DKexport.xls')
    skrivtillatex(exptabel,'DKexpTabel.tex')
    gemplot(exptabel,'DKexpGraf.pdf')
    
    #eksempel.ShowImportPlot(yrtabel)    
      
minperiode=interval(2014,1,2019,6)
vare="25221000"  #brændt kalk
#vare="25222000" #hydratkalk
#vare="25182000" #brændt dolomit

Norge(minperiode,vare)
#Sverige(minperiode,vare)
#Danmark(minperiode,vare)
