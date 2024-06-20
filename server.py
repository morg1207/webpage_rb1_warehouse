from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import psutil

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas

# Almacenar el PID del proceso lanzado
process = None
process_pid = None

@app.route('/launch', methods=['POST'])
def launch_file():
    global process, process_pid
    try:
        process = subprocess.Popen(
            ['ros2', 'launch', 'rb1_shelf_tools', 'servers.launch.py'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        process_pid = process.pid  # Almacenar el PID del proceso lanzado

        # Obtener los PIDs de los procesos hijos (nodos de ROS2)
        parent = psutil.Process(process_pid)
        children = parent.children(recursive=True)
        children_pids = [child.pid for child in children]

        # No esperar a que el proceso termine
        return jsonify({
            'message': 'Launch file started successfully',
            'pid': process_pid,
            'children_pids': children_pids
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop', methods=['POST'])
def stop_processes():
    global process, process_pid
    try:
        if process_pid:
            # Obtener los PIDs de los procesos hijos (nodos de ROS2)
            parent = psutil.Process(process_pid)
            children = parent.children(recursive=True)
            children_pids = [child.pid for child in children]

            # Terminar todos los procesos hijos
            for pid in children_pids:
                child_process = psutil.Process(pid)
                child_process.terminate()
                child_process.wait()

            # Terminar el proceso principal
            process.terminate()
            process.wait()

            process_pid = None  # Reiniciar el PID almacenado

            return jsonify({'message': 'Processes stopped successfully'})
        else:
            return jsonify({'error': 'No processes to stop'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
