import urllib
import json


class Request():
  def __init__(self, req, res, auth):
    #print("RAW RESP:", res)
    self._req = req
    self._method = self._req.method
    self.method = self._method
    if self.method == "GET":
      self.payload = ""
      self.key = urllib.parse.unquote(self._req.path[1:])
      if self.key:
        self.response = json.loads(urllib.parse.unquote(res))
      elif not self.key:
        self.method = "LIST"
        self._method = "LIST"
        self.response = [urllib.parse.unquote(x) for x in res.split("\n")]
    elif self.method == "POST":
      self.key = list(self._req.form.keys())[0]
      self.response = ""
      self.payload = self._req.form[self.key]
    elif self.method == "DELETE":
      self.key = urllib.parse.unquote(self._req.path[1:])
      self.response = ""
      self.payload = ""
    
    
    #self.key = (urllib.parse.unquote(self._req.path[1:]) 
    #            if self.method != "POST" else 
    #            list(self._req.form.keys())[0])
    #self.response = urllib.parse.unquote(res) if self.key else [urllib.parse.unquote(x) for x in res.split("\n")]
    #self.payload = self._req.form[self.key] if self.method == "POST" else False
    #print(self.key, self.payload)

    self.user = AuthUser(auth)

    #print("KEY:", self.key)
    #print("RESP:", self.response)
    #print("MTHD:", self.method)
    #print("PAYLOAD:", self.payload)


class AuthUser():
  def __init__(self, auth):
    self._auth = json.loads(json.loads(auth)['payload'])
    #print(self._auth)
    self.name, self.id = self._auth['username'], self._auth['id']
    



#print("KEY  :", urllib.parse.unquote(flask.request.path[1:]))
#print("METHOD:", flask.request.method)
#if flask.request.method != "GET":
#  print("BODY  :", flask.request.get_req())
#else:
#  print("QUERY :", flask.request.args)