from flask import Flask, jsonify
import sys
import random
import string

app = Flask(__name__)

@app.route('/register/<name>/<port>')
def register_node(name, port):
    cURL.setopt(cURL.URL, ip_proxy + '/register/' + name + '/' + port)
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
            return jsonify({'response': 'success',
                            'port': port,
                            'name': name,
                            'running': running})
    return jsonify({'response': 'failure',
                    'reason': 'unknown'})
  
@app.route('/remove/<name>')
def remove_node(name):
    print("About to get on: " + ip_porxy + '/rm/' + name)
    cURL.setopt(cURL.URL, ip_proxy + '/rm/' + name)
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
  
    
