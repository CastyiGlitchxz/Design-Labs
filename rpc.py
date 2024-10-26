"""Rich Presence initiator"""
import discordrpc
from discordrpc.button import Button

def start_rich_presence(state):
    """Starts the discord rich presence"""
    rpc = discordrpc.RPC(app_id=1068376805104431124)

    button = Button(
        button_one_label="Start Designing",
        button_one_url="https://github.com",
        button_two_label="None",
        button_two_url="https://github.com"
    )

    rpc.set_activity(
        state=state,
        details="A simple online designing app (Still in development)",
        large_text="One of a kind",
        large_image="imageofcool",
        buttons=button,
    )

    rpc.run()
    if rpc.is_connected:
        print('connected')
