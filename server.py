from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas

@app.route('/launch', methods=['POST'])
def launch_file():
    try:
        process = subprocess.Popen(
            ['ros2', 'launch', 'rb1_shelf_tools', 'servers.launch.py'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        stdout, stderr = process.communicate()

        # Imprimir la salida y el error en la consola del servidor
        print("Output:\n", stdout)
        print("Error:\n", stderr)

        # Devolver la salida y el error como respuesta JSON
        return jsonify({
            'output': stdout,
            'error': stderr
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)