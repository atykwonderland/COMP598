from flask import Flask, jsonify
import sys
import random
import string

app = Flask(__name__)

@app.route('/register/<name>/<pod_id>')
def register_node(name, pod_id):
    found = false
    for pod in pods:
        if pod.id == pod_id:
            pod_name = pod.name
            found = true
    if found == false:
        return jsonify({'response': 'failure',
                        'reason': 'pod not found'})
    if pod_name == light_pod:
        cURL.setopt(cURL.URL,  light_proxy + '/register/' + name + '/' + pod_name)
    elif pod_name == medium_pod:
        cURL.setopt(cURL.URL,  medium_proxy + '/register/' + name + '/' + pod_name)
    elif pod_name == heavy_pod:
        cURL.setopt(cURL.URL,  heavy_proxy + '/register/' + name + '/' + pod_name)
    buffer = bytearray()
    
    cURL.setopt(cURL.WRITEFUNCTION, buffer.extend)
    cURL.perfrom()
    
    if cURL.getinfo(cURL.RESPONSE_CODE) == 200:
        response_dictionary = json.loads(buffer.decode())
        response = response_dictionary['response']
        if response == 'success':
            pod_name = response_dictionary['pod_name']
            name = response_dictionary['name']
            running = response_dictionary['running']
            return jsonify({'response': 'success',
                            'port': port,
                            'name': name,
                            'running': running})
    return jsonify({'response': 'failure',
                    'reason': 'unknown'})
  
@app.route('/remove/<name>/<pod_id>')
def remove_node(name, pod_id):
    found = false
    for pod in pods:
        if pod.id == pod_id:
            pod_name = pod.name
            found = true
    if found == false:
        return jsonify({'response': 'failure',
                        'reason': 'pod not found'})
    if pod_name == light_pod:
        cURL.setopt(cURL.URL,  light_proxy + '/rm/' + name + '/' + pod_name)
    elif pod_name == medium_pod:
        cURL.setopt(cURL.URL,  medium_proxy + '/rm/' + name + '/' + pod_name)
    elif pod_name == heavy_pod:
        cURL.setopt(cURL.URL,  heavy_proxy + '/rm/' + name + '/' + pod_name)
    buffer = bytearray()
    
    cURL.setopt(cURL.WRITEFUNCTION, buffer.extend)
    cURL.perfrom()
    
    if cURL.getinfo(cURL.RESPONSE_CODE) == 200:
        response_dictionary = json.loads(buffer.decode())
        response = response_dictionary['response']
        if response == 'success':
            port = response_dictionary['port']
            name = response_dictionary['name']
            running = response_dictionary['running']
            if running:
                disable_command = "echo 'experimental-mode on; set server servers/'" + name + ' state maint ' + '| sudo socat stdio /var/run/haproxy.sock'
                subprocess.run(disable_command, shell=True, check=True)
                
                command = "echo 'experimental-mode on; set server servers/'" + name + '| sudo socat stdio /var/run/haproxy.sock'
                subprocess.run(command, shell=True, check=True)
                return jsonify({'response': 'success',
                                'port': port,
                                'name': name,
                                'running': running})
    return jsonify({'response': 'failure',
                    'reason': 'unknown'})
  
    
