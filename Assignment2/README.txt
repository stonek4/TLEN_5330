TLEN 5330-002: Assignment 1

Contained in folder are two folders named "Client" and "Server".  To run the
client, navigate into the "Client" folder and run:

  python client.py [ip address] [port #]

To run the server, navigate into the "Server" folder and run:

  python server.py [port #]

Upon starting, the client will display:

  Client started, available commands are:
  put [file_name]
  get [file_name]
  list
  exit

The client will also behind the scenes send a message to the server to see if
it can reach the server.  If it cannot reach the server it will display a
message like:

  Timed out, didn't receive packet.
  Initial server contact failed, if server is started, maybe try using a different port?

Upon starting, the server will display:

  Server started...

The client "directory" is stored in "Client/Client_Files".  The files stored in
the client directory to begin with are:

  foo1.txt
  foo2.jpg
  foo3.zip

The server "directory" is stored in "Server/Server_Files".  There are no files
in the server directory to begin with.

The python version used to test this program is:

  Python 2.7.12

Do not delete the .pyc files within the subdirectories of this project.  In the
case that the project does not compile, you may try to recompile the project.

Extra credit:  Although I did not do a system of sending duplicate packets, I
did implement Stop and Wait in order to reduce file transfer errors.  Upon
sending large files, the sender will send one packet at a time, and will wait
for an acknowledgement from the receiver.  If it does not get an acknowledgement
it will resend the file and will display output.  If the sender or receiver times
out 5 times, It will permanently timeout and display that the file transfer failed.
I realize that this is not a completely fool proof method as corrupted packets are
not caught, however it does make sure that every packet reaches the receiver, and
sending duplicates is not fool proof either, as well as taking twice as much data
to send each file. 
