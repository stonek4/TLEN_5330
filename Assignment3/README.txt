TLEN 5330-002: Assignment 3

Contained in folder is one folder named "Server".
To run the server, navigate into the "Server" folder and run:

  python server.py

  or

  python server.py [port#]

  or 

  python server.py [port#] [cache timeout]

Note: The port number can also be changed in the configuration settings, the
default cache timeout value cannot be changed but is set to 120.

Upon starting, the server will display:

  Server started...

The server directory is currently stored in Server/www/ where error files are
located.  The error files may be served back to the client if an error occurs.

Other settings can be changed in ws.conf including the file types, keep alive
time, port number and more (see configuration file)

When the server starts, it will wait for connections.  Upon receiving a
connection it will spin off a process to deal with that connection.  Within
the process, the request from the client will be parsed.

If the request is a valid request, the proxy will first check the cache to
see if a cached version of the file exists.  If it does, it will send the
cached header and the cached file to the user.

If the file does not exist in the cache, or the timeout for that cached file
has occurred, the proxy will make a connection with the server in the request
and send the request to the server.  When it receives the response it will
send the response back to the client, as well as write the response header and
content to a cached file.

Every 10 seconds the proxy will poll itself for active connections.  If there
are no active connections, then the proxy will begin a cache cleanup where it
will remove any files that are in the cache that are past the expiration time.

Extra Credit:   I did spend more time on trying to make a robust proxy than
on the link prefetching.  I began work on link prefetching but found that
many different types of links can be found in many different files and that
in order to do link fetching appropriately it would take a lot of time.

I did not do very much HTTP 1.1 testing however my proxy should be able to
handle HTTP 1.1 requests and it handles keep-alives to make sure that
multiple files can be requested from the same connection.
