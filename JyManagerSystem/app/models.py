from . import db
from datetime import datetime


# 用户信息表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(200))
    realname = db.Column(db.String(40), default='')  # 真实姓名
    department = db.Column(db.String(40), default='')  # 部门
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return f'<user : {self.department} - {self.realname}>'

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)


# 管理员信息表
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    manager = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(200))

    def __repr__(self):
        return f'<managerName : {self.manager}>'

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)


#  数据库字段表信息表
class TableInfo(db.Model):
    __tablename__ = "tableinfo"
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(20), index=True)
    table_describe = db.Column(db.String(100), index=True)
    sys_no = db.Column(db.String(5), default='')
    db_name = db.Column(db.String(40), default='')
    field_name = db.Column(db.String(20), index=True)
    field_describe = db.Column(db.String(100), index=True)
    field_describe_detail = db.Column(db.Text, nullable=True, default='')
    db.Index('idx_search_tableinfo', 'table_name', 'table_describe', 'field_name', 'field_describe')

    def __repr__(self):
        return f'<tableName: {self.table_name}>'


#  业务系统信息表
class BusinSysInfo(db.Model):
    __tablename__ = "businsysinfo"
    id = db.Column(db.Integer, primary_key=True)
    sys_no = db.Column(db.String(5))
    sys_name = db.Column(db.String(40))
    manager = db.Column(db.String(100), default='')


#  接口文件信息表
class InterfaceFile(db.Model):
    __tablename__ = "interfacefile"
    id = db.Column(db.Integer, primary_key=True)
    sys_no = db.Column(db.String(5), index=True)
    file_name = db.Column(db.String(100))
    file_path = db.Column(db.String(100), unique=True)
    upload_time = db.Column(db.DateTime, index=True, default=datetime.now)
    version = db.Column(db.String(100), unique=True, default='')


#  服务器硬件信息表
class HardwareInfo(db.Model):
    __tablename__ = "hardwareinfo"
    id = db.Column(db.Integer, primary_key=True)
    env_type = db.Column(db.String(2), default='')  # 设备类型 0-服务器 1-虚拟机
    brand = db.Column(db.String(40), default='')
    model = db.Column(db.String(40), default='')
    hardware_height = db.Column(db.String(40), default='')
    os_version = db.Column(db.String(40), default='')
    serial_no = db.Column(db.String(40), default='')
    system_name = db.Column(db.String(40), default='')
    system_describe = db.Column(db.String(400), default='')
    contact_name = db.Column(db.String(100), default='')
    hardware_status = db.Column(db.String(2), default='')  # 设备状态 0-已入库上架 1-已入库闲置 2-已上架使用 3-已上架闲置
    hardware_location = db.Column(db.String(40), default='')
    IP = db.Column(db.String(40), default='')
    if_storage = db.Column(db.String(40), default='')
    use_status = db.Column(db.String(40), default='')

    def __repr__(self):
        return f'<hardwareInfo : {self.brand}/{self.model}/{self.serial_no}/{self.contact_name}>'


#  系统环境信息表
class SystemInfo(db.Model):
    __tablename__ = "systeminfo"
    id = db.Column(db.Integer, primary_key=True)
    sys_no = db.Column(db.String(5), default='')
    sys_name = db.Column(db.String(40), default='')
    env_type = db.Column(db.String(2), default='')  # 环境类型 0-测试 1-生产
    env_name = db.Column(db.String(40), default='')  # 环境别名
    db_ip = db.Column(db.String(200), default='')
    db_info = db.Column(db.String(400), default='')
    middleware_ip = db.Column(db.String(200), default='')
    middleware_info = db.Column(db.String(400), default='')
    win_ip = db.Column(db.String(200), default='')
    win_info = db.Column(db.String(400), default='')
    tns_info = db.Column(db.Text, default='')
    client_info = db.Column(db.String(400), default='')
    contact_name = db.Column(db.String(100), default='')
    other_describe = db.Column(db.String(200), default='')

    def __repr__(self):
        return f'<systemInfo : {self.sys_name}/{self.env_name}/{self.env_type}/{self.contact_name}>'
