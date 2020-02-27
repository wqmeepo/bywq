import os

new_date = input('输入想跳到的日期（MMDD）= ')
msg_dir = "E:/TODO/资讯接口/资讯文件"
files = os.listdir(msg_dir)
for name in files:
    new_file_name = name.split('2019')[0] + '2019' + new_date + '.' + name.split('.')[1]
    os.rename(
        os.path.join(msg_dir, name),
        os.path.join(msg_dir, new_file_name)
    )
print('日期更换完毕')
