import datetime
from app.jymng import jymng
from app.models import AnnounceInfo, AnnounceType
from app.jymng.forms import AnnounceForm, AnnounceTypeForm, AnnounceEditForm
from flask import g, render_template, url_for, redirect, flash, session, request, send_from_directory
from app import db
from flask_ckeditor import upload_fail, upload_success
import os
from functools import wraps


# 登录验证装饰器
def jyUserLogin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('home.login'))
        if session.get('department') != '交易系统研发中心':
            return '您无此权限,请联系交易系统研发中心同事'
        return f(*args, **kwargs)

    return decorated_function


#   jy=交易系统研发中心，该view管理研发中心的公告、知识分享、监管信息等信息
@jymng.route('/announcemng')
@jyUserLogin
def announceMng():
    g.ano = AnnounceInfo.query.order_by(AnnounceInfo.upload_time.desc()).all()
    return render_template('jymng/announce_mng.html')


#   jy=交易系统研发中心，新建公告
@jymng.route('/announceset', methods=['GET', 'POST'])
@jyUserLogin
def announceSet():
    g.ano_type = AnnounceType.query.all()
    form = AnnounceForm()
    if form.validate_on_submit():
        data = form.data
        announce_type = AnnounceType.query.get(data['announce_type']).announce_type
        announce_info = AnnounceInfo(
            announce_type=announce_type,
            announce_head=data['announce_head'],
            announce_body=data['announce_body'],
            publisher=session['username'],
            to_who=data['select'],
        )
        db.session.add(announce_info)
        db.session.commit()
        flash('公告新建成功', 'announceSet_success')
        return redirect(url_for('jymng.announceMng'))
    return render_template('jymng/announce_new.html', form=form)


#   jy=交易系统研发中心，新建公告类别
@jymng.route('/announcetypeset', methods=['GET', 'POST'])
@jyUserLogin
def announceTypeSet():
    form = AnnounceTypeForm()
    if form.validate_on_submit():
        data = form.data
        if data['announce_type_name'] is None:
            announce_type_info = AnnounceType(
                announce_type=data['announce_type'],
                announce_type_name=data[' '],
            )
        else:
            announce_type_info = AnnounceType(
                announce_type=data['announce_type'],
                announce_type_name=data['announce_type_name'],
            )
        db.session.add(announce_type_info)
        db.session.commit()
        flash('公告类型新建成功', 'announceTypeSet_success')
        return render_template('jymng/announce_type_set.html', form=form)
    return render_template('jymng/announce_type_set.html', form=form)


@jymng.route('/files/<path:filename>')
@jyUserLogin
def uploaded_files(filename):
    from manage import app
    path = os.path.join(app.root_path, 'storages', 'ckeditor_uploads')
    return send_from_directory(path, filename)


@jymng.route('/upload', methods=['POST'])
@jyUserLogin
def upload():
    from manage import app
    f = request.files.get('upload')  # 获取上传图片文件对象
    # Add more validations here
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:  # 验证文件类型示例
        return upload_fail(message='Image only!')  # 返回upload_fail调用
    save_path = os.path.join(app.root_path, 'storages', 'ckeditor_uploads')
    if not os.path.exists(save_path):
        os.makedirs(save_path, mode=0o777)  # 文件夹权限
    f.save(os.path.join(save_path, f.filename))
    url = url_for('jymng.uploaded_files', filename=f.filename)
    return upload_success(url=url)  # 返回upload_success调用


#   删除公告数据库信息
@jymng.route('/announcedelete/<sys_id>')
@jyUserLogin
def announceDelete(sys_id):
    try:
        #   删除数据库信息
        file_db = AnnounceInfo.query.get(sys_id)
        db.session.delete(file_db)
        db.session.commit()
        flash('删除成功', 'anodelete_success')
    except:
        flash('删除失败，请联系田凌看看', 'anodelete_failed')
    return redirect(url_for('jymng.announceMng'))


#   jy=交易系统研发中心，编辑公告类别
@jymng.route('/announceedit/<sys_id>', methods=['GET', 'POST'])
@jyUserLogin
def announceEdit(sys_id):
    g.ano_type = AnnounceType.query.all()
    ano_info = AnnounceInfo.query.get(sys_id)
    form = AnnounceEditForm()
    form.announce_head.data = ano_info.announce_head
    form.announce_body.data = ano_info.announce_body
    if form.validate_on_submit():
        announce_type = AnnounceType.query.get(request.form['announce_type']).announce_type
        ano_info.announce_head = request.form['announce_head']
        ano_info.announce_body = request.form['announce_body']
        ano_info.to_who = request.form['select']
        ano_info.announce_type = announce_type
        db.session.commit()
        flash('公告修改成功', 'announceSet_success')
        return redirect(url_for('jymng.announceMng'))
    return render_template('jymng/announce_edit.html', form=form)


#   jy=交易系统研发中心，置顶功能
@jymng.route('/announceclicktotop/<sys_id>', methods=['GET', 'POST'])
@jyUserLogin
def announceClickToTop(sys_id):
    time_now = datetime.datetime.now()
    AnnounceInfo.query.get(sys_id).upload_time = time_now
    db.session.commit()
    return redirect(url_for('jymng.announceMng'))


#   jy=交易系统研发中心，公告预览
@jymng.route('/announcepreview/<sys_id>', methods=['GET', 'POST'])
@jyUserLogin
def announcePreview(sys_id):
    announce_info = AnnounceInfo.query.get(sys_id).announce_body
    return announce_info
