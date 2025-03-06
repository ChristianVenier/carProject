import xml.etree.ElementTree as Et
from pymongo import MongoClient


def creaDatabase():
    file=Et.parse("statistiche/vehroute.xml")
    lista=file.getroot()
    i=0
    for elemento in lista.findall('vehicle'):
        i=i+1
        id=i
        tipo=elemento.get("type")
        partenza=elemento.get("depart")
        arrivo=elemento.get("arrival")
        percorso=elemento.find("route")
        percorso=percorso.get('edges')

        InFin=percorso.split()
        durata=float(arrivo)-float(partenza)


        ragruppa={"id":id,"tipo":tipo,"durata":durata,"inizio":InFin[0],"fine":InFin[1]}
        
        
    file=Et.parse("statistiche/summary.xml")
    lista=file.getroot()
    for elemento in lista.findall('step'):
        tempo=float(elemento.get('time'))
        if tempo%120==0:
            nMacchine=elemento.get("running")
            mDurata=elemento.get("meanTravelTime")
            mFermo=elemento.get("meanWaitingTime")
            print(mDurata)
            print(mFermo)
creaDatabase()