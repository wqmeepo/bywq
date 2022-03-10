from app.bs import bs
from app import db
from app.bs.forms import BusinSysInfoForm, InterfaceFileForm, DbFileForm
from app.models import TableInfo, BusinSysInfo, InterfaceFile, SystemInfo, HardwareInfo
from flask import render_template, url_for, redirect, flash, g, send_file
from datetime import datetime
import os
import xlrd


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
    print('1')
    if form.validate_on_submit():
        print('2')
        data = form.data
        f = form.file.data
        sys_select = BusinSysInfo.query.filter_by(sys_no=data['select']).first().sys_name
        print(sys_select)
        save_path = os.path.join(bs.root_path, sys_select, 'interfacefile', f.filename.split('.')[0],
                                 data['version'])
        save_path_file = os.path.join(save_path, f.filename)
        if InterfaceFile.query.filter_by(sys_no=data['select'], version=data['version'],
                                         file_path=save_path_file).count() >= 1:
            flash('不允许上传同版本的接口文件，请先删除后上传', 'ifupload_error')
            return render_template('bs/if_upload.html', form=form)
        if not os.path.exists(save_path):
            os.makedirs(save_path, mode=0o777)  # 文件夹权限
        try:
            f.save(save_path_file)
            interface_file = InterfaceFile(
                sys_no=data['select'],
                file_name=f.filename,
                file_path=save_path_file,
                version=data['version'],
            )
            db.session.add(interface_file)
            db.session.commit()
        except:
            flash('接口文件上传失败', 'ifupload_error')
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


def dfDelete(sys_no):
    try:
        file_db = TableInfo.query.filter(sys_no=sys_no)
        db.session.delete(file_db)
        db.session.commit()
    except:
        flash('删除失败，请联系田凌看看', 'dfdelete_failed')


@bs.route('/dfmng', methods=['GET', 'POST'])
def dfMng():
    g.bs = BusinSysInfo.query.all()
    g.df = TableInfo.query.all()
    return render_template('bs/df_mng.html')


@bs.route('/dfupload', methods=['GET', 'POST'])
def dfUpload():
    def uf20Parse(sys_no, save_path_file):
        df = xlrd.open_workbook(save_path_file)
        total_list = []
        num = 0
        for sheet in df.sheets():
            column_list = []
            for i in range(sheet.nrows):
                cursor = 1
                sheet.row_values(i)
                if '表名' in sheet.row_values(i):
                    column_list.append('MEEPOK')
                    column_list.append(sheet.name)
                    column_list.append(sheet.row_values(i)[2])
                    column_list.append(sheet.row_values(i)[6])
                elif '中文名' in sheet.row_values(i):
                    column_list.append(sheet.row_values(i)[2])
                elif '字段' in sheet.row_values(i):
                    while '索引字段' not in sheet.row_values(i + cursor):
                        if '索引字段' in sheet.row_values(i + cursor):
                            break
                        column_list.append(sheet.row_values(i + cursor)[2])
                        column_list.append(sheet.row_values(i + cursor)[5])
                        cursor += 1
            total_list.append(column_list)
            num += 1
        for list_sheet in total_list:
            i = 0
            while i < len(list_sheet):
                if list_sheet[i] == 'MEEPOK':
                    count = 1
                    while list_sheet[i + count] != 'MEEPOK':
                        count += 1
                        if i + count == len(list_sheet) or list_sheet[i + count] == 'MEEPOK':
                            break
                    j = i + 5
                    k = i + 5

                    while k <= i + count:
                        if k + 1 > i + count:
                            break
                        table_delete = TableInfo.query.filter_by(sys_no=sys_no, table_name=list_sheet[i + 2]).all()
                        for each in table_delete:
                            db.session.delete(each)
                        k += 2
                    db.session.commit()

                    while j <= i + count:
                        if j + 1 > i + count:
                            break
                        table_info = TableInfo(
                            sys_no=sys_no,
                            file_path=save_path_file,
                            sheet_name=list_sheet[i + 1],
                            table_name=list_sheet[i + 2],
                            db_name=list_sheet[i + 3],
                            table_describe=list_sheet[i + 4],
                            field_name=list_sheet[j],
                            field_describe=list_sheet[j + 1],
                        )
                        db.session.add(table_info)
                        j += 2
                    db.session.commit()
                    i += count

    g.bs = BusinSysInfo.query.all()
    form = DbFileForm()
    if form.validate_on_submit():
        data = form.data
        sys_no = data['select']
        f = form.file.data
        sys_select = BusinSysInfo.query.filter_by(sys_no=sys_no).first().sys_name
        save_path = os.path.join(bs.root_path, sys_select, 'databasefile')
        save_path_file = os.path.join(save_path, f.filename)
        if not os.path.exists(save_path):
            os.makedirs(save_path, mode=0o777)  # 文件夹权限
        try:
            if os.path.exists(save_path_file):
                os.remove(save_path_file)
            f.save(save_path_file)
            flash('文件上传完成，开始解析数据库文件', 'dfupload_success')
        except:
            flash('接口文件上传失败,请重新上传', 'dfupload_error')
            return render_template('bs/df_upload.html', form=form)

        if sys_select == 'UF20':
            # dfDelete(sys_no)
            uf20Parse(sys_no, save_path_file)
        else:
            flash('当前只支持UF20数据库解析', 'dfupload_error')
            return render_template('bs/df_upload.html', form=form)
        # except:
        #     flash('数据库新增失败，请重试', 'dfupload_error')
        #     return render_template('bs/df_upload.html', form=form)
        flash('接口文件解析完成', 'dfupload_success')
        return redirect(url_for('bs.dfMng'))
    return render_template('bs/df_upload.html', form=form)
