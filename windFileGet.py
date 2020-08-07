import paramiko
import time
import os


class getWindFile(object):  # 获取万得资讯的类
    def __init__(self, host_dict):  # 从字典引入初始化数据，这个类需要服务器IP端口，登录用户名密码，远程路径和本地路径，即可获取文件
        self.host = host_dict['host']
        self.port = host_dict['port']
        self.username = host_dict['username']
        self.password = host_dict['password']
        self.remote_path = host_dict['remote_path']
        self.local_path = host_dict['local_path']

    def connect(self):  # 登录服务器并生成paramiko对象
        tran = paramiko.Transport((self.host, self.port))  # tran是paramiko的一个连接对象，用于连接和操作
        tran.connect(username=self.username, password=self.password)
        self._tran = tran

    def close(self):  # 导入完成后需要关闭连接
        self._tran.close()

    def run_trans(self):  # 生成sftp对象
        sftp = paramiko.SFTPClient.from_transport(self._tran)
        self._sftp = sftp

    def get_remote_file(self):  # 获取远程文件前准备
        file_List = self._sftp.listdir(self.remote_path)  # 获取远程目录的文件列表
        print('{0}{1}{2}'.format('服务器资讯文件共', len(file_List), '个'))  # 统计共有多少个文件
        print(file_List)
        self.remote_path_file = []
        self.local_path_file = []
        for i in range(len(file_List)):  # 生成远程路径+文件名 和 本地路径+文件名的2个列表用于获取文件
            self.remote_path_file.append(self.remote_path + file_List[i])
            self.local_path_file.append(self.local_path + file_List[i])
        # return self.remote_path_file, self.local_path_file

    def getfile(self):  # 获取远程文件
        self.get_remote_file()
        print('开始资讯文件下载')
        print('{0}{1}{2}'.format('共有文件', len(self.remote_path_file), '个'))
        for i in range(len(self.remote_path_file)):
            print('{0}{1}{2}{3}'.format('开始下载第', i + 1, '个,文件路径为', self.remote_path_file[i]))
            self._sftp.get(self.remote_path_file[i], self.local_path_file[i])  # 文件下载
        print('资讯文件全部下载完成')

    def file_in_remote_path(self):
        return self._sftp.listdir(self.remote_path)  # 获取服务器文件列表


if __name__ == '__main__':
    print('脚本开始')
    time.sleep(2)
    d = time.strftime("%Y%m%d", time.localtime())  # 生成当日日期
    remote_path = '/home/report/wind/fileSync.linux_x64/WIND/DATA/JY/' + d + '/'  # 对于使用本脚本得人，在这里配置远程路径
    local_path = 'D:/wind/' + d + '/'  # 对于使用本脚本得人，在这里配置本地路径
    # 判断本地路径是否存在，如果不存在则新建本地路径
    print('开始判断本地路径是否存在')
    time.sleep(2)
    if not os.path.exists(local_path):
        try:
            os.mkdir(local_path)
            print('基于日期的路径不存在，已自动创建')
        except:
            print('wind路径不存在，请先创建,5秒后退出')
            time.sleep(5)
            exit('-1')
    print('路径判断完成')
    print('开始读取字典')
    time.sleep(2)
    # 对于使用本脚本得人，在这里配置服务器的连接配置
    host_dict = {
        'host': '10.8.198.238',  # sftp服务器IP
        'port': 22,  # sftp端口22
        'username': 'reportsftp',  # 服务器登录用户
        'password': 'YIy*Y94$d(8t',  # 服务器登录密码
        'remote_path': remote_path,
        'local_path': local_path,
    }
    print('字典读取完成')
    time.sleep(2)
    print('开始登录万得sftp服务器')
    time.sleep(2)
    getWindFile = getWindFile(host_dict)  # 生成类
    try:
        getWindFile.connect()  # 连接 生成paramiko对象
        print('paramiko对象生成成功')
    except:
        print('登录sftp服务器失败，请检查网络或者reportsftp用户密码是否被修改,5秒后退出')
        time.sleep(5)
        exit(-1)
    getWindFile.run_trans()  # 生成sftp对象

    print('判断远程文件是否更新')
    time.sleep(2)
    # 远程环境文件与本地不匹配时，再下载文件
    if sorted(getWindFile.file_in_remote_path()) == sorted(os.listdir(local_path)):
        print('本地文件与远程文件一致，无需下载')
    else:
        print('本地文件与远程文件不一致，3s后开始文件下载')
        time.sleep(3)
        try:
            getWindFile.getfile()  # 获取文件
            print('文件下载完成,5秒后关闭')
            time.sleep(5)
        except:
            print('文件下载失败，请重新下载，5秒后关闭')
            time.sleep(5)
        finally:
            getWindFile.close()  # 关闭
