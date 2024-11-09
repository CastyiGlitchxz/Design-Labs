"""Rich Presence initiator"""
import time
from pypresence import Presence

# rpc = discordrpc.RPC(app_id=1068376805104431124)
CLIENT_ID = "1068376805104431124"
rpc = Presence(CLIENT_ID)

def start_rich_presence(state) -> None:
    """Starts the discord rich presence"""
    rpc.connect()

    print(rpc.update(state=state,
                     details="A simple online designing app (Still in development)"))


    while True:  # The presence will stay on as long as the program is running
        time.sleep(15) # Can only update rich presence every 15 seconds

def stop_rich_presence() -> None:
    """Clears and stops discord rich presence"""
    rpc.clear()
    rpc.close()
