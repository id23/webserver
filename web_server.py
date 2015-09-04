import socket
import datetime
import os.path
import imp



document_root = '/etc/page'
default_page = '/page.html'
host = 'localhost'
port = 1026
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(1)
dictionary = {}
date = datetime.datetime.now()

def lenght (fileaddr):
    file = open(fileaddr)
    filelenght = len(file.read())
    return filelenght

def execute_site (fileaddr,content_type,date ,file_type,file_name,socket_dictionary):
    if os.path.isfile(fileaddr) == True:
        header = 'HTTP/1.1 200 OK\r\n' \
                 'Server: Myserver\r\n' \
                 'Date:{0}\r\n' \
                 'Content-Type: '.format(date)+ content_type +'\r\n' \
                 'Content-Length:{0}\r\n\r\n'.format(lenght(fileaddr))
        open_file(fileaddr, header,file_type,file_name,socket_dictionary)
    else:
        header = 'HTTP/1.1 404 Not Found\r\n\r\n' \
                 '<html><body><h1>404 Page Not Found</h1></body></html>'

        csock.sendall(header)



def open_file(fileaddr, header,file_type,file_name, all_socket_dictionary):
    if file_type == 'py':
        try:
            imp.find_module(file_name[1:-3],[document_root])
            f, filename, description = imp.find_module(file_name[1:-3],[document_root])
            script_module = imp.load_module(file_name[1:-3],f,filename,description)
            request_handler = getattr( script_module , 'request_handler')
            html_output = request_handler(all_socket_dictionary)
        except:
            header='HTTP/1.1 500 Internal Error\r\n\r\n' \
                   '<html><body><h1>500 Internal Error</h1></body></html>'
            html_output = ''

        csock.sendall(header)
        csock.sendall(html_output)

    else:
        page = open(fileaddr)
        page_content = page.read()
        print "Connection from: " + `caddr`
        csock.sendall(header)
        csock.sendall(page_content)


def obtain_content_type(file_type_str):
    content_type = ''
    if file_type_str == '/' or file_type_str == 'html' or file_type_str == '':
        content_type = 'text/html'
    elif file_type_str == 'jpg' or file_type_str == 'jpeg':
        content_type = 'image/jpeg'
    elif file_type_str == 'py':
        content_type = 'text/html'

    if content_type == '':
        content_type = 'text/html'

    return content_type


def obtain_file_type(file_name_str):
    file_name_str = file_name_str.split('?')
    file_name_str = file_name_str[0]
    file_type_index = file_name_str.find(".")
    file_type = file_name_str[file_type_index + 1:]
    return file_type


def obtain_file_address(file_name_str):
    file_name_str = file_name_str.split('?')
    file_name_str = file_name_str[0]
    file_address = document_root + file_name_str
    if file_name_str == '/':
        file_address = document_root + default_page
    return file_address


def create_socket_dictionary(req):
    request_values = req.split("\r\n")
    i = 1
    for element in request_values:
        try:
            request_values[i] = request_values[i].split(":",1)
        except:
            "Do nothing"
        dictionary_elements = request_values[1:]
        try:
            dictionary[dictionary_elements[i - 1][0]] = dictionary_elements[i - 1][1]
        except:
            "Do nothing"
        i = i + 1
    return dictionary

while True:

    csock, caddr = sock.accept()
    req = csock.recv(1024)
    if len(req) > 0:
        lines = req.split()
        socket_dictionary = create_socket_dictionary(req)
        all_socket_dictionary = {'method': lines[0], 'url': lines[1], 'request_headers': socket_dictionary, 'request_data': lines[-1]}
        file_name = lines[1]
        file_address = obtain_file_address(file_name)
        file_type = obtain_file_type(file_name)
        content_type = obtain_content_type(file_type)
        execute_site (file_address,content_type,date,file_type,file_name,all_socket_dictionary)

    csock.close()
