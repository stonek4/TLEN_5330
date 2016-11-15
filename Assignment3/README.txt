TLEN 5330-002: Assignment 2

Contained in folder is one folder named "Server".
To run the server, navigate into the "Server" folder and run:

  python server.py

Upon starting, the server will display:

  Server started...

The server directory is currently stored in Server/www/ where index.html is the
default file. This can be changed in the server configuration file which is
located at Server/ws.conf

Other settings can be changed in ws.conf including the file types, keep alive
time, port number and more (see configuration file)

In order to test the server, use commands such as GET and POST, or access
the server using the browser.  By default the server will use the localhost
ip address so you could type that and the port number into the browser in
order to access the default page.

Using the page that is currently in the www directory, you can also send post
requests to the server by typing into the input box and pressing enter.

The program can handle a few different types of errors by sending a generic
error file to the client. Errors handled are:

  400
  404
  500
  501

In general any unknown errors fall under 500 when processing commands.

It is a known bug that if you remove html from the configuration file that
the server will not be able to show errors to the client.

The server can be killed using CTRL-C.  Upon killing the server it will
try to exit processes regardless of what the processes are doing.

The python version used to test this program is:

  Python 2.7.12

Do not delete the .pyc files within the subdirectories of this project.  In the
case that the project does not compile, you may try to recompile the project.

Extra credit: POST commands work, but need a certain html class in order to work
