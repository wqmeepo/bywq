from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed


class SiUploadForm(FlaskForm):
    '''
    维护接口文件信息，例如文件名称、保存路径，上传时间等
    '''
    chioce_list = [(1, 1), (2, 2), (3, 3), (4, 4)]
    select = SelectField(
        '选择对内对外',
        validators=[
            DataRequired('need')
        ],
        render_kw={
            'class': 'form-control',
        },
        choices=chioce_list,
        coerce=int,
    )

    announce_type = SelectField(
        '选择公告类型',
        validators=[
            DataRequired('need')
        ],
        render_kw={
            'class': 'form-control',
        },
        choices=chioce_list,
        coerce=int,
    )

    announce_head = StringField(
        label='公告名称 ： ',
        validators=[
            DataRequired('请输入公告名称')
        ],
        description='公告名称',
        render_kw={
            "placeholder": "公告名称",
            "size": 38,
            'class': 'custom-select',
        }
    )

    announce_body = TextAreaField(
        label='公告内容 ： ',
        validators=[
            DataRequired('请输入公告内容')
        ],
        description='公告内容',
        render_kw={
            "placeholder": "公告内容",
            "size": 38,
            'class': 'form-control',
        }
    )

    publisher = StringField(
        label='发布人 ： ',
        validators=[
            DataRequired('请输入发布人')
        ],
        description='发布人',
        render_kw={
            "placeholder": "发布人",
            "size": 38,
            'class': 'custom-select',
        }
    )

    submit = SubmitField(
        '上传',
        render_kw={
            'class': "w-100 btn btn-lg btn-primary",
        }
    )
