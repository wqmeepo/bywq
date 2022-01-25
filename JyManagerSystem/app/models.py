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
    db.UniqueConstraint('real_name', 'department', name='uniq_realname_department')

    def __repr__(self):
        return f'<user : {self.department} - {self.real_name}>'

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
    tablename = db.Column(db.String(20), index=True)
    tabledescribe = db.Column(db.String(100), index=True)
    sysno = db.Column(db.String(5), default='')
    sysname = db.Column(db.String(40), default='')
    dbname = db.Column(db.String(40), default='')
    fieldname = db.Column(db.String(20), index=True)
    fielddescribe = db.Column(db.String(100), index=True)
    fielddescibedetail = db.Column(db.Text, nullable=True, default='')
    db.Index('idx_search_tableinfo', 'table_name', 'table_describe', 'field_name', 'field_describe')

    def __repr__(self):
        return f'<tableName: {self.table_name}>'


#  接口信息表
class InterfaceInfo(db.Model):
    __tablename__ = "interfaceinfo"
    id = db.Column(db.Integer, primary_key=True)
    interfaceid = db.Column(db.String(20), index=True)
    interfaceold = db.Column(db.String(20), default='')
    interfacename = db.Column(db.String(100), index=True)
    interfacedescribe = db.Column(db.String(100), default='')
    interfaceversion = db.Column(db.String(20), default='')
    businessrange = db.Column(db.String(40), default='')
    productrange = db.Column(db.String(40), default='')
    funcstatus = db.Column(db.String(5), default='')
    ifreturn = db.Column(db.String(2), default='')  # 是否返回 0-否 1-是
    db.Index('idx_search_interfaceinfo', 'interface_id', 'interface_name')

    def __repr__(self):
        return f'<interfaceInfo : {self.interface_id} - {self.interface_name}>'


#  接口字段信息表
class InterfaceFieldInfo(db.Model):
    __tablename__ = "interfacefieldinfo"
    id = db.Column(db.Integer, primary_key=True)
    interfaceid = db.Column(db.String(20), index=True)
    updatetime = db.Column(db.String(8), default='')  # 更新时间 YYYYMMDD
    parameterin = db.Column(db.String(20), default='')
    parameterindescribe = db.Column(db.String(100), default='')
    necessaryin = db.Column(db.String(2), default='')  # 入参是否必须 0-非必须 1-必须
    parameterout = db.Column(db.String(20), default='')
    parameteroutdescribe = db.Column(db.String(100), default='')
    errorid = db.Column(db.String(20), default='')

    def __repr__(self):
        return f'<interfaceFieldInfo: {self.interface_id}>'


#  错误信息表
class ErrorInfo(db.Model):
    __tablename__ = "errorinfo"
    id = db.Column(db.Integer, primary_key=True)
    errorsystem = db.Column(db.String(40), default='')
    errorid = db.Column(db.String(20), default='')
    errordescribe = db.Column(db.String(100), default='')

    def __repr__(self):
        return f'<errorDescribe : {self.error_id} - {self.error_describe}>'


#  接口字段字典表
class InterfaceFieldDic(db.Model):
    __tablename__ = "interfacefielddic"
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(40), unique=True)
    fieldname = db.Column(db.String(40), default='')
    dicno = db.Column(db.String(20), default='')

    def __repr__(self):
        return f'<field : {self.field} - {self.field_name}>'


#  接口字典表
class InterfaceDic(db.Model):
    __tablename__ = "interfacedic"
    id = db.Column(db.Integer, primary_key=True)
    dicid = db.Column(db.String(20), default='')
    dicdetailname = db.Column(db.String(40), default='', index=True)
    dicno = db.Column(db.String(20), default='')
    dicname = db.Column(db.String(40), default='', index=True)
    db.Index('idx_search_interFaceDic', 'dic_no', 'dic_id')

    def __repr__(self):
        return f'<dic : {self.dic_no} - {self.dic_name}>'


#  服务器硬件信息表
class HardwareInfo(db.Model):
    __tablename__ = "hardwareinfo"
    id = db.Column(db.Integer, primary_key=True)
    envtype = db.Column(db.String(2), default='')  # 设备类型 0-服务器 1-虚拟机
    brand = db.Column(db.String(40), default='')
    model = db.Column(db.String(40), default='')
    hardwareheight = db.Column(db.String(40), default='')
    osversion = db.Column(db.String(40), default='')
    serialno = db.Column(db.String(40), default='')
    systemname = db.Column(db.String(40), default='')
    systemdescribe = db.Column(db.String(400), default='')
    contactname = db.Column(db.String(100), default='')
    hardwarestatus = db.Column(db.String(2), default='')  # 设备状态 0-已入库上架 1-已入库闲置 2-已上架使用 3-已上架闲置
    hardwarelocation = db.Column(db.String(40), default='')
    IP = db.Column(db.String(40), default='')
    ifstorage = db.Column(db.String(40), default='')
    usestatus = db.Column(db.String(40), default='')

    def __repr__(self):
        return f'<hardwareInfo : {self.brand}/{self.model}/{self.serial_no}/{self.contact_name}>'


#  系统环境信息表
class SystemInfo(db.Model):
    __tablename__ = "systeminfo"
    id = db.Column(db.Integer, primary_key=True)
    sysno = db.Column(db.String(5), default='')
    sysname = db.Column(db.String(40), default='')
    envtype = db.Column(db.String(2), default='')  # 环境类型 0-测试 1-生产
    envname = db.Column(db.String(40), default='')  # 环境别名
    dbip = db.Column(db.String(200), default='')
    dbinfo = db.Column(db.String(400), default='')
    middlewareip = db.Column(db.String(200), default='')
    middlewareinfo = db.Column(db.String(400), default='')
    winip = db.Column(db.String(200), default='')
    wininfo = db.Column(db.String(400), default='')
    tnsinfo = db.Column(db.Text, default='')
    clientinfo = db.Column(db.String(400), default='')
    contactname = db.Column(db.String(100), default='')
    otherdescribe = db.Column(db.String(200), default='')

    def __repr__(self):
        return f'<systemInfo : {self.sys_name}/{self.env_name}/{self.env_type}/{self.contact_name}>'
