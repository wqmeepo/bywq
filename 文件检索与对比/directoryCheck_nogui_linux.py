import os
import csv


class DigFileFromPath(object):
    def __init__(self):
        self.remote_path = '/home/hundsun/scanfile/clientfile/'
        self.save_path = '/home/hundsun/scanfile/clientfile_result/'

    def getFileFromPath(self):
        for dir_in_remote_path in os.listdir(self.remote_path):
            path_in_remote_path = os.path.join(self.remote_path, dir_in_remote_path)
            if os.path.isdir(path_in_remote_path):
                fileList = []
                for root, dirs, files in os.walk(path_in_remote_path):
                    for file in files:
                        fileList.append(file)
                with open(os.path.join(self.save_path, dir_in_remote_path + '.csv'), 'w+') as f:
                    writer = csv.writer(f, dialect='excel')
                    for i in fileList:
                        writer.writerow([i])
            elif os.path.isfile(path_in_remote_path):
                fileList = []
                fileList.append(dir_in_remote_path)
                with open(os.path.join(self.save_path, 'notInDir.csv'), 'a+') as f:
                    writer = csv.writer(f, dialect='excel')
                    for i in fileList:
                        writer.writerow([i])


if __name__ == '__main__':
    DigFile = DigFileFromPath()
    DigFile.getFileFromPath()
