import datetime

from app.home import home
from app import db
from app.home.forms import RegisterForm, LoginForm, ModifyForm, IfFieldSearchForm, DfFieldSearchForm
from app.models import User, BusinSysInfo, InterfaceFile, AnnounceInfo, InterfaceFuncInfo, UF20TableInfo
from flask import render_template, url_for, redirect, flash, session, request, make_response, g
from werkzeug.security import generate_password_hash
from functools import wraps
import random
import string
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from sqlalchemy import or_


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


# 登录装饰器
def userLogin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('home.login'))
        return f(*args, **kwargs)

    return decorated_function


@home.route('/')
def index():
    announce_info = AnnounceInfo.query.filter(or_(AnnounceInfo.to_who == "2", AnnounceInfo.to_who == "3")).order_by(
        AnnounceInfo.upload_time.desc()).limit(3).all()
    return render_template('home/index.html', announce_info=announce_info)


# @home.app_template_filter()


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
        if user.user_status == '1':
            flash('您的账户已被冻结，请联系系统管理员', 'err_login')
            return render_template('home/login.html', form=form)
        if user.user_status == '2':
            flash('您的账户已被注销，请联系系统管理员', 'err_login')
            return render_template('home/login.html', form=form)
        session['user_id'] = user.id
        session['department'] = user.department
        session['realname'] = user.realname
        #   更新最近登录时间
        user.last_login_time = datetime.datetime.now()
        db.session.commit()
        return redirect(url_for('home.index'))
    return render_template('home/login.html', form=form)


# 登出
@home.route('/logout/')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home.index'))


# 在线用户修改密码
@home.route('/usermodify/', methods=['GET', 'POST'])
@userLogin
def userModify():
    form = ModifyForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(id=session.get('user_id')).first()
        if not user:
            flash('您已经登出，请重新登录', 'err_modify')
            return redirect(url_for('home.login'))
        user.password = generate_password_hash(data['newpassword'])
        db.session.commit()
        flash('密码修改完成！', 'info_modify')
        return redirect(url_for('home.userModify'))
    return render_template('home/modify_password.html', form=form)


@home.route('/uf20')
@userLogin
def uf20():
    return render_template('home/uf20.html')


#   if=interface，mng=manage，接口上传后的管理界面
@home.route('/uf20iffetch', methods=['GET', 'POST'])
@userLogin
def uf20IfFetch():
    g.bs = db.session.query().filter(BusinSysInfo.sys_no == InterfaceFile.sys_no).with_entities(BusinSysInfo.sys_no,
                                                                                                BusinSysInfo.sys_name,
                                                                                                BusinSysInfo.manager).distinct().all()
    g.interface = InterfaceFile.query.order_by(InterfaceFile.upload_time.desc()).all()
    return render_template('home/uf20_if_fetch.html')


# if=interface,接口信息搜索
@home.route('/uf20ifsearch', methods=['GET', 'POST'])
@userLogin
def uf20IfSearch():
    g.bs = BusinSysInfo.query.all()
    form = IfFieldSearchForm()
    if form.validate_on_submit():
        data = form.data
        sys_no = BusinSysInfo.query.filter(
            or_(BusinSysInfo.sys_name.like(f"%UF2%"), BusinSysInfo.sys_name.like(f"%uf2%"),
                BusinSysInfo.sys_name.like(f"%经纪业务运营平台V2%"))).first().sys_no
        key_word = data['keyword'].strip(' ')
        select_type = data['select_type']
        g.sys_name = BusinSysInfo.query.filter_by(sys_no=sys_no).first()
        if select_type == 1:
            g.query_result = InterfaceFuncInfo.query.filter(
                or_(InterfaceFuncInfo.func_no.like(f"%{key_word}%"),
                    InterfaceFuncInfo.func_no_old.like(f"%{key_word}%"))).all()
        else:
            g.query_result = InterfaceFuncInfo.query.filter(
                or_(InterfaceFuncInfo.func_name.like(f"%{key_word}%"),
                    InterfaceFuncInfo.func_describe.like(f"%{key_word}%"))).all()
        return render_template('home/uf20_if_search.html', form=form)
    return render_template('home/uf20_if_search.html', form=form)


# df=Database File，数据库信息检索
@home.route('/uf20dfsearch', methods=['GET', 'POST'])
@userLogin
def uf20DfSearch():
    g.bs = BusinSysInfo.query.all()
    form = DfFieldSearchForm()
    if form.validate_on_submit():
        data = form.data
        sys_no = BusinSysInfo.query.filter(
            or_(BusinSysInfo.sys_name.like(f"%UF2%"), BusinSysInfo.sys_name.like(f"%uf2%"),
                BusinSysInfo.sys_name.like(f"%经纪业务运营平台V2%"))).first().sys_no
        g.select_type = data['select_type']
        key_word = data['keyword'].strip(' ')
        g.sys_name = BusinSysInfo.query.filter_by(sys_no=sys_no).first()
        if g.select_type == 1:
            g.query_result = UF20TableInfo.query.filter(
                or_(UF20TableInfo.table_name.like(f"%{key_word}%"),
                    UF20TableInfo.table_describe.like(f"%{key_word}%"))).all()
        elif g.select_type == 2:
            g.query_result = UF20TableInfo.query.filter(
                or_(UF20TableInfo.field_name.like(f"%{key_word}%"),
                    UF20TableInfo.field_describe.like(f"%{key_word}%"))).all()
        return render_template('home/uf20_df_search.html', form=form)
    return render_template('home/uf20_df_search.html', form=form)


@home.route('/othersystem')
@userLogin
def otherSystem():
    return render_template('home/other_system.html')


# 公告预览
@home.route('/announcepreview/<sys_id>', methods=['GET', 'POST'])
@userLogin
def announcePreview(sys_id):
    announce_info = AnnounceInfo.query.get(sys_id)
    return render_template('home/announce_preview.html', data=announce_info)


#   jy=交易系统研发中心，内部人员往期公告查看
@home.route('/announcetuan')
@userLogin
def announceTuan():
    list_to_who = ['2', '3']  # 限制to_who为2-对外与3-对内对外
    g.ano = AnnounceInfo.query.filter(AnnounceInfo.to_who.in_(list_to_who)).order_by(
        AnnounceInfo.modify_time.desc()).offset(3).all()
    if len(g.ano) == 0:
        return render_template('home/announce_tuan.html', data='暂无更多数据')
    else:
        return render_template('home/announce_tuan.html')
