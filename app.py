from flask import Flask, request, jsonify
from flask_cors import CORS
from speech_to_text import convert_speech_to_text
from query_to_structured_output import structured_output
from json_to_polyline import get_route_info

# Create a Flask application instance
app = Flask(__name__)
CORS(app)  # <-- Enable CORS for all routes

@app.route("/speech-to-text", methods=["POST"])
def handle_speech():
    """
    This endpoint receives an audio file via POST request,
    converts it into text, processes that text into a structured format,
    and returns both in JSON form.
    """

    if "file" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    
    # text1 = structured_output("Give me a route from dallas to houston")
    # result = jsonify({"text": "Give me a route from dallas to houston", "processed": text1, "polyline": get_route_info(text1)})
    # return result

    audio_file = request.files["file"]
    text = convert_speech_to_text(audio_file)
    print(text)

    if text is None:
        return jsonify({"error": "Could not transcribe audio"}), 400

    structur_output = structured_output(text)
    print(structur_output)

    polyline = get_route_info(structur_output)

    return jsonify({"text": text, "processed": structur_output, "polyline": polyline})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=True)
