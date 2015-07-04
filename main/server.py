__author__ = 'eric'
import cherrypy
import threading
import re
import os
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import *

cherrypy.config.update({'log.screen': False})
cherrypy.config.update({'server.socket_host': '0.0.0.0'})

class CommandWebSocket(WebSocket):

    def received_message(self, message):
        response = self.main.run_server_command(message.data)
        response = re.sub("\n", "<br />", response)
        response = re.sub("\t", "&nbsp;", response)
        self.send(response, message.is_binary)


class WSServer:

    def __init__(self, main, port):

        self.main = main
        self.port = port

        self.CommandWebSocket = CommandWebSocket
        self.CommandWebSocket.main = self.main

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()

    def run(self):
        cherrypy.config.update({'server.socket_port': self.port})
        WebSocketPlugin(cherrypy.engine).subscribe()
        cherrypy.tools.websocket = WebSocketTool()


        class Root(object):
            @cherrypy.expose
            def index(self):
                script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
                rel_path = "../web/command.html"
                abs_file_path = os.path.join(script_dir, rel_path)
                commandMarkup = open(abs_file_path).read()
                return commandMarkup

            @cherrypy.expose
            def ws(self):
                # you can access the class instance through
                handler = cherrypy.request.ws_handler

        cherrypy.quickstart(Root(), '/', config={'/ws':
                                                     {
                                                         'tools.websocket.on': True,
                                                         'tools.websocket.handler_cls': self.CommandWebSocket
                                                     },
                                                 'global': {
                                                   'log.screen': False,
                                                   'log.error_file': '',
                                                   'log.access_file': ''
                                                }})
