from app.jymng import jymng
from app.models import AnnounceInfo, AnnounceType
from app.jymng.forms import AnnounceForm, AnnounceTypeForm
from flask import g, render_template, url_for, redirect, flash, session, request, send_from_directory
from app import db
from flask_ckeditor import upload_fail, upload_success
import os


#   jy=交易系统研发中心，该view管理研发中心的公告、知识分享、监管信息等信息
@jymng.route('/announcemng')
def announceMng():
    g.ano = AnnounceInfo.query.order_by(AnnounceInfo.upload_time.desc()).all()
    return render_template('jymng/announce_mng.html')


#   jy=交易系统研发中心，新建公告
@jymng.route('/announceset', methods=['GET', 'POST'])
def announceSet():
    g.ano_type = AnnounceType.query.all()
    form = AnnounceForm()
    if form.validate_on_submit():
        data = form.data
        print(data['announce_body'])
        print(request.form.get(1))
        announce_info = AnnounceInfo(
            announce_type=data['announce_type'],
            announce_head=data['announce_head'],
            announce_body=data['announce_body'],
            publisher=session['username'],
            to_who=data['select'],
        )
        db.session.add(announce_info)
        db.session.commit()
        flash('公告新建成功', 'announceSet_success')
        return redirect(url_for('jymng.announceMng'))
    return render_template('jymng/announce_set.html', form=form)


#   jy=交易系统研发中心，新建公告类别
@jymng.route('/announcetypeset', methods=['GET', 'POST'])
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
def uploaded_files(filename):
    from manage import app
    path = os.path.join(app.root_path, 'storages', 'ckeditor_uploads')
    return send_from_directory(path, filename)


@jymng.route('/upload', methods=['POST'])
def upload():
    from manage import app
    f = request.files.get('upload')  # 获取上传图片文件对象
    # Add more validations here
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:  # 验证文件类型示例
        return upload_fail(message='Image only!')  # 返回upload_fail调用
    f.save(os.path.join(app.root_path, 'storages', 'ckeditor_uploads', f.filename))
    url = url_for('jymng.uploaded_files', filename=f.filename)
    return upload_success(url=url)  # 返回upload_success调用