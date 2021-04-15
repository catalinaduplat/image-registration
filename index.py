#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:08:25 2021

@author: duplacat
"""

import tornado.web
import tornado.ioloop
import imageRegistration

class uploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
    
    def post(self):
        dtiFiles = self.request.files["dtiFile"]
        dtiFilename = ""
        for f in dtiFiles:
            fh = open(f"img/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
            dtiFilename = f"img/{f.filename}"
        
        t2Files = self.request.files["t2File"]
        t2Filename = ""
        for f in t2Files:
            fh = open(f"img/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
            t2Filename = f"img/{f.filename}"
        
        self.write("<h1>IMAGE CREATED</h1>")
        imageRegistration.run_registration(dtiFilename, t2Filename)

if (__name__  == "__main__"):
    app = tornado.web.Application([
        ("/", uploadHandler),
        ("/styles/(.*)", tornado.web.StaticFileHandler, {"path" : "styles"}),
        ("/img/(.*)", tornado.web.StaticFileHandler, {"path" : "img"})
    ])
    
    app.listen(3000)
    print("Listening on port 3000")
    
    tornado.ioloop.IOLoop.instance().start()