import pyaimp
import requests
import time

# Revolt user url
url = "https://api.revolt.chat/users/@me"

# Account token, read README.md for more info.
token = ""

headers = {
    "Content-Type": "application/json",
    "X-Session-Token": token
}

try:

    client = pyaimp.Client()

    state = client.get_playback_state()

    # Make sure that music is being played, or music is currently paused
    while state == pyaimp.PlayBackState.Playing or state == pyaimp.PlayBackState.Paused:
        name = pyaimp.Client.get_current_track_info(client).get("title")

        # This adds delay between each check, to not boil your device. Sometimes this can actually desync what you're
        # listening to, and what it thinks you're listening to. This isn't a big deal, but the delay can be changed.
        delay = 5
        time.sleep(delay)

        if name != pyaimp.Client.get_current_track_info(client).get("title"):
            payload = {"status": {"text": "Listening to: " + pyaimp.Client.get_current_track_info(client).get(
                "artist") + " - " + pyaimp.Client.get_current_track_info(client).get("title")}}
            response = requests.patch(url, json=payload, headers=headers)
            print(response.json())

except RuntimeError as re: # AIMP is not open!!!!! OPEN IT!!!!
    payload = {"status": {"text": ""}}
    response = requests.patch(url, json=payload, headers=headers)
    print("Resetting Status: " + response.json())
    print(re)
    print("Please open AIMP")
except Exception as e:
    payload = {"status": {"text": ""}}
    response = requests.patch(url, json=payload, headers=headers)
    print("Resetting Status: " + response.json())
    print(e)

finally:
    payload = {"status": {"text": ""}}
    response = requests.patch(url, json=payload, headers=headers)