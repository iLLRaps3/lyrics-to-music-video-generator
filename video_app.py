from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import time
from music_video_gen import generate_video, download_video, query_video_status
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/output'

@app.route('/')
def index():
    return render_template('video_ui.html')

@app.route('/generate', methods=['POST'])
def handle_generation():
    try:
        data = request.json
        required_fields = ['api_key', 'group_id', 'prompt', 'model']
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        task_id = generate_video(
            prompt=data['prompt'],
            clip_num=int(data.get('clip_number', 1)),
            model=data['model'],
            api_key=data['api_key'],
            group_id=data['group_id']
        )

        if not task_id:
            return jsonify({'error': 'Failed to start video generation'}), 500

        return jsonify({
            'success': True,
            'task_id': task_id,
            'status_url': f'/status/{task_id}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<task_id>')
def check_status(task_id):
    try:
        file_id, status = query_video_status(task_id)
        return jsonify({
            'status': status,
            'file_id': file_id if file_id else None,
            'ready': status == 'Success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<file_id>')
def handle_download(file_id):
    try:
        filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not download_video(file_id, output_path):
            return jsonify({'error': 'Download failed'}), 500

        return jsonify({
            'download_url': f'/static/output/{filename}',
            'filename': filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/output/<filename>')
def serve_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=8000, debug=True)