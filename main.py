#! /usr/bin/env python3
"""A complex and secure proxy to Repl.it Database.

Great for safely sharing one database among many repls, while
preventing abuse to resources which fall under your name.

Copyright @python660, All Rights Reserved.
Licensed under the MIT License, attribution
required for commercial use. Please see LICENSE.md
for more information."""

from server import start
from replit import db

def ACL(req):
  #print("USERNAME:", req.user.name)
  """
  Input: Request object
    req.response: The response of said operation (or list of keys for a "GET /")
    req.key: The wanted key (only the first layer)
    req.method: One of LIST, GET, POST, DELETE
    req.payload: The data of the new variable
    req.user: An AuthUser object
      req.user.name: The user's username (CAN CHANGE)
      req.user.id: The user's id (DOES NOT CHANGE)

  Output: Object or None

  NOTE: TO REJECT A REQUEST YOU MUST RETURN ONLY "NONE", NOT
  FALSE OR ANY OTHER EQUIVALENT FALSELY OBJECT.

  NOTE: If a certain field does not exist because it is not applicable
  for the current request, its value will be an empty string.

  NOTE: Despite being a dict, the Replit Database only sends HTTP
  requests to get the ROOT LEVEL information. That means any data
  that is "nested" will not be retrieved specifically, but either
  from memory or from a GET request referencing the ROOT LEVEL key
  name. This is important and if you didn't pay attention then
  don't blame me for not telling you.
  """
  #if req.user.name == "python660":
  #  # Allow all requests from the admin
  #  return req.response

  if req.method == "LIST":
    # Allow listing registered users
    return req.response

  elif req.method == "GET":
    # Allow reading all user's public info
    if type(req.response) is dict:
      # Filter response to only include "public" information
      filtered = dict([(x, req.response[x]) for x in req.response if (x == "public" or req.key == req.user.name) and not req.response.get("deleted")])
      return filtered
    else:
      # You can't access anything that's not a dict. 
      # Why would user data not be a dict?
      # Only allow resources that you strictly need.
      return

  elif req.method == "POST":
    # Only allow write access to their username's value
    if req.key == req.user.name:
      return req.response

  elif req.method == "DELETE":
    # Only allow users to delete content listed under
    # their username, not the whole entry itself.
    return
  else:
    # Anomalies should be rejected.
    return


start(ACL)("::")