import socket
import datetime
import Image

document_root = '/home/u1/page/ws'
host = '0.0.0.0'
port = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
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
    #print req

    lines = req.split()

    file_name_list = lines[1]
    print file_name_list
    file_address = document_root + file_name_list
    print file_address
    if file_name_list == '/':
        file_address = '/home/u1/page/ws/page.html'
    file_type = file_name_list.find(".")
    file_type_list = file_name_list[file_type + 1:]
    #file_type_list = ''.join(file_type[-1:])
    print file_type
    print file_type_list
    if file_type_list == '/' or file_type_list == 'html':
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

