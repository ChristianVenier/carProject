import traci
import time
from creaDatabase import *

def main():
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

if __name__ == "__main__":
    main()
    creaDatabase()
