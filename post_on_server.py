import requests

url = "http://127.0.0.1:7860/speech-to-text"
audio_path = "download1.webm"

with open(audio_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        data = response.json()
        print("Text:", data.get("text"))
        print("Processed:", data.get("processed"))
        print("Polyline:", data.get("polyline"))
    else:
        print("Error:", response.status_code, response.text)
