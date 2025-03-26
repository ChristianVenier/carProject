import traci
import time
from collections import defaultdict
from get_ip import *
# from creaDatabase import *

JUNCTION_INTERNAL_PREFIX = ":J4_"

accidents = defaultdict(list)
lane_changed = defaultdict(bool)
accident_occurred = False

def check_for_accidents():
    global accident_occurred
    try:
        colliding_pairs = traci.simulation.getCollisions()
        current_time = traci.simulation.getTime()
        if colliding_pairs:
            print(f"Step {current_time}: {len(colliding_pairs)} collisioni rilevate.")
            accident_occurred = True
            for collision in colliding_pairs:
                veh1_id = collision.collider
                veh2_id = collision.victim
                lane1 = traci.vehicle.getLaneID(veh1_id) if veh1_id in traci.vehicle.getIDList() else ""
                lane2 = traci.vehicle.getLaneID(veh2_id) if veh2_id in traci.vehicle.getIDList() else ""
                if (lane1.startswith(JUNCTION_INTERNAL_PREFIX) and
                    lane2.startswith(JUNCTION_INTERNAL_PREFIX) and
                    veh1_id not in accidents and veh2_id not in accidents):
                    handle_accident(veh1_id, veh2_id, current_time)
                    print(f"Collisione tra {veh1_id} e {veh2_id} su {lane1} al tempo {current_time}")
                    # updateAccidents(program_traffic_light, current)
    except traci.TraCIException as e:
        print(f"Errore nel rilevamento collisioni: {e}")

def handle_accident(veh1_id, veh2_id, collision_time):
    try:
        # Ferma i veicoli
        traci.vehicle.setSpeed(veh1_id, 0)
        traci.vehicle.setSpeed(veh2_id, 0)

        # Cambia colore a rosso per indicare l'incidente
        traci.vehicle.setColor(veh1_id, (255, 0, 0))  # Rosso
        traci.vehicle.setColor(veh2_id, (255, 0, 0))  # Rosso

        # Evidenzia i veicoli con un contorno visibile
        traci.vehicle.highlight(veh1_id, (255, 0, 0))  # Rosso
        traci.vehicle.highlight(veh2_id, (255, 0, 0))  # Rosso

        # Calcola il punto medio della collisione
        pos1 = traci.vehicle.getPosition(veh1_id)
        pos2 = traci.vehicle.getPosition(veh2_id)
        center_x = (pos1[0] + pos2[0]) / 2
        center_y = (pos1[1] + pos2[1]) / 2

        # Sposta i veicoli più vicini al punto medio (a 0.5 unità di distanza)
        traci.vehicle.moveToXY(veh1_id, "", -1, center_x + 0.5, center_y + 0.5, keepRoute=2)
        traci.vehicle.moveToXY(veh2_id, "", -1, center_x - 0.5, center_y - 0.5, keepRoute=2)

        v1_class = traci.vehicle.getVehicleClass(veh1_id)
        v2_class = traci.vehicle.getVehicleClass(veh2_id)
        duration = 900 if v1_class in ["truck", "delivery", "bus"] or v2_class in ["truck", "delivery", "bus"] else 1800
        accidents[veh1_id] = [collision_time, duration]
        accidents[veh2_id] = [collision_time, duration]
        print(f"Veicoli coinvolti {veh1_id} ({v1_class}) e {veh2_id} ({v2_class}) fermati per {duration/60} minuti.")
    except traci.TraCIException as e:
        print(f"Errore nella gestione incidente: {e}")

def manage_accident_duration():
    try:
        current_time = traci.simulation.getTime()
        vehicles_to_remove = []
        for veh_id in list(accidents.keys()):
            start_time, duration = accidents[veh_id]
            elapsed_time = current_time - start_time
            if elapsed_time >= duration:
                try:
                    if veh_id in traci.vehicle.getIDList():
                        traci.vehicle.remove(veh_id)
                        print(f"Veicolo {veh_id} rimosso al tempo {current_time} dopo {elapsed_time} secondi.")
                    else:
                        print(f"Veicolo {veh_id} non più presente nella simulazione al tempo {current_time}.")
                    vehicles_to_remove.append(veh_id)
                except traci.TraCIException as e:
                    print(f"Errore nella rimozione del veicolo {veh_id}: {e}")
        for veh_id in vehicles_to_remove:
            del accidents[veh_id]
    except traci.TraCIException as e:
        print(f"Errore nella gestione durata: {e}")

def is_lane_change_safe(veh_id, target_lane_idx):
    try:
        current_lane_idx = traci.vehicle.getLaneIndex(veh_id)
        if current_lane_idx == target_lane_idx:
            return True

        current_lane = traci.vehicle.getLaneID(veh_id)
        edge = current_lane.split('_')[0]
        num_lanes = traci.edge.getLaneNumber(edge)
        if not (0 <= target_lane_idx < num_lanes):
            print(f"Corsia target {target_lane_idx} non valida per {veh_id} sul bordo {edge}.")
            return False

        target_lane = f"{edge}_{target_lane_idx}"
        safety_distance = 10.0 if traci.vehicle.getVehicleClass(veh_id) in ["truck", "delivery", "bus"] else 3.0

        vehicles_on_target = traci.lane.getLastStepVehicleIDs(target_lane)
        for other_veh_id in vehicles_on_target:
            if other_veh_id == veh_id:
                continue
            other_pos = traci.vehicle.getPosition(other_veh_id)
            veh_pos = traci.vehicle.getPosition(veh_id)
            distance = ((other_pos[0] - veh_pos[0])**2 + (other_pos[1] - veh_pos[1])**2)**0.5
            if distance < safety_distance:
                return False
        return True
    except traci.TraCIException as e:
        print(f"Errore in is_lane_change_safe per {veh_id}: {e}")
        return False

def reroute_with_lane_change(veh_id):
    try:
        if veh_id not in traci.vehicle.getIDList():
            print(f"Veicolo {veh_id} non più presente.")
            return False

        if veh_id in accidents:
            print(f"Veicolo {veh_id} coinvolto in collisione, cambio corsia ignorato.")
            return False

        if lane_changed[veh_id]:
            print(f"Veicolo {veh_id} ha già cambiato corsia.")
            return False

        current_lane = traci.vehicle.getLaneID(veh_id)
        if current_lane.startswith(JUNCTION_INTERNAL_PREFIX):
            print(f"Veicolo {veh_id} su corsia interna {current_lane}, cambio corsia ignorato.")
            return False

        v_class = traci.vehicle.getVehicleClass(veh_id)
        if v_class in ["truck", "delivery", "bus"]:
            print(f"Veicolo {veh_id} ({v_class}) non cambia corsia.")
            return False

        current_lane_idx = traci.vehicle.getLaneIndex(veh_id)
        edge = current_lane.split('_')[0]
        lane_count = traci.edge.getLaneNumber(edge)
        print(f"Tentativo di cambio corsia per {veh_id} ({v_class}): corsia {current_lane_idx} su {current_lane}.")

        position = traci.vehicle.getPosition(veh_id)
        junction_pos = (0, 100)
        distance_to_junction = ((position[0] - junction_pos[0])**2 + (position[1] - junction_pos[1])**2)**0.5
        if distance_to_junction < 10:
            print(f"Veicolo {veh_id} troppo vicino all'incrocio ({distance_to_junction:.2f} m).")
            return False

        possible_lanes = []
        if current_lane_idx > 0:
            possible_lanes.append(current_lane_idx - 1)
        if current_lane_idx < lane_count - 1:
            possible_lanes.append(current_lane_idx + 1)

        for target_lane_idx in possible_lanes:
            if is_lane_change_safe(veh_id, target_lane_idx):
                duration = 2
                duration = int(max(0, min(255, duration)))
                try:
                    traci.vehicle.changeLane(veh_id, target_lane_idx, duration)
                    lane_changed[veh_id] = True
                    print(f"Veicolo {veh_id} cambia a corsia {target_lane_idx}.")
                    return True
                except traci.TraCIException as e:
                    print(f"Errore cambio corsia per {veh_id}: {e}")
                    return False
        print(f"Nessuna corsia sicura per {veh_id}.")
        return False
    except traci.TraCIException as e:
        print(f"Errore durante il cambio corsia per {veh_id}: {e}")
        return False

def main():
    global accident_occurred, program_traffic_light
    
    while True:
        program_traffic_light = input("Programma semaforo (0-1) / 0 = SICURO - 1 = PERICOLOSO: ")
        if program_traffic_light in ["0", "1"]:
            break
        print("Input non valido. Inserisci 0 o 1.")
    
    random_seed = int(time.time())
    try:
        print("Avvio di SUMO...")
        traci.start([
            "sumo-gui",
            "-c", "app/config.sumocfg",
            "--start",
            "--delay", "100",
            "--gui-settings-file", "app/view.port.xml",
            "--random",
            "--seed", str(random_seed)
        ])
        print("Simulazione avviata.")
        
        traci.trafficlight.setProgram("light", program_traffic_light)
        
        step = 0
        last_collision_step = -10
        while step < 86400:
            try:
                traci.simulationStep()
                check_for_accidents()
                manage_accident_duration()
                
                if accident_occurred:
                    if step - last_collision_step >= 10:
                        for veh_id in traci.vehicle.getIDList():
                            if veh_id not in accidents and not lane_changed.get(veh_id, False):
                                try:
                                    reroute_with_lane_change(veh_id)
                                except Exception as e:
                                    print(f"Errore in reroute_with_lane_change per {veh_id}: {e}")
                                    continue
                    last_collision_step = step if accident_occurred else last_collision_step
                
                step += 1
            except traci.TraCIException as e:
                print(f"Errore allo step {step}: {e}")
                step += 1
                continue
        
        print("Simulazione completata.")
        traci.close()
    except Exception as e:
        print(f"Errore generale: {e}")
    finally:
        if traci.isLoaded():
            traci.close()

if __name__ == "__main__":
    main()