import sys
import Queue
import socket
import json
from select import select

OVSDB_IP = '127.0.0.1'
OVSDB_PORT = 5000
DEFAULT_DB = 'Open_vSwitch'
BUFFER_SIZE = 4096

def gather_reply(socket):
    result = ""
    # we got the whole thing if we received all the fields
    while "error" not in result or "id" not in result or "result" not in result:
        reply = socket.recv(BUFFER_SIZE)
        result += reply
    return json.loads(result)

def monitor(columns, monitor_id = None, db = DEFAULT_DB):
    msg = {"method":"monitor", "params":[db, monitor_id, columns], "id":0}
    return json.dumps(msg)

def list_bridges(db = DEFAULT_DB):
    columns = {"Bridge":{"columns":["name","ports"]}, "Port":{"columns":["interfaces","name"]},"Interface":{"columns":["name", "type", "options"]},"Open_vSwitch":{"columns":["bridges","cur_cfg"]}}
    return monitor(columns, db)

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((OVSDB_IP, OVSDB_PORT))

    current_id = 0

    s.send(list_dbs())
    db_list = gather_reply(s)
    db_name = db_list['result'][0]

    s.send(list_bridges())
    bridge_list = gather_reply(s)
    port = bridge_list['result']['Port']
    for key,value in port.items():
        print "key", key
        print value
    interface = bridge_list['result']['Interface']
    for key, value in interface.items():
        print "key", key
        print value