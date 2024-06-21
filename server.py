from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import psutil
import threading
import time
import os

app = Flask(__name__, static_folder='frontend', static_url_path='/')
CORS(app)  # Esto habilita CORS para todas las rutas

# Almacenar el PID del proceso lanzado
process = None
process_pid = None
process_output = []

output_file_path = "/tmp/process_output.log"

def read_process_output():
    global process_output
    with open(output_file_path, 'r') as file:
        while True:
            line = file.readline()
            if line:
                process_output.append(line.strip())
            else:
                time.sleep(0.1)

@app.route('/launch', methods=['POST'])
def launch_file():
    global process, process_pid, process_output
    try:
        print("Received request to launch file")
        process_output = []
        with open(output_file_path, 'w') as file:
            pass  # Clear the file

        process = subprocess.Popen(
            ['ros2', 'launch', 'path_planner_server', 'navigation.launch.py'],
            stdout=open(output_file_path, 'a'),
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        process_pid = process.pid  # Almacenar el PID del proceso lanzado

        # Iniciar el hilo para leer la salida del proceso
        threading.Thread(target=read_process_output, daemon=True).start()

        # Obtener los PIDs de los procesos hijos (nodos de ROS2)
        parent = psutil.Process(process_pid)
        children = parent.children(recursive=True)
        children_pids = [child.pid for child in children]
        
        # Imprimir los PIDs en la consola
        print(f"Launched process PID: {process_pid}")
        print(f"Children PIDs: {children_pids}")
        
        return jsonify({
            'message': 'Archivo de lanzamiento iniciado correctamente',
            'pid': process_pid,
            'children_pids': children_pids
        })
    except Exception as e:
        print(f"Error launching file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/stop', methods=['POST'])
def stop_processes():
    global process, process_pid
    try:
        print("Received request to stop processes")
        if process_pid:
            # Obtener los PIDs de los procesos hijos (nodos de ROS2)
            parent = psutil.Process(process_pid)
            children = parent.children(recursive=True)
            children_pids = [child.pid for child in children]

            # Imprimir los PIDs en la consola
            print(f"Stopping children PIDs: {children_pids}")

            # Terminar todos los procesos hijos
            for pid in children_pids:
                child_process = psutil.Process(pid)
                child_process.terminate()
                child_process.wait()

            # Terminar el proceso principal
            process.terminate()
            process.wait()

            process_pid = None  # Reiniciar el PID almacenado

            print("Processes stopped successfully")
            return jsonify({'message': 'Procesos detenidos correctamente'})
        else:
            print("No processes to stop")
            return jsonify({'error': 'No hay procesos para detener'}), 400
    except Exception as e:
        print(f"Error stopping processes: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/output', methods=['GET'])
def get_output():
    global process_output
    return jsonify(process_output)

# Ruta para servir la aplicación Vue.js
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue_app(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
