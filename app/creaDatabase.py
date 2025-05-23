from lxml import etree as Et
import mysql.connector
from mysql.connector import Error
import time

timeAccident = []
tabelle = [["veicoliSicuri", "statisticheSicure", "incidentiSicuri"], ["veicoliRischiosi", "statisticheRischiose", "incidentiRischiosi"]]

def connect_to_database():
    try:
        connection= mysql.connector.connect(
            host="localhost",
            database="simulazione",
            user="root",
            password="project"
        )
        if connection.is_connected():
            print("Connessione al database riuscita")
            return connection
    except Error as e:
        print(f"Errore nella connessione al database: {e}")
        return None
    
def updateLogs():
    global connection
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO logs (time) VALUES (%s)"
        data = (time.strftime("%Y-%m-%d %H:%M:%S"),)
        cursor.execute(insert_query, data)
        connection.commit()
        print("Log aggiornato con successo")
    except Error as e:
        print(f"Errore durante l'aggiornamento del log: {e}")
        
def updateAccidents(accidents):
    global timeAccident
    for veicolo, data in accidents.items():
        timeAccident.append(data[0])

def secondi_to_time(secondi):
    """Converte secondi in formato HH:MM:SS."""
    ore = secondi // 3600
    minuti = (secondi % 3600) // 60
    secondi_rimanenti = secondi % 60
    return f"{ore:02}:{minuti:02}:{secondi_rimanenti:02}"

def insertAccidents(connection, accident, scelta):
    try:
        cursor = connection.cursor()
        accident_time = secondi_to_time(int(float(accident)))  # Formato HH:MM:SS
        
        # Controlla se esiste già un record con quel tempo
        select_query = f"SELECT numeroIncidenti FROM {tabelle[scelta][2]} WHERE tempo = %s"
        cursor.execute(select_query, (accident_time,))
        result = cursor.fetchone()
        
        if result:
            # Aggiorna incrementando il numeroIncidenti
            new_count = result[0] + 1
            update_query = f"UPDATE {tabelle[scelta][2]} SET numeroIncidenti = %s WHERE tempo = %s"
            cursor.execute(update_query, (new_count, accident_time))
        else:
            # Inserisce nuovo record
            insert_query = f"INSERT INTO {tabelle[scelta][2]} (numeroIncidenti, tempo) VALUES (%s, %s)"
            cursor.execute(insert_query, (1, accident_time))
        
        connection.commit()
        print("Dati incidenti aggiornati con successo!")
        
    except Error as e:
        print(f"Errore durante l'inserimento o aggiornamento: {e}")
    finally:
        cursor.close()


def insert_dataVehRoute(raggruppa, scelta):
    global connection
    try:
        cursor = connection.cursor()
        insert_query = f"INSERT INTO {tabelle[scelta][0]} (tipo, durata, partenza, arrivo, tempoPartenza, tempoArrivo) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (raggruppa["tipo"], raggruppa["durata"], raggruppa["inizio"], raggruppa["fine"], raggruppa["partenza"], raggruppa["arrivo"])
        cursor.execute(insert_query, data)
        connection.commit()
        print("Dati inseriti con successo nella tabella veicoli")
    except Error as e:
        print(f"Errore durante l'inserimento della tabella veicoli: {e}")
    finally:
        cursor.close()

def insert_dataSummary(raggruppa, scelta):
    global connection
    try:
        cursor = connection.cursor()
        insert_query = f"INSERT INTO {tabelle[scelta][1]} (tempo, nMacchine, mDurata, mFermo) VALUES (%s, %s, %s, %s)"
        data = (raggruppa["tempo"], raggruppa["nMacchine"], raggruppa["mDurata"], raggruppa["mFermo"])
        cursor.execute(insert_query, data)
        connection.commit()
        print("Dati inseriti con successo nella tabella statistiche")
    except Error as e:
        print(f"Errore durante l'inserimento nella tabella statistiche: {e}")
    finally:
        cursor.close()

def trunkTables(scelta):
    global connection
    tablesToTruncate=tabelle[scelta]
    for table in tablesToTruncate:
        try:
            cursor=connection.cursor()
            truncateQuery=f"TRUNCATE TABLE {table}"
            cursor.execute(truncateQuery)
            connection.commit()
            print(f"Tabella {table} troncato con successo")
        except Error as e:
            print(f"Errore durante il troncamento della tabella {table}: {e}")
        finally:
            cursor.close()
            
def svuota_file_xml(file_path):
    try:
        with open(file_path, 'w') as f:
            f.write('')
        print(f"File {file_path} svuotato con successo")
    except Exception as e:
        print(f"Errore durante lo svuotamento del file: {e}")

def creaDatabase(scelta):
    global timeaccident
    global connection
    print("Ciao sono dentro crea database")
    parser = Et.XMLParser(recover=True)
    file=Et.parse("app/statistiche/vehroute.xml", parser=parser)
    lista=file.getroot()
    connection=connect_to_database()
    trunkTables(scelta)
    updateLogs()
    
    if connection is None:
        return

    for elemento in lista.findall('vehicle'):
        tipo=elemento.get("type")
        partenza=elemento.get("depart")
        arrivo=elemento.get("arrival")
        percorso=elemento.find("route")
        if percorso is not None:
            edges = percorso.get('edges')
        else:
            print("⚠️ percorso è None. Controlla il dato passato.")
       

        InFin=edges.split()
        durata=int(float(arrivo)-float(partenza))

        raggruppa={"tipo":tipo,"durata":durata,"inizio":InFin[0],"fine":InFin[1], "partenza":partenza, "arrivo":arrivo}
        insert_dataVehRoute(raggruppa, scelta)
    
    # Svuota il file vehroute.xml dopo averlo letto
    svuota_file_xml("app/statistiche/vehroute.xml")
        
    file=Et.parse("app/statistiche/summary.xml", parser=parser)
    lista=file.getroot()
    for elemento in lista.findall('step'):
        tempo=float(elemento.get('time'))
        if tempo%120==0:
            nMacchine=elemento.get("running")
            mDurata=elemento.get("meanTravelTime")
            mFermo=elemento.get("meanWaitingTime")
            raggruppa={"tempo":tempo,"nMacchine":nMacchine,"mDurata":mDurata,"mFermo":mFermo}
            insert_dataSummary(raggruppa, scelta)
    if timeAccident:
        for elemento in timeAccident:
            insertAccidents(connection, elemento, scelta)
            
    # Svuota il file summary.xml dopo averlo letto
    svuota_file_xml("app/statistiche/summary.xml")
    
    if connection.is_connected():
        connection.close()
        print("Connessione al database chiusa.")