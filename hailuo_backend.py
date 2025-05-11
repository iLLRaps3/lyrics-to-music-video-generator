from flask import Flask, request, jsonify
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable not set")

GROQ_API_URL = "https://api.groq.ai/v1/chat/completions"

@app.route('/generate-prompt', methods=['POST'])
def generate_prompt():
    data = request.json
    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400

    model = data.get('model')
    style = data.get('style')
    cartoon_style = data.get('cartoonStyle', '')
    subject = data.get('subject')
    action = data.get('action')
    atmosphere = data.get('atmosphere')
    aspect = data.get('aspect')
    effects = data.get('effects', '')
    realism = data.get('realism')
    camera_buttons = data.get('cameraButtons', [])
    camera_push = data.get('cameraPush', False)
    camera_pullout = data.get('cameraPullout', False)
    camera_lowangle = data.get('cameraLowangle', False)
    camera_overhead = data.get('cameraOverhead', False)

    if not model or not subject or not action:
        return jsonify({'error': 'Missing required fields: model, subject, action'}), 400

    instruction = f"Create an optimized prompt for Hailuo AI's {model} video model (MiniMax) featuring \"{subject}\" in a {style} style."
    instruction += f" The main action is: {action}."
    if cartoon_style:
        instruction += f" Use cartoon style: {cartoon_style}."
    if atmosphere:
        instruction += f" The atmosphere/setting is: {atmosphere}."
    if effects:
        instruction += f" Include {effects} visual effects."
    if aspect:
        instruction += f" The video should be in {aspect} aspect ratio."

    realism_desc = ""
    if realism is not None:
        if realism <= 2:
            realism_desc = "cartoon/animated style"
        elif realism <= 4:
            realism_desc = "stylized, non-photorealistic look"
        elif realism <= 6:
            realism_desc = "semi-realistic style"
        elif realism <= 8:
            realism_desc = "moderately realistic appearance"
        else:
            realism_desc = "photorealistic, highly detailed style"
        if cartoon_style:
            realism_desc = f"{cartoon_style} {realism_desc}"
        instruction += f" The visual appearance should be in a {realism_desc}."

    camera_movements = []
    camera_map = {
        'zoom': "[Zoom in/out]",
        'pan': "[Pan left/right]",
        'tracking': "[Tracking shot]",
        'dolly': "[Dolly shot]",
        'shake': "[Shake]",
        'aerial': "[Aerial view]"
    }
    for cam in camera_buttons:
        if cam in camera_map:
            camera_movements.append(camera_map[cam])
    if camera_push:
        camera_movements.append("[Push in]")
    if camera_pullout:
        camera_movements.append("[Pull out]")
    if camera_lowangle:
        camera_movements.append("[Low angle]")
    if camera_overhead:
        camera_movements.append("[Overhead]")

    if model == 'director' and camera_movements:
        instruction += " Using camera movements: " + ", ".join(camera_movements) + "."

    if model == 'director':
        instruction += " Add appropriate camera direction commands in square brackets like [Zoom in] where it makes sense."
    elif model == 'live':
        instruction += " Focus on smooth, natural animation that preserves artistic integrity."
    elif model == 'subject':
        instruction += " Focus on maintaining character consistency throughout the prompt."

    instruction += " Format it as a concise, flowing description without sections or labels. Don't include explanations - just provide the prompt text itself."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": instruction}],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 1
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        generated_prompt = result['choices'][0]['message']['content'].strip()
        return jsonify({'prompt': generated_prompt})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return "Hailuo AI Video Prompt Builder Backend is running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
