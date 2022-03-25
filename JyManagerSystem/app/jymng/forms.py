from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, TextField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed


class AnnounceForm(FlaskForm):
    '''
    维护接口文件信息，例如文件名称、保存路径，上传时间等
    '''
    chioce_list = [(x, y) for x in range(20)
                   for y in range(20) if x == y]
    select = SelectField(
        '选择对内对外',
        validators=[
            DataRequired('need'),
        ],
        render_kw={
            'class': 'form-control',
        },
        choices=chioce_list,
        coerce=int
    )

    announce_type = SelectField(
        '选择公告类型',
        validators=[
            DataRequired('need'),
        ],
        render_kw={
            'class': 'form-control',
        },
        choices=chioce_list,
        coerce=int
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

    announce_body = CKEditorField(
        '公告内容',
        description='发布内容',
        validators=[DataRequired()],
        render_kw={
            "placeholder": "发布内容",
            "size": 38,
            'class': 'ckeditor',
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
        '新建',
        render_kw={
            'class': "w-100 btn btn-lg btn-primary col-2 mt-3 mb-4",
        }
    )


class AnnounceEditForm(FlaskForm):
    '''
    维护接口文件信息，例如文件名称、保存路径，上传时间等
    '''
    chioce_list = [(x, y) for x in range(20)
                   for y in range(20) if x == y]
    select = SelectField(
        '选择对内对外',
        validators=[
            DataRequired('need'),
        ],
        render_kw={
            'class': 'form-control',
        },
        choices=chioce_list,
        coerce=int
    )

    announce_type = SelectField(
        '选择公告类型',
        validators=[
            DataRequired('need'),
        ],
        render_kw={
            'class': 'form-control',
        },
        choices=chioce_list,
        coerce=int
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

    announce_body = CKEditorField(
        '公告内容',
        description='发布内容',
        validators=[DataRequired()],
        render_kw={
            "placeholder": "发布内容",
            "size": 38,
            'class': 'ckeditor',
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
        '修改',
        render_kw={
            'class': "w-100 btn btn-lg btn-primary col-2 mt-3 mb-4",
        }
    )


class AnnounceTypeForm(FlaskForm):
    '''
    维护接口文件信息，例如文件名称、保存路径，上传时间等
    '''
    announce_type = StringField(
        label='公告类型 ： ',
        validators=[
            DataRequired('请输入公告类型')
        ],
        description='公告类型',
        render_kw={
            "placeholder": "公告类型",
            "size": 38,
            'class': 'custom-select',
        }
    )

    announce_type_name = StringField(
        label='公告描述 ： ',
        description='公告描述',
        render_kw={
            "placeholder": "公告类型描述（可为空）",
            "size": 38,
            'class': 'form-control',
        }
    )

    submit = SubmitField(
        '新建',
        render_kw={
            'class': "w-100 btn btn-lg btn-primary",
        }
    )
