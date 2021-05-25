from socket import *
from logger import _logging as Log
import threading
import time
from timer import _Timer as timer


class Mysocket():
    def __init__(self, host, port):
        self.logger = Log().Getlogger(__name__)
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
        # print(cmd)

        self.conn.sendall(cmd.encode())
        # time.sleep(0.1)
        return self.conn.recv(1024).decode()

    def Sends(self, register, num, datas, bit=''):
        # cmd = "\x57\x52\x20\x5A\x46\x31\x30\x30\x2E\x44\x20\x38\x31\x35\x30\x30\x0D\x0A"
        self.__data = ""
        for x in datas:
            self.__data += " " + str(x)
        # print(self.__data)
        cmd = "WRS " + str(register) + bit + " " + str(num) + self.__data + "\x0D"
        # print(cmd)
        self.conn.sendall(cmd.encode())
        # time.sleep(0.1)
        return self.conn.recv(1024).decode()

    def Get(self, register, bit='.U', logout= False):
        # cmd = "\x52\x44\x20\x5A\x46\x31\x30\x30\2E\55\x0D\x0A"
        cmd = "RD " + register + str(bit) + "\x0D"
        # print(cmd.encode())
        self.conn.sendall(cmd.encode())
        result = int(self.conn.recv(1024).decode().strip())
        if logout == True:
            print(result)
        return result

    def Gets(self, register, nums, bit='.U'):
        # cmd = "\x52\x44\x20\x5A\x46\x31\x30\x30\2E\55\x0D\x0A"
        cmd = "RDS " + register + bit + ' ' + str(nums) + "\x0D"
        # print(cmd.encode())

        self.conn.sendall(cmd.encode())
        self.__list = []
        [self.__list.append(int(x)) for x in self.conn.recv(1024).decode().strip().split(" ")]
        return self.__list

    def HeartLive(self, datasend):
        self.Send('DM7000', datasend, '.U')

    def Type(self):
        return self.Get('DM7001')

    def GB(self):
        return self.Get('DM7002')

    def barcodename(self):
        return self.Get('DM7003')

    def req_barcodename(self, action, datasend=""):
        if action == "W":
            self.Send('DM7004', datasend, '.U')
        elif action == "R":
            return self.Get('DM7004')

    def SSD_barcodename_Trigger(self, action, datasend=""):
        if action == "W":
            self.Send('DM7005', datasend, '.U')
        elif action == "R":
            return self.Get('DM7005')

    def SSD_barcodename_Result(self, action, datasend=""):
        if action == "W":
            self.Send('DM7006', datasend, '.U')
        elif action == "R":
            return self.Get('DM7006')

    def box_barcodename_Trigger(self, action, datasend=""):
        if action == "W":
            self.Send('DM7007', datasend, '.U')
        elif action == "R":
            return self.Get('DM7007')

    def box_barcodename_Result(self, action, datasend=""):
        if action == "W":
            self.Send('DM7008', datasend, '.U')
        elif action == "R":
            return self.Get('DM7008')

    def printer_num(self):
        return self.Get('DM7009')

    def printer(self, action, datasend=""):
        if action == "W":
            self.Send('DM7010', datasend, '.U')
        elif action == "R":
            return self.Get('DM7010',logout=False)

    def lab_barcodename_Trigger(self, action, datasend=""):
        if action == "W":
            self.Send('DM7011', datasend, '.U')
        elif action == "R":
            return self.Get('DM7011')

    def lab_barcodename_Result(self, action, datasend=""):
        if action == "W":
            self.Send('DM7012', datasend, '.U')
        elif action == "R":
            return self.Get('DM7012')

    def Error(self, action, datasend=""):
        if action == "W":
            self.Send('DM7013', datasend, '.U')
        elif action == "R":
            return self.Get('DM7013')

    def Getname(self):
        return self.conn.getsockname()

    def Close(self):
        self.conn.close()

    def socket_K1bareader_close(self):
        self.pr = False
        self.prin = True

        self.conn.sendall("LOFF\x0D".encode())

    def soc2(self):
        self.pr = True
        self.prin = False
        # self.conn = Mysocket("192.168.8.100", 9004)
        self.t = timer(2.5, self.socket_K1bareader_close, args=[], kwargs={})
        self.t.start()
        self.conn.sendall("LON\x0D".encode())
        while self.pr:
            self.recive = self.conn.recv(1024).decode()
            if self.recive != '':
                break
        if self.prin == True:
            self.t.cancel()
        if self.recive.strip() == "ERROR":
            self.logger.info("barcode not found")
        else:
            print(self.recive)


if __name__ == '__main__':

    soc = Mysocket("192.168.20.10", 8501)
    while True:
        print(soc.Get("DM7010"))
        time.sleep(1)

    # while True:
    #
    #     # t1.join()
    #     time.sleep(1)
    #     print(1)
    #     pass

    # for i in range(50):
    #     b.append(str(random.randint(0, 1)))
    # print(b)
    # socket.Sends('B076', 50, b)
    # print(socket.Gets('B076',50))
    # socket.Send('W04', 1, '.U')
    # socket.Send('W01', 5, '.U')
    # socket.Send('W02', 10, '.U')
    # socket.Send('W05',5144,'.U')
    # socket.Send('W06', 4509, '.U')
    # print(socket.Gets("DM000",150,'.U'))
    # while 1:
    #     print(socket.Gets("DM200", 50, '.D'))
    #     if len(socket.Gets("DM251", 50, '.D')) != 551:
    #         break
    #     if len(socket.Gets("DM301", 50, '.D'))!= 551:
    #         break
    # time.sleep(0.3)
    # socket.Get('CR2006') #RD 功能 兩個參�? 1.寄存�?2.資料格式
    # socket.Send('ZF100','.U') #WR 功能 兩個參�? 1.寄存�?2.資料格式
    # socket.Close() #關閉連線
    # socket.Reconn() #重�?
    # 資料格式如下:
    #  .U : 16位無符號十進位
    #  .S : 16位有符號十進位
    #  .D : 32位無符號十進位
    #  .L : 32位有符號十進位
    #  .H : 16位十六進位值數
    #
    # while 1:
    #     test = [str(a)] * 83
    #     socket.SendPLCinfo(test)
    #     a += 1
    #     time.sleep(1)
