from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Regexp, EqualTo, ValidationError, Length
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
            'placeholder': '请输入用户名',
            'class': 'validata-username',
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
            'placeholder': '请输入您所在部门',
            'size': 38,
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
            'placeholder': '请输入真实姓名',
            'size': 38,
        }
    )
    password = PasswordField(
        label="密码 ：",
        validators=[
            DataRequired("密码不能为空！")
        ],
        description="首次密码",
        render_kw={
            "placeholder": "请输入密码",
            "size": 38,
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
            "placeholder": "请确认密码",
            "size": 38,
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            'class': 'btn btn-primary login',
        }
    )

    @staticmethod
    def validate_username(self, filed):
        '''
        if eamil is exist
        :param filed: email
        :return: None
        '''
        username = filed.data
        user = User.query.filter_by(username=username).count()
        if user == 1:
            raise ValidationError('用户名已存在')


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
            'placeholder': '请输入用户名',
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
            "placeholder": "请输入密码！",
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
            "placeholder": "请输入验证码",
            "size": 19,
            "maxlength": 4,
            'class': 'form-control',
        }
    )
    submit = SubmitField(
        '用户登录',
        render_kw={
            'class': 'btn btn-primary login',
        }
    )


class ModifyForm(FlaskForm):
    '''
    修改用户功能
    '''
    department = StringField(
        label='部门 ：',
        validators=[
            DataRequired('部门不能为空'),
            Length(min=3, max=40, message='请输入您所在部门')
        ],
        description='部门名称',
        render_kw={
            'type': 'text',
            'placeholder': '请输入您所在部门',
            'size': 38,
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
            'placeholder': '请输入真实姓名',
            'size': 38,
        }
    )
    oldpassword = PasswordField(
        label="原始密码 ：",
        validators=[
            DataRequired("原始密码不能为空！")
        ],
        description="原始密码",
        render_kw={
            "placeholder": "请输入原始密码",
            "size": 38,
        }
    )
    newpassword = PasswordField(
        label="新密码 ：",
        validators=[
            DataRequired("新密码不能为空！")
        ],
        description="新密码",
        render_kw={
            "placeholder": "请输入新密码",
            "size": 38,
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
            "placeholder": "请确认新密码",
            "size": 38,
        }
    )
    submit = SubmitField(
        '修改',
        render_kw={
            'class': 'btn btn-primary login',
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
