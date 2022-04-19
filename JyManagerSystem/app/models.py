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
    user_status = db.Column(db.String(2), default='0')  # 0-正常 1-冻结 2-注销
    last_login_time = db.Column(db.DateTime, default=datetime.now)

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
class UF20TableInfo(db.Model):
    __tablename__ = "uf20tableinfo"
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100), index=True)
    table_describe = db.Column(db.String(200), index=True)
    sys_no = db.Column(db.String(5), default='')
    db_name = db.Column(db.String(40), default='')
    field_name = db.Column(db.String(100), index=True)
    field_describe = db.Column(db.String(200), index=True)
    sheet_name = db.Column(db.String(40), nullable=True, default='')
    file_path = db.Column(db.String(400), default='')
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
    sys_no = db.Column(db.String(10), index=True)
    file_name = db.Column(db.String(100), index=True)
    file_path = db.Column(db.String(400))
    upload_time = db.Column(db.DateTime, index=True, default=datetime.now)
    version = db.Column(db.String(100), default='')


#  接口文件字段信息表
class InterfaceFuncInfo(db.Model):
    __tablename__ = "interfacefuncinfo"
    id = db.Column(db.Integer, primary_key=True)
    sys_no = db.Column(db.String(10))
    file_path = db.Column(db.String(400))
    func_no = db.Column(db.String(12), index=True)
    func_name = db.Column(db.String(50), index=True)
    func_describe = db.Column(db.String(400))
    func_no_old = db.Column(db.String(24))
    func_range = db.Column(db.String(50))
    product_range = db.Column(db.String(100))
    func_status = db.Column(db.String(12))
    func_return = db.Column(db.String(5))
    hyperlink_position = db.Column(db.String(12))


#  服务器硬件信息表
class ServiceInfo(db.Model):
    __tablename__ = "serviceinfo"
    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(2))
    file_name = db.Column(db.String(100))
    file_path = db.Column(db.String(400))
    upload_time = db.Column(db.DateTime, index=True, default=datetime.now)
    version = db.Column(db.String(100), default='')

    def __repr__(self):
        return f'<ServiceInfo : {self.file_name}/{self.upload_time}/{self.version}>'


#  公告信息表
class AnnounceInfo(db.Model):
    __tablename__ = "announceinfo"
    id = db.Column(db.Integer, primary_key=True)
    announce_type = db.Column(db.String(200))
    announce_head = db.Column(db.String(200), unique=True)
    announce_body = db.Column(db.Text)
    publisher = db.Column(db.String(40))
    upload_time = db.Column(db.DateTime, index=True, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now)
    to_who = db.Column(db.String(2), default='1')


#  公告类别表
class AnnounceType(db.Model):
    __tablename__ = "announcetype"
    id = db.Column(db.Integer, primary_key=True)
    announce_type = db.Column(db.String(40), unique=True)
    announce_type_name = db.Column(db.String(400), nullable=True, default='')


#  数据字典表
class Dictionary(db.Model):
    __tablename__ = "dictionary"
    id = db.Column(db.Integer, primary_key=True)
    sys_no = db.Column(db.String(10))
    branch_no = db.Column(db.String(10), default='')
    field_name = db.Column(db.String(100), index=True)
    field_describe = db.Column(db.String(200))
    dic_no = db.Column(db.String(10), index=True)
    dic_sub_id = db.Column(db.String(10))
    dic_sub_name = db.Column(db.String(100))
