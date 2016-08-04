import sys, string,cStringIO, cgi,time,datetime
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs

query_components = parse_qs(urlparse(self.path).query)
source = query_components["source"] 
destination = query_components["destination"] 

class MyHandler(BaseHTTPRequestHandler):

# I WANT TO EXTRACT imsi parameter here and send a success response to 
# back to the client.
def do_GET(self):
    try:
        if self.path.endswith(".html"):
            #self.path has /index.htm
            f = open(curdir + sep + self.path)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("<h1>Device Static Content</h1>")
            self.wfile.write(f.read())
            f.close()
            return
        if self.path.endswith(".esp"):   #our dynamic content
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("<h1>Dynamic Dynamic Content</h1>")
            self.wfile.write("Today is the " + str(time.localtime()[7]))
            self.wfile.write(" day in the year " + str(time.localtime()[0]))
            return

        # The root
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        lst = list(sys.argv[1])
        n = lst[len(lst) - 1]
        now = datetime.datetime.now()

        output = cStringIO.StringIO()
        output.write("<html><head>")
        output.write("<style type=\"text/css\">")
        output.write("h1 {color:blue;}")
        output.write("h2 {color:red;}")
        output.write("</style>")
        output.write("<h1>Device #" + n + " Root Content</h1>")
        output.write("<h2>Device Addr: " + sys.argv[1] + ":" + sys.argv[2] + "</h1>")
        output.write("<h2>Device Time: " + now.strftime("%Y-%m-%d %H:%M:%S") + "</h2>")
        output.write("</body>")
        output.write("</html>")

        self.wfile.write(output.getvalue())

        return

    except IOError:
        self.send_error(404,'File Not Found: %s' % self.path)

#import sqlite3

#sqlite3.connect("wiki.sql")

#return "Made it to wiki.py"