from app.bs import bs
from app import db
from app.bs.forms import BusinSysInfoForm, InterfaceFileForm
from app.models import TableInfo, BusinSysInfo, InterfaceFile, SystemInfo, HardwareInfo
from flask import render_template, url_for, redirect, flash, session, request, make_response, g
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime
import os, stat


@bs.route('/')
def index():
    return render_template('bs/bsset.html')


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
def bsmap():
    g.bs_query_data = BusinSysInfo.query.all()
    return render_template('bs/bsmap.html')


@bs.route('/bsmapset', methods=['GET', 'POST'])
def bsmapset():
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
        return redirect(url_for('bs.bsmap'))
    return render_template('bs/bsmapset.html', form=form)


@bs.route('/ifmng', methods=['GET', 'POST'])
def ifmng():
    g.bs = BusinSysInfo.query.all()
    g.interface = InterfaceFile.query.all()
    return render_template('bs/ifmng.html')


@bs.route('/ifupload', methods=['GET', 'POST'])
def ifupload():
    g.bs = BusinSysInfo.query.all()
    form = InterfaceFileForm()
    if form.validate_on_submit():
        data = form.data
        f = form.file.data
        sys_select = BusinSysInfo.query.filter_by(sys_no=data['select']).first().sys_name
        save_path = os.path.join(bs.root_path, sys_select, str(datetime.now().year))
        print(save_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            os.chmod(save_path, stat.S_IWRITE)
        f.save(save_path, f.filename)
        f.close()
        interface_file = InterfaceFile(
            sys_no=data['select'],
            file_name=f.filename,
            file_path=save_path,
            version=data['version'],
        )
        db.session.add(interface_file)
        db.session.commit()
        print('db done')
        flash('接口文件上传完成', 'success_upload_interface')
        return redirect(url_for('bs.ifmng'))
    return render_template('bs/ifupload.html', form=form)
