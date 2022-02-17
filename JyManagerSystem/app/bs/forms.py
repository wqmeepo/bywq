from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired, Regexp, EqualTo, ValidationError, Length
from app.models import TableInfo, BusinSysInfo, InterfaceFile, SystemInfo, HardwareInfo
from flask_wtf.file import FileField, FileRequired, FileAllowed


class BusinSysInfoForm(FlaskForm):
    '''
    维护业务系统信息，例如0-UF20-负责人
    '''
    sysno = StringField(
        label='系统编号 ： ',
        validators=[
            DataRequired('请维护系统编号')
        ],
        description='系统编号',
        render_kw={
            "placeholder": "请输入系统编号",
            "size": 38,
            'class': 'form-control',
        }
    )
    sysname = StringField(
        label='系统名称 ： ',
        validators=[
            DataRequired('请维护系统名称')
        ],
        description='系统名称',
        render_kw={
            "placeholder": "请输入系统名称",
            "size": 38,
            'class': 'form-control',
        }
    )
    manager = StringField(
        label='系统管理员 ： ',
        validators=[
            DataRequired('请维护系统管理员')
        ],
        description='系统管理员',
        render_kw={
            "placeholder": "请输入系统管理员",
            "size": 38,
            'class': 'form-control',
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': "w-100 btn btn-lg btn-primary",
        }
    )

    @staticmethod
    def validate_sysno(self, field):
        sysno = field.data
        sysno_query = BusinSysInfo.query.filter_by(sys_no=sysno).count()
        if sysno_query >= 1:
            raise ValidationError('该编号已经被使用')

    @staticmethod
    def validate_sysname(self, field):
        sysname = field.data
        sysname_query = BusinSysInfo.query.filter_by(sys_name=sysname).count()
        if sysname_query >= 1:
            raise ValidationError('该系统已经存在')


class InterfaceFileForm(FlaskForm):
    '''
    维护接口文件信息，例如文件名称、保存路径，上传时间等
    '''
    select = SelectField(
        '选择',
        validators=[
            DataRequired('need')
        ],
        render_kw={
            'class': 'form-control',
        },
        choices=[(1, 'x'), (2, 'y')],
        default=2,
        coerce=int
    )

    file = FileField(
        '上传文件',
        validators=[
            FileRequired('文件不能为空'),
            FileAllowed(['xls', 'xlsx', 'pdf', 'doc', 'docx'])
        ],
        render_kw={
            'class': 'form-control',
            'accept': '.xls, .xlsx, .pdf, .doc, .docx',
        }
    )
    version = StringField(
        label='接口版本 ： ',
        validators=[
            DataRequired('请输入接口版本')
        ],
        description='接口版本',
        render_kw={
            "placeholder": "请输入接口版本",
            "size": 38,
            'class': 'form-control',
        }
    )

    submit = SubmitField(
        '上传',
        render_kw={
            'class': "w-100 btn btn-lg btn-primary",
        }
    )

    @staticmethod
    def validate_version(self, field):
        version = field.data
        version_query = InterfaceFile.query.filter_by(version=version).count()
        if version_query >= 1:
            raise ValidationError('不允许上传同版本的接口文件，请先删除后上传')
