from app.bs import bs
from app import db
from app.bs.forms import BusinSysInfoForm
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


@bs.route('/bsmap', methods=['GET', 'POST'])
def bsmap():
    form = BusinSysInfoForm()
    bs_query_data = BusinSysInfo.query.all()
    if form.validate_on_submit():
        data = form.data
        bsdata = BusinSysInfo(
            sys_no=data['sysno'],
            sys_name=data['sysname'],
            manager=data['manager'],
        )
        db.session.add(bsdata)
        db.session.commit()
    return render_template('bs/bsmap.html', form=form, bs_query_data=bs_query_data)
