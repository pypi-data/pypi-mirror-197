import asyncio
from src.pyytlounge.wrapper import YtLoungeApi
from ast import literal_eval
import os

from src.pyytlounge.wrapper import PlaybackState

AUTH_STATE_FILE = "auth_state"


async def go():
    api = YtLoungeApi("Test")
    if os.path.exists(AUTH_STATE_FILE):
        with open(AUTH_STATE_FILE, "r") as f:
            content = f.read()
            api.load_auth_state(literal_eval(content))
            api.auth.lounge_id_token = "AGdO5p_6vEjSUu6aPm_E_Cqem9d2g6uDsYQrOsKYPCLMjCP746xnxBeoOS8IskNwn7pAwNpPE1S-NISvBvXVw7WYrauy-vLHUM3QrCc_A-sx1P-iae7ILRI"
            print("Loaded from file")
    else:
        pairing_code = int(input("Enter pairing code: "))
        print("Pairing...")
        paired = await api.pair(pairing_code)
        print(paired and "success" or "failed")
        if not paired:
            exit()
        auth_state = api.auth.serialize()
        with open(AUTH_STATE_FILE, "w") as f:
            f.write(str(auth_state))
    print(api)
    is_available = await api.is_available()
    print(f"Screen availability: {is_available}")

    print("Connecting...")
    connected = await api.connect()
    print(connected and "success" or "failed")
    if not connected:
        authed = await api.refresh_auth()
        if not authed or not await api.connect():
            exit()
        else:
            print("Reauth success")

    print(f"Screen: {api.screen_name}")
    print(f"Device: {api.screen_device_name}")

    print(api.auth.serialize())

    async def receive_state(state: PlaybackState):
        print(f"New state: {state}")
        print(f"Image should be at: https://img.youtube.com/vi/{state.videoId}/0.jpg")

    await api.subscribe(receive_state)


asyncio.run(go())
