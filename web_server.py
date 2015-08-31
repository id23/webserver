import socket
import datetime
import os.path
document_root = '/etc/page'
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
    content_type = ''
    file_name_list = lines[1]
    file_address = document_root + file_name_list
    if file_name_list == '/':
        file_address = document_root + '/page.html'
    file_type_index = file_name_list.find(".")
    file_type_list = file_name_list[file_type_index + 1:]

    header_get = "HTTP/1.1 200 OK\r\n"

    if file_type_list == '/' or file_type_list == 'html' or file_type_list == '':
        content_type = 'text/html'
    elif file_type_list == 'jpg' or file_type_list == 'jpeg':
        content_type = 'image/jpeg'

    if os.path.isfile(file_address) == False:
        header_get = 'HTTP/1.1 404 Not Found \r\n'
        file_address = document_root + '/404page.html'
        content_type = 'text/html'
    if content_type == '':
        content_type = 'text/html'
    header = header_get + \
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
