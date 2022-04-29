from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from app.models import User


class RegisterForm(FlaskForm):
    '''
    注册功能
    '''
    username = StringField(
        label='用户名 ：',
        validators=[
            DataRequired('用户名不能为空'),
            Length(min=3, max=40, message='用户名长度在3到40之间')
        ],
        description='用户名',
        render_kw={
            'type': 'text',
            'placeholder': '用户名',
            'class': 'form-control',
            'size': 38,
        }
    )
    department = StringField(
        label='部门 ：',
        validators=[
            DataRequired('部门不能为空'),
            Length(min=3, max=40, message='请输入您所在部门')
        ],
        description='部门名称',
        render_kw={
            'type': 'text',
            'placeholder': '所在部门',
            'size': 38,
            'class': 'form-control',
        }
    )
    realname = StringField(
        label='姓名 ：',
        validators=[
            DataRequired('请输入真实姓名'),
            Length(min=1, max=40, message='长度校验失败')
        ],
        description='真实姓名',
        render_kw={
            'type': 'text',
            'placeholder': '真实姓名',
            'size': 38,
            'class': 'form-control',
        }
    )
    password = PasswordField(
        label="密码 ：",
        validators=[
            DataRequired("密码不能为空！")
        ],
        description="首次密码",
        render_kw={
            "placeholder": "密码",
            "size": 38,
            'class': 'form-control',
        }
    )
    repassword = PasswordField(
        label="确认密码 ：",
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('password', message='两次密码不一致！')
        ],
        description="确认密码",
        render_kw={
            "placeholder": "确认密码",
            "size": 38,
            'class': 'form-control',
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            'class': "w-100 btn btn-lg btn-primary",
        }
    )

    @staticmethod
    def validate_username(self, filed):
        '''
        if username is exist
        :param filed: username
        :return: None
        '''
        username = filed.data
        user = User.query.filter_by(username=username).count()
        if user >= 1:
            raise ValidationError('该用户名已存在，请设置其他用户名')


class LoginForm(FlaskForm):
    '''
    登录功能
    '''
    username = StringField(
        label='用户名 : ',
        validators=[
            DataRequired('用户名不能为空'),
            Length(min=3, max=40, message='用户名长度在3到40之间')
        ],
        description='username',
        render_kw={
            'type': 'text',
            'placeholder': '用户名',
            'class': 'form-control',
            'size': 38,
        }
    )
    password = PasswordField(
        label="密码 ：",
        validators=[
            DataRequired("密码不能为空！")
        ],
        description="password",
        render_kw={
            "placeholder": "密码！",
            "size": 38,
            'class': 'form-control',
        }
    )
    verifyCode = StringField(
        label="验证码 ：",
        validators=[
            DataRequired("验证码不能为空！")
        ],
        description="验证码",
        render_kw={
            "placeholder": "验证码",
            "size": 19,
            "maxlength": 4,
            'class': 'form-control',
        }
    )
    submit = SubmitField(
        '用户登录',
        render_kw={
            'class': "w-100 btn btn-lg btn-primary",
        }
    )


class ModifyForm(FlaskForm):
    '''
    修改用户功能
    '''
    oldpassword = PasswordField(
        label="原始密码 ：",
        validators=[
            DataRequired("原始密码不能为空！")
        ],
        description="原始密码",
        render_kw={
            "placeholder": "原始密码",
            "size": 38,
            'class': 'form-control',
        }
    )
    newpassword = PasswordField(
        label="新密码 ：",
        validators=[
            DataRequired("新密码不能为空！")
        ],
        description="新密码",
        render_kw={
            "placeholder": "新密码",
            "size": 38,
            'class': 'form-control',
        }
    )
    renewpassword = PasswordField(
        label="确认新密码 ：",
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('newpassword', message='两次密码不一致！')
        ],
        description="确认密码",
        render_kw={
            "placeholder": "确认新密码",
            "size": 38,
            'class': 'form-control',
        }
    )
    submit = SubmitField(
        '修改',
        render_kw={
            'class': "w-100 btn btn-lg btn-primary",
        }
    )

    @staticmethod
    def validate_oldpassword(self, field):
        from flask import session
        old_password = field.data
        user_id = session.get('user_id')
        user = User.query.get(int(user_id))
        if not user.check_password(old_password):
            raise ValidationError('原始密码错误！')


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


class DfFieldSearchForm(FlaskForm):
    '''
    数据库搜索
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
