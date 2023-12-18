import pickle

from utils.file_info import *
"""
+----------------+------------------+---------------------------------+
|                |                  |                                 |
|  tipo mensagem | tamanho mensagem |   mensagem                      |
|    1 byte      |     2  bytes     |                                 |
+----------------+------------------+---------------------------------+
"""
#definir nomes para os numeros de tipo de mensagem
REGISTER_NODE = 0
DELETE_NODE = 1
#Okay has no data field since it's not needed, the Default None is used so we just create a regular Tracker_packet with type OK
OKAY = 2
#file not found has no data field
FILE_NOT_FOUND = 3


ADD_FILES = 10
REMOVE_FILE = 11
REQUEST_FILE = 12
REQUEST_FILE_RESPONSE = 13
LIST_FILES = 14
REMOVE_FILE = 15

#definining file hash protocol universally
FILE_HASHING_PROTOCOL = "sha1"


#creates a packet with the given parameters (data length is NOT verified, methods that implement it should make sure the data fits in a single packet)
def create_tracker_packet(type:int, data:bytes):
        #The type is converted to bytes
        type_bytes = type.to_bytes(1,'little')
        if data != None:
            #The size is determined and converted to bytes
            size = len(data)
            size_bytes = size.to_bytes(2,'little')
            #The packet is assembled and returned
            return type_bytes + size_bytes + data
        else:
            size = 0
            size_bytes = size.to_bytes(2,'little')
            #The packet is assembled and returned
            return type_bytes + size_bytes
    
    
#Correctly receives a packet given a connection
def receive_packet_from_socket(conn):
    
    message_bytes = conn.recv(65535)
    
    msg_type_bytes = message_bytes[:1]
    message_bytes = message_bytes[1:]
    msg_type = int.from_bytes(msg_type_bytes,'little')
    
    msg_length_bytes = message_bytes[:2]
    message_bytes = message_bytes[2:]
    #translates the message length from bytes to an int
    msg_length = int.from_bytes(msg_length_bytes,'little')
   
    data = message_bytes[:msg_length]
    return msg_type, data
                    

class Register_Node_Packet:
    
    def __init__(self):
        #para já inutil, no futuro dirá o seu hostname
        self.host_name = "" 
    
    def serialize(self):
        #Cria uma variável de bytes e serializa-os
        serialized_packet: bytes  = pickle.dumps(self,pickle.HIGHEST_PROTOCOL)
        return serialized_packet
    
    def deserialize(serialized_packet):
        #deserializa o pacote dados os bytes do mesmo
        packet: Register_Node_Packet = pickle.loads(serialized_packet)
        return packet
    
class Unregister_Node_Packet:
    
    def __init__(self):
        #para já inutil, no futuro dirá o seu hostname
        self.host_name = "" 
    
    def serialize(self):
        #Cria uma variável de bytes e serializa-os
        serialized_packet: bytes  = pickle.dumps(self,pickle.HIGHEST_PROTOCOL)
        return serialized_packet
    
    def deserialize(serialized_packet):
        #deserializa o pacote dados os bytes do mesmo
        packet: Unregister_Node_Packet = pickle.loads(serialized_packet)
        return packet
    
class Remove_File_Packet:
    
    #creates a packet to remove files according to their hash 
    def __init__(self,file_hashes):
        #array of hashes of the files that got deleted
        self.file_hashes = file_hashes
        
    def serialize(self):
        #Cria uma variável de bytes e serializa-os
        serialized_packet: bytes  = pickle.dumps(self,pickle.HIGHEST_PROTOCOL)
        return serialized_packet
    
    def deserialize(serialized_packet):
        #deserializa o pacote dados os bytes do mesmo
        packet: Remove_File_Packet = pickle.loads(serialized_packet)
        return packet
    
class Add_File_PacketContent:
    
    def __init__(self,name:str ,size : int, chunks : []):
        self.name = name
        self.size = size
        self.chunks = chunks
    
#Dizer ao servidor que tem ficheiros novos
class Add_File_Packet:
    
    def __init__(self,fileinfos: {}):
        #Dicionário de chave hash e valor class Add_FilePacketContent, definido acima
        self.files = fileinfos
    
    def getFiles(self):
        return self.files
            
    def serialize(self):
        #Cria uma variável de bytes e serializa-os
        serialized_packet: bytes  = pickle.dumps(self,pickle.HIGHEST_PROTOCOL)
        return serialized_packet
    
    def deserialize(serialized_packet):
        #deserializa o pacote dados os bytes do mesmo
        packet: Add_File_Packet = pickle.loads(serialized_packet)
        return packet

#Pedido de um cliente ao servidor de um ficheiro novo
class File_Request_Packet:
    
    def __init__(self,hash):
        self.hash = hash

    def getHash(self):
        return self.hash

    def serialize(self):
        #Cria uma variável de bytes e serializa-os
        serialized_packet: bytes  = pickle.dumps(self,pickle.HIGHEST_PROTOCOL)
        return serialized_packet
    
    def deserialize(serialized_packet):
        #deserializa o pacote dados os bytes do mesmo
        packet: File_Request_Packet = pickle.loads(serialized_packet)
        return packet        


class File_Request_Response_Packet:
    
    def __init__(self,nodeinfo:FileInfo):
        #do tipo class FileInfo
        self.nodeinfo = nodeinfo
        
    def serialize(self):
        #Cria uma variável de bytes e serializa-os
        serialized_packet: bytes  = pickle.dumps(self,pickle.HIGHEST_PROTOCOL)
        return serialized_packet
    
    def deserialize(serialized_packet):
        #deserializa o pacote dados os bytes do mesmo
        packet: File_Request_Response_Packet = pickle.loads(serialized_packet)
        return packet   


class List_Files_Packet:
    
    def __init__(self, lista_ficheiros):
        # lista de ficheiros convertido em lista
        self.list_files = lista_ficheiros
    
    def serialize(self):
        #Cria uma variável de bytes e serializa-os
        serialized_packet: bytes  = pickle.dumps(self,pickle.HIGHEST_PROTOCOL)
        return serialized_packet
    
    def deserialize(serialized_packet):
        #deserializa o pacote dados os bytes do mesmo
        packet: List_Files_Packet = pickle.loads(serialized_packet)
        return packet
    
class Remove_File_Packet:
    
    def __init__(self, filehashes):
        # lista de ficheiros convertido em lista
        self.hashes = filehashes
    
    def serialize(self):
        #Cria uma variável de bytes e serializa-os
        serialized_packet: bytes  = pickle.dumps(self,pickle.HIGHEST_PROTOCOL)
        return serialized_packet
    
    def deserialize(serialized_packet):
        #deserializa o pacote dados os bytes do mesmo
        packet: Remove_File_Packet = pickle.loads(serialized_packet)
        return packet