import traci
import time
import threading
from creaDatabase import *

def simulazione():
    try:
        # Avvia la simulazione con TraCI usando SUMO-GUI
        traci.start([
        "sumo-gui", 
        "-c", "config.sumocfg", 
        "--start", 
        "--delay", "100"
        ])
        # Simula per 24 ore (86400 secondi)
        step = 0
        while step < 86400:
            traci.simulationStep()

            if step == 25200:  # 7:00 (7 ore * 3600 secondi)
                print("Switching to peak hour program (programID 1) at 07:00")
                traci.trafficlight.setProgram("light", "1")
                print(f"Current program: {traci.trafficlight.getProgram('light')}")

            elif step == 46800:  # 13:00 (13 ore * 3600 secondi)
                print("Switching to off-peak program (programID 0) at 13:00")
                traci.trafficlight.setProgram("light", "0")
                print(f"Current program: {traci.trafficlight.getProgram('light')}")

            step += 1

    except traci.TraCIException as e:
        print(f"TraCI Error: {e}")

    finally:
        print("Simulation ended. Closing TraCI...")
        time.sleep(2)  # Aspetta un paio di secondi prima di chiudere
        traci.close()
        print("TraCI closed successfully.")



def read_xml_continuously(file_path):
    try:
        with open(file_path, 'r') as file:
            # Move the pointer to the end of the file
            file.seek(0, 2)  # '2' means seek to the end of the file
            while True:
                # Read the next line
                line = file.readline()
                
                # If line is non-empty, process it
                if line:
                    print(f"New line: {line.strip()}")
                else:
                    # No new line, sleep for a while
                    time.sleep(0.0001)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("dioporco")
    thread1 = threading.Thread(target=simulazione)
    thread2 = threading.Thread(target=read_xml_continuously, args=('statistiche/summary.xml',))
    print("dioporco")
        
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()    


if __name__ == "__main__":
    main()

    #creaDatabase()


   
