from aiohttp import web
import socketio
import os
import subprocess
import threading
import asyncio
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
v = False
async def index(request, test=None):
    global v
    """Serve the client-side application."""
    #with open('index.html') as f:
    #    return web.Response(text=f.read(), content_type='text/html')
    has_args = False
    if v == False:
        _temp = os.system('cls')
        print("Requested Helper Service from User::SquarerFive")
        print('          [METHOD]   [APP]     [ADDI]')
        v=True
    try:
        method = request.query['method']
        game = request.query['app']
        server = request.query['server']
        has_args = True
        print('[HELPER]', method,game,server)
        process_helper(method,game,server)
    except:
        has_args = False
        pass
    with open('index.html') as f:
        if (has_args):
            await asyncio.sleep(25)
        return web.Response(text=f.read(), content_type='text/html')
def process_helper(method,app,server):
    if method == "startgame":
        if app == "conquest":
            file_name = "F:\\UE4 Stuff\\Packaged\\Conquest Builds\\Release\\WindowsNoEditor\\Conquest.exe"
   # launch_command= '{0} {1} -dx12'.format(file_name, server)
            tr = threading.Thread(target =__internal_start, args=(app, ([file_name, '{}'.format(server)])))
            tr.start()
    # Launch subprocess on main thread.
            
def __internal_start(file_name, args):
    v = subprocess.call(args)
    print(v)
@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('chat message', namespace='/chat')
async def message(sid, data):
    print("message ", data)
    await sio.emit('reply', room=sid)

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

#app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    print("Hosting Helper Service")
    
    web.run_app(app, port=1337)
    
