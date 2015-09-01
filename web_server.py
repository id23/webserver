import socket
import datetime
import os.path
document_root = '/etc/page'
default_page = '/page.html'
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

def site_execution (fileaddr,content_type,date):
    if os.path.isfile(fileaddr) == True:
        header = 'HTTP/1.1 200 OK\r\n' \
                 'Server: Myserver\r\n ' \
                 'Date: {0}\r\n ' \
                 'Content-Type: '+ content_type +'\r\n' \
                 'Content-Length:{1}\r\n\r\n'.format(date, lenght(fileaddr))
        file_open(fileaddr, header)
    else:
        header = 'HTTP/1.1 404 Not Found\r\n' \

        csock.sendall(header)



def file_open(fileaddr, header):
    page = open(fileaddr)
    page_content = page.read()
    print "Connection from: " + `caddr`
    csock.sendall(header)
    csock.sendall(page_content)


def content_type_define(file_type_str):
    content_type = ''
    if file_type_str == '/' or file_type_str == 'html' or file_type_str == '':
        content_type = 'text/html'
    elif file_type_str == 'jpg' or file_type_str == 'jpeg':
        content_type = 'image/jpeg'
    if content_type == '':
        content_type = 'text/html'
    return content_type


def file_type_define(file_name_str):
    file_type_index = file_name_str.find(".")
    file_type = file_name_str[file_type_index + 1:]
    return file_type


def file_address_define(file_name_str):
    file_address = document_root + file_name_str
    if file_name_str == '/':
        file_address = document_root + default_page
    return file_address


while True:

    csock, caddr = sock.accept()
    req = csock.recv(1024)
    if req == '':
        csock.close()
    else:
        lines = req.split()
        file_name = lines[1]
        file_address = file_address_define(file_name)
        file_type = file_type_define(file_name)
        content_type = content_type_define(file_type)
        site_execution (file_address,content_type,date)
        csock.close()
