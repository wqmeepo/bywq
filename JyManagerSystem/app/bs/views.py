from app.bs import bs
from app import db
from app.bs.forms import BusinSysInfoForm, InterfaceFileForm
from app.models import TableInfo, BusinSysInfo, InterfaceFile, SystemInfo, HardwareInfo
from flask import render_template, url_for, redirect, flash, g, send_file
from datetime import datetime
import os


@bs.route('/')
def index():
    return render_template('bs/bs_set.html')


@bs.route('/uf20')
def uf20():
    return render_template('bs/uf20.html')


@bs.route('/o32')
def o32():
    return render_template('bs/o32.html')


@bs.route('/bop')
def bop():
    return render_template('bs/bop.html')


@bs.route('/ta')
def ta():
    return render_template('bs/ta.html')


@bs.route('/frqs')
def frqs():
    return render_template('bs/frqs.html')


@bs.route('/hspb')
def hspb():
    return render_template('bs/hspb.html')


@bs.route('/bsmap')
def bsMap():
    g.bs_query_data = BusinSysInfo.query.all()
    return render_template('bs/bs_map.html')


@bs.route('/bsmapset', methods=['GET', 'POST'])
def bsMapSet():
    form = BusinSysInfoForm()
    if form.validate_on_submit():
        data = form.data
        bsdata = BusinSysInfo(
            sys_no=data['sysno'],
            sys_name=data['sysname'],
            manager=data['manager'],
        )
        db.session.add(bsdata)
        db.session.commit()
        return redirect(url_for('bs.bsMap'))
    return render_template('bs/bs_map_set.html', form=form)


@bs.route('/ifmng', methods=['GET', 'POST'])
def ifMng():
    g.bs = BusinSysInfo.query.all()
    g.interface = InterfaceFile.query.all()
    return render_template('bs/if_mng.html')


@bs.route('/iffetch', methods=['GET', 'POST'])
def ifFetch():
    g.bs = BusinSysInfo.query.all()
    g.interface = InterfaceFile.query.all()
    return render_template('bs/if_fetch.html')


@bs.route('/ifupload', methods=['GET', 'POST'])
def ifUpload():
    g.bs = BusinSysInfo.query.all()
    form = InterfaceFileForm()
    if form.validate_on_submit():
        data = form.data
        f = form.file.data
        sys_select = BusinSysInfo.query.filter_by(sys_no=data['select']).first().sys_name
        save_path = os.path.join(bs.root_path, sys_select, str(datetime.now().year), f.filename, data['version'])
        save_path_file = os.path.join(save_path, f.filename)
        if InterfaceFile.query.filter_by(sys_no=data['select'], version=data['version'],
                                         file_path=save_path_file).count() >= 1:
            flash('不允许上传同版本的接口文件，请先删除后上传', 'ifupload_error')
            return render_template('bs/if_upload.html', form=form)
        if not os.path.exists(save_path):
            os.makedirs(save_path, mode=0o777)  # 文件夹权限
        f.save(save_path_file)
        interface_file = InterfaceFile(
            sys_no=data['select'],
            file_name=f.filename,
            file_path=save_path_file,
            version=data['version'],
        )
        db.session.add(interface_file)
        db.session.commit()
        flash('接口文件上传完成', 'ifupload_success')
        return redirect(url_for('bs.ifMng'))
    return render_template('bs/if_upload.html', form=form)


@bs.route('/ifdownload/<file_path>')
def ifDownload(file_path):
    file_name = file_path.rsplit('\\')[-1]
    return send_file(file_path, as_attachment=True, attachment_filename=file_name)


@bs.route('/ifdelete/<id>')
def ifDelete(id):
    file_path = InterfaceFile.query.get(id).file_path
    try:
        file_db = InterfaceFile.query.get(id)
        db.session.delete(file_db)
        db.session.commit()
        os.remove(file_path)
    except:
        flash('删除失败，请联系田凌看看', 'ifdelete_failed')
    return redirect(url_for('bs.ifMng'))