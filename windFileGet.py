import paramiko
import time


class getWindFile(object):
    def __init__(self, host_dict):
        self.host = host_dict['host']
        self.port = host_dict['port']
        self.username = host_dict['username']
        self.password = host_dict['password']
        self.remotepath = host_dict['remotepath']
        self.localpath = host_dict['localpath']

    def connect(self):
        tran = paramiko.Transport((self.host, self.port))
        tran.connect(username=self.username, password=self.password)
        self._tran = tran

    def close(self):
        self._tran.close()

    def runTrans(self):
        sftp = paramiko.SFTPClient.from_transport(self._tran)
        self._sftp = sftp

    def getRemotefile(self):
        fileList = self._sftp.listdir(self.remotepath)
        print('{0}{1}{2}'.format('服务器资讯文件共', len(fileList), '个'))
        print(fileList)
        self.remotepath_file = []
        self.localpath_file = []
        for i in range(len(fileList)):
            self.remotepath_file.append(self.remotepath + fileList[i])
            self.localpath_file.append(self.localpath + fileList[i])
        # return self.remotepath_file, self.localpath_file

    def getFile(self):
        self.getRemotefile()
        print('开始资讯文件下载')
        print('{0}{1}{2}'.format('共有文件', len(self.remotepath_file), '个'))
        for i in range(len(self.remotepath_file)):
            print('{0}{1}{2}{3}'.format('开始下载第', i+1, '个,文件路径为', self.remotepath_file[i]))
            self._sftp.get(self.remotepath_file[i], self.localpath_file[i])
        print('资讯文件全部下载完成')


if __name__ == '__main__':
    d = time.strftime("%Y%m%d", time.localtime())
    remotepath = '/home/oracle/wind/fileSync.linux_x64/WIND/DATA/JY/' + d + '/'
    localpath = 'D:/zixun/'
    host_dict = {
        'host': '10.1.92.110',
        'port': 22,
        'username': 'oracle',
        'password': 'oracle#123',
        'remotepath': remotepath,
        'localpath': localpath,
    }

    getWindFile = getWindFile(host_dict)
    getWindFile.connect()
    getWindFile.runTrans()
    getWindFile.getFile()
