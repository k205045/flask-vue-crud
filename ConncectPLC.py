from socket import *
from logger import _logging as Log
import threading
import time
import binascii
import struct
import codecs
import re
from socket import error as sckerror

class Mysocket():
    def __init__(self, host, port):
        self.k = Log()
        self.logger = self.k.Getlogger(__name__)
        self.HOST = host
        self.PORT = port
        self.conn = socket(AF_INET, SOCK_STREAM)
        self.conn.connect((self.HOST, self.PORT))
        self.conn.settimeout(10)
        # self.Connect()

    # "RD ZF100.U"
    # "WR ZF100.U 150"

    def Reconn(self):

        self.conn = socket(AF_INET, SOCK_STREAM)
        try:
            self.conn.connect((self.HOST, self.PORT))
        except:
            pass
        self.conn.settimeout(1)
        return self.conn


    def Send(self, register, value, bit=''):
        # cmd = "\x57\x52\x20\x5A\x46\x31\x30\x30\x2E\x44\x20\x38\x31\x35\x30\x30\x0D\x0A"
        cmd = "WR " + str(register) + bit + " " + str(value) + "\x0D"
        print(cmd)

        self.conn.sendall(cmd.encode())
        time.sleep(0.1)
        return self.conn.recv(1024).decode()


    def Sends(self, register, num,datas, bit=''):
        # cmd = "\x57\x52\x20\x5A\x46\x31\x30\x30\x2E\x44\x20\x38\x31\x35\x30\x30\x0D\x0A"
        self.__data = ""
        for x in datas:
            self.__data += " "+ str(x)
        # print(self.__data)
        cmd = "WRS " + str(register) + bit + " " + str(num) + self.__data + "\x0D"
        # print(cmd)
        self.conn.sendall(cmd.encode())
        # time.sleep(0.1)
        return self.conn.recv(1024).decode()



    def Get(self, register, bit=''):
        # cmd = "\x52\x44\x20\x5A\x46\x31\x30\x30\2E\55\x0D\x0A"
        cmd = "RD " + register + str(bit) +"\x0D"
        # print(cmd.encode())
        self.conn.sendall(cmd.encode())
        # a =
        # print(a)
        return self.conn.recv(1024).decode().strip()


    def Gets(self, register, nums, bit=''):
        # cmd = "\x52\x44\x20\x5A\x46\x31\x30\x30\2E\55\x0D\x0A"
        cmd = "RDS " + register + bit + ' ' + str(nums) +"\x0D"
        # print(cmd.encode())

        self.conn.sendall(cmd.encode())
        self.__list = []
        [self.__list.append(int(x)) for x in self.conn.recv(1024).decode().strip().split(" ")]
        return self.__list

    


if __name__ == '__main__':
    a = Mysocket("192.168.10.10",8501)
    print(a.Get("DM0",".U"))
    pass
    #  .U : 16位無符號十進位
    #  .S : 16位有符號十進位
    #  .D : 32位無符號十進位
    #  .L : 32位有符號十進位
    #  .H : 16位十六進位值數