from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import BusinSysInfo
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
            "placeholder": "系统编号",
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
            "placeholder": "系统名称",
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
            "placeholder": "系统管理员",
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
    chioce_list = [(x, y) for x in range(20)
                   for y in range(20) if x == y]
    select = SelectField(
        '选择',
        validators=[
            DataRequired('need')
        ],
        render_kw={
            'class': 'form-control',
        },
        choices=chioce_list,
        coerce=int,
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


class DbFileForm(FlaskForm):
    '''
    维护接口文件信息，例如文件名称、保存路径，上传时间等
    '''
    chioce_list = [(x, y) for x in range(20)
                   for y in range(20) if x == y]
    select = SelectField(
        '选择',
        validators=[
            DataRequired('need')
        ],
        render_kw={
            'class': 'form-control',
        },
        choices=chioce_list,
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

    submit = SubmitField(
        '上传',
        render_kw={
            'class': "w-100 btn btn-lg btn-primary",
            'id': 'submit'
        }
    )


class DfFieldSearchForm(FlaskForm):
    '''
    维护接口文件信息，例如文件名称、保存路径，上传时间等
    '''
    chioce_list = [(x, y) for x in range(20)
                   for y in range(20) if x == y]
    select_sys = SelectField(
        '选择',
        validators=[
            DataRequired('need')
        ],
        render_kw={
            'class': 'custom-select',
        },
        choices=chioce_list,
        coerce=int
    )

    select_type = SelectField(
        '选择',
        validators=[
            DataRequired('need')
        ],
        render_kw={
            'class': 'custom-select',
            'aria-label': ".form-select-lg",
        },
        choices=[(1, '搜表/表名'), (2, '搜字段/字段名')],
        coerce=int
    )

    keyword = StringField(
        label='搜索内容 ： ',
        validators=[
            DataRequired('请输入要搜索的内容')
        ],
        description='搜索内容',
        render_kw={
            "placeholder": "输入搜索内容",
            "size": 38,
            'class': 'custom-select',
        }
    )

    submit = SubmitField(
        '搜索',
        render_kw={
            'class': "w-100 btn  btn-primary col-2 height-control",
        }
    )


class SiUploadForm(FlaskForm):
    '''
    维护接口文件信息，例如文件名称、保存路径，上传时间等
    '''
    chioce_list = [(1, 1), (2, 2)]
    select = SelectField(
        '选择',
        validators=[
            DataRequired('need')
        ],
        render_kw={
            'class': 'form-control',
        },
        choices=chioce_list,
        coerce=int,
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


class IfFieldSearchForm(FlaskForm):
    '''
    接口文件搜索
    '''
    chioce_list = [(x, y) for x in range(20)
                   for y in range(20) if x == y]
    select_sys = SelectField(
        '选择',
        validators=[
            DataRequired('need')
        ],
        render_kw={
            'class': 'custom-select',
        },
        choices=chioce_list,
        coerce=int
    )

    select_type = SelectField(
        '选择',
        validators=[
            DataRequired('need')
        ],
        render_kw={
            'class': 'custom-select',
            'aria-label': ".form-select-lg",
        },
        choices=[(1, '按功能号'), (2, '按功能号名')],
        coerce=int
    )

    keyword = StringField(
        label='搜索内容 ： ',
        validators=[
            DataRequired('请输入要搜索的内容')
        ],
        description='搜索内容',
        render_kw={
            "placeholder": "输入搜索内容",
            "size": 38,
            'class': 'custom-select',
        }
    )

    submit = SubmitField(
        '搜索',
        render_kw={
            'class': "w-100 btn  btn-primary col-2 height-control",
        }
    )
