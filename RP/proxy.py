from flask import Flask, jsonify, request

app = Flask(__name__)

nodes = []
jobs = []

# TODO: this file needs to contain all possible api calls that need docker commands 
# includes: resource manager and resource monitor api calls

@app.route('/cloudproxy/nodes/all')
def cloud_get_all_nodes():
    if request.method == 'GET':
        #TODO: loop through all nodes and add them to the json
        pass

@app.route('/cloudproxy/nodes/<name')
def cloud_register(name):
    if request.method == 'GET':
        print('Request to register new node: ' + str(name))
        result = 'unknown'
        node_status = 'unknown'
        for node in nodes:
            if name == node['name']:
                print('Node already exists: ' + node['name'] + ' with status ' + node['status'])
        if result == 'unknown' and node_status == 'unknown':
            result = 'node_added'
            nodes.append({'name': name, 'status': 'IDLE'})
            node_status = 'IDLE'
            print('Successfully added a new node: ' + str(name))
        return jsonify({'result': result, 'node_status': node_status, 'node_name': name})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)