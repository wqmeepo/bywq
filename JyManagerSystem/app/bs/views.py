from app.bs import bs
from app import db
from app.bs.forms import BusinSysInfoForm, InterfaceFileForm
from app.models import TableInfo, BusinSysInfo, InterfaceFile, SystemInfo, HardwareInfo
from flask import render_template, url_for, redirect, flash, session, request, make_response, g
from werkzeug.utils import secure_filename
from functools import wraps


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
    bs_q_data = BusinSysInfo.query.all()
    choices = []
    for i in bs_q_data:
        choices.append((i.sys_no, i.sys_name))
    g.choices = choices
    form = InterfaceFileForm()
    if form.validate_on_submit():
        data = form.data
        print(data['sysno'])
    return render_template('bs/ifupload.html', form=form)