from flask import session 
from flask_socketio import emit

def socketio_init(socketio):
    @socketio.on('testSocket',namespace='/test')
    def testEvent(message):
        tsession = session.get('test')
        print('received message'+str(message))
        retMessage = { 'msg' : "hello response" }
        emit('test',retMessage,callback=tsession)