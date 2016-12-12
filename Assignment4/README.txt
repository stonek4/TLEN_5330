TLEN 5330-002: Assignment 4

Contained in folder are two folders name Client and Server.
To run the server, navigate into the "Server" folder and run:

  python server.py [Server name] [Port]

Upon starting, the server will display:

  Server started...

To run the client, navigate into the "Client" folder and run:

  python client.py

Upon starting, the client will display:

  Client started...

If there is no directory already, the server will create a directory for itself
by the name given in the command.

The server supports 3 commands: GET, PUT, LIST

The server configuration file contains settings such as keep alive time.

The client configuration file contains settings for the number of servers
and the redundancy.  Both of these settings can be configured.  The client
configuration also specifies a username and password.

The client can send any of the three commands mentioned above to the server.


List will display the files contained on the server based on the user.  If there
are no files, nothing will be displayed.  If there are partial files then
incomplete will be displayed next to the file name.


Get will retrieve the requested file from the server.  If there are not enough
parts, the file retrieve will fail.


Put will distribute portions of a file to the servers based on the server and
redundancy settings.  Each file will be distributed based on its md5 hash.

The server  and client can be killed using CTRL-C.  Upon killing the server it
will try to exit processes regardless of what the processes are doing.


Extra credit:
The get command will only pull the portions of the file that it needs from the
servers.  It will not pull duplicate portions.



The python version used to test this program is:

  Python 2.7.12+

Do not delete the .pyc files within the subdirectories of this project.  In the
case that the project does not compile, you may try to recompile the project.
