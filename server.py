import os
import flask
import requests
import json
import urllib
from verify import verifySignature, getAuth
from data import Request

app = flask.Flask(__name__)
sess = requests.Session()

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "DELETE"])
def proxy(path):
  try:
    #print(flask.request.cookies)
    auth = flask.request.cookies.get('auth')
    userinfo = getAuth(auth)
  except Exception as e:
  #except ZeroDivisionError as e:
    if flask.request.cookies.get('auth'):
      print(e)
    return flask.Response("<h1>Unauthorized</h1><p>Your client did not send any authorization data. Please obtain an authorization token and try again.</p>", status=401, mimetype='text/html')

  try:
    resp = {"status_code": 400}
    url = os.environ["REPLIT_DB_URL"]
    if flask.request.path != "/":
      url += flask.request.path
  
    proxreq = requests.Request(flask.request.method, url, data=flask.request.form, params=flask.request.args).prepare()
    if flask.request.method == "GET":
      resp = sess.send(proxreq)
      req = Request(flask.request, resp.text, auth)
    else:
      resp = False
      req = Request(flask.request, False, auth)
  
    #print("RESP:", resp.text)
  
  
    if (filteredResp := accessCheck(req)) is None:
      return flask.Response("<h1>Forbidden</h1><p>Your client tried to access a resource but doesn't have the required permissions to view them.</p>", status=403, mimetype='text/html')
  
    if flask.request.method != "GET":
      resp = sess.send(proxreq)
  
    #print("REPR RESP.TEXT:", repr(resp.text))
    #print("RESP.TEXT", resp.text)
    #print("FILTEREDRESPTEXT:", repr(urllib.parse.quote("\n".join(filteredResp))))
    output = ""
    if req._method == "LIST":
      output = "\n".join([urllib.parse.quote(x) for x in filteredResp])
    elif req._method == "GET":
      output = json.dumps(filteredResp)
    else:
      output = ""
      
    #print("REPR OUTPUT:", repr(output))
    #  
    #print("OUTPUT:", output)
    #
    #print("RESP:", resp.status_code)
    #
    #print("CONDITION:", resp.text == output)
  except Exception as e:
    if resp.status_code == 400:
        return flask.Response("<h1>Bad or malformed request</h1><p>Your client tried to tell us something, but we couldn't quite understand what they were trying to say.</p>", status=400, mimetype='text/html')
    else:
        return flask.Response("<h1>Database Error</h1>Your client tried to access a resource, but the database server couldn't complete that request.</p>", status=resp.status_code, mimetype='text/html')
    print(e, resp.status_code)
  
  proxy_resp = flask.make_response(output)
  proxy_resp.status_code = resp.status_code
  for k, v in resp.headers.items():
    if k.lower() != "content-length":
      proxy_resp.headers[k] = v
    else:
      proxy_resp.headers[k] = len(output)

  return proxy_resp

def start(acl):
  global accessCheck
  accessCheck = acl
  return app.run
