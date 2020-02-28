import SE_Meta as se
import DK_Meta as dk
import NO_Meta as no

#Sweden search statistics
minstat=se.SwedenMeta()
exportmeta=minstat.ExpTabelMetaDict() 

countrytable=minstat.CountryCodeNameDict(exportmeta)
producttable=minstat.ProductCodeNameDict(exportmeta)

koder=list(countrytable.keys())
landname=list(countrytable.values())
tjekland='stan'
for land in landname:
    if tjekland in land: print(land)
    
koder=list(producttable.keys())
prodname=list(producttable.values())
tjekprod="iron ore"

for nr,prod in enumerate(prodname):
    if tjekprod in prod and len(koder[nr])==8: 
        print('{:10}''{:50}'.format(koder[nr],prod))
        print("")

#Denmark search statistics
minstatdk=dk.DenmarkMeta()
metadatadk=minstatdk.ForeignTradeMetaDict()
lande=minstatdk.CountryCodeNameDict(metadatadk)
varer=minstatdk.ProductCodeNameDict(metadatadk)

landekoder=list(lande.keys())
landname=list(lande.values())

tjekland='stan'
for land in landname:
    if tjekland in land: print(land)
    
prodkoder=list(varer.keys())
prodnamedk=list(varer.values())

tjekprod="kalk"

for nr,prod in enumerate(prodnamedk):
    if tjekprod in prod: 
        print('{:50}'.format(prod))
        print("")        
        
#Norway search statistics
minstatno=no.NorwayMeta()  
mintabelno=minstatno.ForeignTradeMetaDict() 
landeno=minstatno.CountryCodeNameDict(mintabelno)  
varerno=minstatno.ProductCodeNameDict(mintabelno)
landekodern=list(landeno.keys())
landnameno=list(landeno.values())

tjekland='stan'
for land in landnameno:
    if tjekland in land: print(land)
    
prodkoderno=list(varerno.keys())
prodnameno=list(varerno.values())

tjekprod="2522"

for nr,prod in enumerate(prodkoderno):
    if tjekprod in prod: 
        print('{:10}''{:50}'.format(prod,prodnameno[nr]))
        print("")