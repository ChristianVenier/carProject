import requests
import json
import time

class GrafanaAPI:
    def __init__(self, base_url="http://localhost:3000", username="admin", password="admin"):
        self.base_url = base_url
        self.auth = (username, password)
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.session = requests.Session()
        self.session.auth = self.auth
        
    def initialize_dashboard(self, dashboard_uid="degeyfhf3uqdcb"):
        """Inizializza il dashboard e forza l'esecuzione della prima query"""
        try:
            # Ottieni il dashboard
            dashboard_url = f"{self.base_url}/api/dashboards/uid/{dashboard_uid}"
            response = self.session.get(dashboard_url, headers=self.headers)
            
            if response.status_code == 200:
                dashboard_data = response.json()
                
                # Forza l'aggiornamento del dashboard
                refresh_url = f"{self.base_url}/api/dashboards/db"
                dashboard_data['dashboard']['refresh'] = "5s"  # Imposta aggiornamento automatico
                
                # Rimuovi i campi non necessari per l'aggiornamento
                if 'id' in dashboard_data['dashboard']:
                    dashboard_data['dashboard']['id'] = None
                dashboard_data['overwrite'] = True
                
                update_response = self.session.post(
                    refresh_url, 
                    headers=self.headers,
                    json=dashboard_data
                )
                
                if update_response.status_code == 200:
                    print("Dashboard inizializzato con successo e configurato per aggiornamento automatico")
                else:
                    print(f"Errore nell'inizializzazione del dashboard: {update_response.text}")
            else:
                print(f"Errore nel recupero del dashboard: {response.text}")
                
        except Exception as e:
            print(f"Errore nell'inizializzazione del dashboard: {e}")

    def refresh_all_panels(self, dashboard_uid="degeyfhf3uqdcb"):
        """Aggiorna tutti i pannelli del dashboard"""
        try:
            # Ottieni il dashboard
            dashboard_url = f"{self.base_url}/api/dashboards/uid/{dashboard_uid}"
            response = self.session.get(dashboard_url, headers=self.headers)
            
            if response.status_code == 200:
                dashboard_data = response.json()
                
                # Aggiorna il dashboard usando l'endpoint corretto
                refresh_url = f"{self.base_url}/api/dashboards/db"
                dashboard_data['dashboard']['refresh'] = "5s"
                
                # Rimuovi i campi non necessari per l'aggiornamento
                if 'id' in dashboard_data['dashboard']:
                    dashboard_data['dashboard']['id'] = None
                dashboard_data['overwrite'] = True
                
                refresh_response = self.session.post(refresh_url, headers=self.headers, json=dashboard_data)
                
                if refresh_response.status_code == 200:
                    print("Dashboard aggiornato con successo")
                else:
                    print(f"Errore nell'aggiornamento del dashboard: {refresh_response.text}")
            else:
                print(f"Errore nel recupero del dashboard: {response.text}")
                
        except Exception as e:
            print(f"Errore nell'aggiornamento dei pannelli: {e}")

    def refresh_panel(self, dashboard_uid, panel_id):
        """Aggiorna un singolo pannello"""
        try:
            # Aggiorna il dashboard intero invece del singolo pannello
            self.refresh_all_panels(dashboard_uid)
                
        except Exception as e:
            print(f"Errore nell'aggiornamento del pannello {panel_id}: {e}")

def main():
    try:
        # Usa l'hostname del container Grafana
        grafana = GrafanaAPI(base_url="http://localhost:3000", username="admin", password="admin")
        
        # Inizializza il dashboard e forza la prima query
        grafana.initialize_dashboard()
        
        # Attendi un momento per l'inizializzazione
        print("Attesa per inizializzazione dashboard...")
        time.sleep(2)
        
        while True:  # Loop infinito per la simulazione
            # Aggiorna tutti i pannelli
            grafana.refresh_all_panels()
            
            # Attendi 5 secondi prima del prossimo aggiornamento
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nSimulazione interrotta dall'utente")
    except Exception as e:
        print(f"Errore: {str(e)}")

if __name__ == "__main__":
    main() 