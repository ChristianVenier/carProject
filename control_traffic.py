import traci
import time

def main():
    try:
        # Avvia la simulazione con TraCI usando SUMO-GUI
        traci.start([
            "sumo-gui", 
            "-c", "config.sumocfg", 
            "--start", 
            "--delay", "100",  # Rallenta la simulazione (100 ms per passo)
            "--demo", "true"   # Abilita modalità demo per visualizzazione
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
        # Chiudi la simulazione
        traci.close()

if __name__ == "__main__":
    main()