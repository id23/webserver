import socket
import datetime
import os.path
import sys
import imp
import time
import cgi



document_root = '/page'
default_page = '/page.html'
host = 'localhost'
port = 1026
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(1)
dictionary = {}
request_data_dictionary = {}
date = datetime.datetime.now()
form =cgi.FieldStorage()

def lenght (fileaddr):
    file = open(fileaddr)
    filelenght = len(file.read())
    return filelenght

def execute_site (fileaddr,content_type,date ,file_type,file_name,all_socket_dictionary):
    if os.path.isfile(fileaddr) == True:
        header_dictionary={'HTTP':'HTTP/1.1 200 OK\r\n', \
                 'Server':' Myserver\r\n', \
                 'Date':'{0}\r\n'.format(date), \
                 'Content-Type': content_type +'\r\n', \
                 'Content-Lenght':'{0}\r\n\r\n'.format(lenght(fileaddr))}

        all_socket_dictionary['header']= header_dictionary
        open_file(fileaddr,file_type,file_name,all_socket_dictionary)
    else:
        header = 'HTTP/1.1 404 Not Found\r\n\r\n' \
                 '<html><body><h1>404 Page Not Found</h1></body></html>'
        csock.sendall(header)



def open_file(fileaddr,file_type,file_name, all_socket_dictionary):
    if file_type == 'py':
        file_name = file_name.split("?")
        file_name = file_name[0]
        try:
            imp.find_module(file_name[1:-3],[document_root])
            f, filename, description = imp.find_module(file_name[1:-3],[document_root])
            script_module = imp.load_module(file_name[1:-3],f,filename,description)
            request_handler = getattr( script_module , 'request_handler')
            all_socket_dictionary = request_handler(all_socket_dictionary)
            header = all_socket_dictionary['header']['HTTP']+'Server:'+all_socket_dictionary['header']['Server']+'Date:' + all_socket_dictionary['header']['Date']+ \
            'Content-Type:'+all_socket_dictionary['header']['Content-Type']+'Content-Lenght:'+all_socket_dictionary['header']['Content-Lenght']

        except:
            print "Unexpected error:", sys.exc_info()[0]
            header = all_socket_dictionary['header']='HTTP/1.1 500 Internal Error\r\n\r\n' \
                   '<html><body><h1>500 Internal Error</h1></body></html>'
            all_socket_dictionary['html_output'] = ''
        #header = all_socket_dictionary['header']['HTTP']+'Server:'+all_socket_dictionary['header']['Server']+'Date:' + all_socket_dictionary['header']['Date']+ \
        #'Content-Type:'+all_socket_dictionary['header']['Content-Type']+'Content-Lenght:'+all_socket_dictionary['header']['Content-Lenght']
        csock.sendall(header)
        csock.sendall(all_socket_dictionary['html_output'])
        print "Connection from: " + `caddr`
    else:
        header = all_socket_dictionary['header']['HTTP']+'Server:'+all_socket_dictionary['header']['Server']+'Date:' + all_socket_dictionary['header']['Date']+ \
        'Content-Type:'+all_socket_dictionary['header']['Content-Type']+'Content-Lenght:'+all_socket_dictionary['header']['Content-Lenght']
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
    #print file_name_str
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


def recv_timeout(the_socket,timeout=0.5):
    the_socket.setblocking(0)
    total_data=[];begin=time.time()
    while 1:

        #if you got some data, then break after wait sec
        if total_data and time.time()-begin>timeout:
            break
        #if you got no data at all, wait a little longer
        elif time.time()-begin>timeout*2:
            break

        try:
            data=the_socket.recv(8192)
            if data:
                total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return ''.join(total_data)


while True:

    csock, caddr = sock.accept()
    req = recv_timeout(csock)
    if len(req) > 0:
            lines = req.split()
            #print lines[34]
            try:
                image_name = lines[34].split('"')
                #print image_name[1]
                #image_name = image_name[1]
                #print image_name
                sup_lines = req.split('boundary=',1)
                sup_lines = sup_lines[1].split('Content-Type: image/jpeg')
                sup_lines = sup_lines[1].split('\r\n\r\n',1)
                request_data_dictionary = {'x-www_type':lines[-1],'multipart_type_n1':lines[-2],'multipart_type_n2':lines[-7], 'multipart_type_image':sup_lines[1], 'image_name':image_name[1]}
                #print request_data_dictionary['image_name']
            except:
                request_data_dictionary = {'x-www_type':lines[-1],'multipart_type_n1':lines[-2],'multipart_type_n2':lines[-7]}
            socket_dictionary = create_socket_dictionary(req)
            all_socket_dictionary = {'method': lines[0], 'url': lines[1], 'request_headers': socket_dictionary, 'request_data': request_data_dictionary}
            #print all_socket_dictionary
            file_name = lines[1]
            file_address = obtain_file_address(file_name)
            file_type = obtain_file_type(file_name)
            content_type = obtain_content_type(file_type)
            execute_site (file_address,content_type,date,file_type,file_name,all_socket_dictionary)

    csock.close()
