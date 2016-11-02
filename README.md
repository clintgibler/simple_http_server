# Simple HTTP Server

This is a minimal HTTP server the listens to all paths on a given port
  and dumps what it sees to STDOUT, including:
* Requesting IP
* URL/POST body params
* Headers

Sometimes you're testing a web app or network service and you're confirm
  (or exploiting) remote code execution (RCE).
You can run this server to test if your attack can make outbound connections and
  then extract information.

The advantage of using this over Python's builtin `SimpleHTTPServer` or `netcat`/`nc`
  is that it's more flexible, if you need to rapidly iterate some additional functionality.

## Installation/Running It

This was written in Python 3 but should work fine in Python 2.

```bash
# Install dependencies
$ pip3 install -r requirements.txt --user

# Run the server
$ python3 server.py
```

## Features

* For any request, this server prints the source IP, request method and any headers, which is useful for
  verifying connectivity and a bit of fingerprinting of the host (via `User-Agent` header).
* Routes:
  * POST `/file/filename=<supplied_file_name>` - any content POSTed to here will be saved to
    `loot/<supplied_file_name>`
  * GET `/payloads/<filepath>` - serves any file in `payloads/<filepath>` - useful for supplying malicious
    payloads/scripts to a victim machine which can then be run.
  * A default controller that will match all other routes.
