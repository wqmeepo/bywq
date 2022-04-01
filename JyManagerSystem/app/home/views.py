from app.home import home
from app import db
from app.home.forms import RegisterForm, LoginForm, ModifyForm
from app.models import User, BusinSysInfo, InterfaceFile
from flask import render_template, url_for, redirect, flash, session, request, make_response, g
from werkzeug.security import generate_password_hash
from functools import wraps
import random
import string
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO


def rndColor():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def geneText():
    return ''.join(random.sample(string.ascii_letters + string.digits, 4))


def draw_line(draw, num, width, height):
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)


def getVerifyCode():
    code = geneText()
    width, height = 93, 56
    im = Image.new('RGB', (width, height), color='white')
    font = ImageFont.truetype('app/static/fonts/arial.ttf', 32)
    draw = ImageDraw.Draw(im)
    for item in range(4):
        draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)), code[item], rndColor(), font)
    return im, code


@home.route('/')
def index():
    return render_template('home/index.html')


@home.route('/code')
def getCode():
    image, code = getVerifyCode()
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端
    response = make_response(buf_str)
    response.headers['content-type'] = 'image/gif'
    #   验证码存在session内
    session['image'] = code
    return response


# 注册
@home.route('/register/', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home.index'))
    form = RegisterForm()  # 实例化注册表单
    if form.validate_on_submit():
        data = form.data
        realuser = User.query.filter_by(realname=data['realname'], department=data['department']).count()
        if realuser >= 1:
            flash('存在同一部门下同名员工，请注册时区分！', 'err_register')
            return render_template('home/register.html', form=form)
        user = User(
            username=data['username'],
            password=generate_password_hash(data['password']),
            realname=data['realname'],
            department=data['department'],
        )

        db.session.add(user)
        db.session.commit()
        flash('注册完成，请登录！', 'success_register')
        return redirect(url_for('home.login'))
    return render_template('home/register.html', form=form)


# 登录
@home.route('/login/', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home.index'))
    form = LoginForm()  # 实例化登录表单
    if form.validate_on_submit():
        data = form.data
        if session.get('image').lower() != form.verifyCode.data.lower():  # 检查验证码
            flash('验证码输入错误！', 'err_login')
            return render_template('home/login.html', form=form)
        user = User.query.filter_by(username=data['username']).first()  # 获取人员信息
        if not user:  # 校验人员
            flash('该用户不存在！', 'err_login')
            return render_template('home/login.html', form=form)
        if not user.check_password(data['password']):  # 校验密码
            flash('密码错误！', 'err_login')
            return render_template('home/login.html', form=form)
        session['user_id'] = user.id
        session['username'] = user.username
        session['department'] = user.department
        return redirect(url_for('home.index'))
    return render_template('home/login.html', form=form)


# 登出
@home.route('/logout/')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home.index'))


# 登录装饰器
def userLogin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('home.login'))
        return f(*args, **kwargs)

    return decorated_function


# 在线用户修改密码
@userLogin
@home.route('/usermodify/', methods=['GET', 'POST'])
def userModify():
    form = ModifyForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=session.get('username')).first()
        if not user:
            flash('已经注销', 'err_modify')
            return redirect(url_for('home.login'))
        user.password = generate_password_hash(data['newpassword'])
        db.session.commit()
        flash('修改完成！', 'info_modify')
        return redirect(url_for('home.userModify'))
    return render_template('home/modify_password.html', form=form)


@home.route('/uf20')
def uf20():
    return render_template('home/uf20.html')


@home.route('/o32')
def o32():
    return render_template('home/o32.html')


@home.route('/bop')
def bop():
    return render_template('home/bop.html')


@home.route('/ta')
def ta():
    return render_template('home/ta.html')


@home.route('/frqs')
def frqs():
    return render_template('home/frqs.html')


@home.route('/hspb')
def hspb():
    return render_template('home/hspb.html')


#   if=interface，接口上传后各个系统的查询界面
@home.route('/iffetch', methods=['GET', 'POST'])
@userLogin
def ifFetch():
    g.bs = BusinSysInfo.query.all()  # 传到前端
    g.interface = InterfaceFile.query.all()  # 传到前端
    return render_template('home/if_fetch.html')
