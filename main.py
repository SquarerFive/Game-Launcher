from aiohttp import web
import socketio
import json
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
servers = [
    ]
latest_version=0.2
download_url="http://localhost/game/patch/"
download_file="Conquest-WindowsNoEditor_0_P.pak"
GameServers = [
    ]
serverData={
    "serverName": str(),
    "serverMap": str()
    }
log_class = [
    "LOG",
    "WARNING",
    "CRITICAL",
    "ERROR"
    ]
async def index(request):
    print(request)
    """Serve the client-side application."""
    return web.Response(text='test', content_type='text/html')
    #with open('index.html') as f:
     #   return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect', namespace='/')
def connect(sid, environ):
    log(("Client Connected:",sid))
@sio.on('add_server',namespace='/')
def add_server(sid, data):
    #print(data['server_id'])
    servers.append(data)
    log(("Added serving client with data: ",data))
@sio.on('remove_server',namespace='/')
def remove_server(sid):
    global servers
    for server in servers:
        if server['session_id'] == str(sid):
            servers.remove(server)
    log(("Removed serving client with SID:",sid))
@sio.on('chat message', namespace='/')
async def message(sid, data):
    print("message ", data)
    await sio.emit('reply', room=sid)
@sio.on('disconnect', namespace='/')
def disconnect(sid):
    log(("Disconnected client with SID: ",sid)) 
    print('disconnect ', sid)
    remove_server(sid)
@sio.on('get_latest_version', namespace='/')
async def get_latest_version(sid, environ):
    d = {
        "version":latest_version
        }
    log("::get_latest_version:: Executed")
    datas= json.dumps(d)
  #  print(datas)
    await sio.emit('latest_version', data=latest_version, room=sid)
    await sio.emit('update_url', data=download_url, room=sid)
    await sio.emit('update_file', data=download_file, room=sid)
app.router.add_get('/', index)
@sio.on('register_server',namespace='/')
async def register_server(sid, data):
    global GameServers
    serverName = data['serverName']
    serverMap = data['serverMap']
    GameServers.append(create_server(serverName, serverMap))
    log(("Registered Gameserver with data: ",data))
@sio.on('get_servers',namespace='/')
async def get_servers(sid, environ):
    global GameServers
    serverClient = {
        "servers": GameServers
        }
    await sio.emit('on_GotServers', data=serverClient, room=sid)
def create_server(serverName, serverMap):
    server = {
        "serverName": serverName,
        "serverMap": serverMap}
    return server
def log(message, typeIDX=0):
    #print(type(message))
    if (type(message) == tuple):
        message = str(message)
  # msg = str(str(log_class[typeIDX])+": "+message)
    msg = "[{0}]: {1}".format(log_class[typeIDX],message)
    print(msg)
if __name__ == '__main__':
    web.run_app(app, host="127.0.0.1", port=3000)
