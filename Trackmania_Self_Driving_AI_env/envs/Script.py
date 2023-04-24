from tminterface.interface import TMInterface, ServerException
from tminterface.client import Client, run_client
from tminterface.structs import SceneVehicleCar, SceneVehicleCarState, SimStateData 
import sys
import threading
import time

class MainClient(Client):

    def __init__(self) -> None:
        super(MainClient, self).__init__()
        self.iface = None

    def on_registered(self, iface: TMInterface) -> None:
        print(f'Registered to {iface.server_name}')
        self.iface = iface

    def on_run_step(self, iface: TMInterface, _time: int):
        pass
     
def main(client):
    server_name = f'TMInterface{sys.argv[1]}' if len(sys.argv) > 1 else 'TMInterface0'
    print(f'Connecting to {server_name}...')
    iface = TMInterface(server_name, 65535)

    iface.register(client)

    while iface.running:
        time.sleep(0)

def get_data(client):
    time.sleep(0)
    while True:
        time.sleep(0)
        if client.iface:
            try:
                if client.iface.get_simulation_state().player_info:
                    #logging.debug("{} - position: {}".format(client.iface.get_simulation_state().time,
                    #                                    client.iface.get_simulation_state().simulation_wheels))
                    time.sleep(0)
            except ServerException:
                time.sleep(0)
if __name__ == '__main__':
    client = MainClient()
    threading.Thread(target=main, daemon=False, args=[client]).start()
    threading.Thread(target=get_data, daemon=True, args=[client]).start()