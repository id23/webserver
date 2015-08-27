import socket
import datetime
import Image

document_root = '/etc/page/'
host = 'localhost'
port = 1026
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)

date = datetime.datetime.now()

def lenght (fileaddr):
    file = open(fileaddr)
    filelenght = len(file.read())
    return filelenght

while True:
    csock, caddr = sock.accept()

    req = csock.recv(1024)
    lines = req.split()
    file_name = lines[1].split("/")
    file_name_list = ''.join(file_name[-1:])
    file_address = document_root + file_name_list
    if file_name_list == '':
        file_address = '/etc/page/page.html'
    file_type = file_name_list.split(".")
    file_type_list = ''.join(file_type[-1:])

    if file_type_list == '':
        content_type = 'text/html'
    elif file_type_list == 'html':
        content_type = 'text/html'
    elif file_type_list == 'jpg' or file_type_list == 'jpeg':
        content_type = 'image/jpeg'

    header = 'HTTP/1.1 200 OK\r\n' \
             'Server: Myserver\r\n' \
             'Date: {0}\r\n' \
             'Content-Type: '+ content_type +'\r\n' \
             'Content-Length:{1}\r\n\r\n'.format(date, lenght(file_address))

    page = open(file_address)
    page_content = page.read()
    print "Connection from: " + `caddr`
    csock.sendall(header)
    csock.sendall(page_content)
    csock.close()

