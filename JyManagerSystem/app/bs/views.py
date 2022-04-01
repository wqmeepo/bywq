from app.bs import bs
from app import db
from manage import app
from app.bs.forms import BusinSysInfoForm, InterfaceFileForm, DbFileForm, DfFieldSearchForm, SiUploadForm
from app.models import TableInfo, BusinSysInfo, InterfaceFile, ServiceInfo, Dictionary
from flask import render_template, url_for, redirect, flash, g, send_file, request
from sqlalchemy import or_
import os
import xlrd
from app.functions.iterExcel import siHardExcelPreview, siSoftExcelPreview
from app.jymng.views import userLogin


#   bs=Business system，业务系统，该view管理所有业务系统相关页面
@bs.route('/')
@userLogin
def index():
    pagination = TableInfo.query.paginate(1, 10)
    item = pagination.items
    return render_template('bs/bs_index.html')


@bs.route('/bsmap')
@userLogin
def bsMap():
    g.bs_query_data = BusinSysInfo.query.all()
    return render_template('bs/bs_map.html')


#   系统对应映射关系设置界面
@bs.route('/bsmapset', methods=['GET', 'POST'])
@userLogin
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
        flash('系统关系新建完成', 'mapset_success')
        return redirect(url_for('bs.bsMap'))
    return render_template('bs/bs_map_set.html', form=form)


#   if=interface，mng=manage，接口上传后的管理界面
@bs.route('/ifmng', methods=['GET', 'POST'])
@userLogin
def ifMng():
    g.bs = db.session.query().filter(BusinSysInfo.sys_no == InterfaceFile.sys_no).with_entities(BusinSysInfo.sys_no,
                                                                                                BusinSysInfo.sys_name,
                                                                                                BusinSysInfo.manager).distinct().all()
    g.interface = InterfaceFile.query.order_by(InterfaceFile.upload_time.desc()).all()
    return render_template('bs/if_mng.html')


#   if=interface，接口文件上传界面
@bs.route('/ifupload', methods=['GET', 'POST'])
@userLogin
def ifUpload():
    g.bs = BusinSysInfo.query.all()  # 用于传到前端进行展示
    form = InterfaceFileForm()
    if form.validate_on_submit():
        data = form.data
        f = form.file.data  # 上传的文件
        #   获取映射系统名称
        sys_select = BusinSysInfo.query.filter_by(sys_no=data['select']).first().sys_name
        #   文件夹
        save_path = os.path.join(app.root_path, 'storages', 'InterfaceFile', sys_select, 'version-' + data['version'])
        #   文件绝对路径
        save_path_file = os.path.join(save_path, f.filename)
        #   检测数据库是否有同一个sys_no下相同版本的，同目录文件
        if InterfaceFile.query.filter_by(sys_no=data['select'], version=data['version'],
                                         file_path=save_path_file).count() >= 1:
            flash('不允许上传同版本的接口文件，请先删除后上传', 'ifupload_error')
            return render_template('bs/if_upload.html', form=form)
        #   保存文件到服务器，没有目录创建目录
        if not os.path.exists(save_path):
            os.makedirs(save_path, mode=0o777)  # 文件夹权限
        try:
            #   保存文件
            f.save(save_path_file)
            #   数据库写入
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


#   下载接口文件
@bs.route('/ifdownload/<file_path>')
@userLogin
def ifDownload(file_path):
    #   接口文件下载 send_file方法
    file_name = file_path.rsplit('\\')[-1]
    return send_file(file_path, as_attachment=True, attachment_filename=file_name)


#   删除接口文件与数据库信息
@bs.route('/ifdelete/<sys_id>')
@userLogin
def ifDelete(sys_id):
    file_path = InterfaceFile.query.get(sys_id).file_path
    try:
        #   删除数据库信息
        file_db = InterfaceFile.query.get(sys_id)
        db.session.delete(file_db)
        db.session.commit()
        #   删除服务器文件
        os.remove(file_path)
    except:
        flash('删除失败，请联系田凌看看', 'ifdelete_failed')
    return redirect(url_for('bs.ifMng'))


# df=Database File，数据库文件上传解析后管理页面
@bs.route('/dfmng', methods=['GET', 'POST'])
@userLogin
def dfMng():
    g.bs = BusinSysInfo.query.all()
    #   group_by一下TableInfo表，因为这个表是按字段导入
    g.df = TableInfo.query.with_entities(TableInfo.sys_no, TableInfo.file_path).group_by(TableInfo.sys_no,
                                                                                         TableInfo.file_path).all()
    return render_template('bs/df_mng.html')


# df=Database File，数据库信息检索
@bs.route('/dfsearch', methods=['GET', 'POST'])
@userLogin
def dfSearch():
    g.bs = BusinSysInfo.query.all()
    form = DfFieldSearchForm()
    if form.validate_on_submit():
        data = form.data
        sys_no = data['select_sys']
        g.select_type = data['select_type']
        key_word = data['keyword']
        g.sys_name = BusinSysInfo.query.filter_by(sys_no=sys_no).first()
        if g.select_type == 1:
            g.query_result_table = TableInfo.query.filter(
                or_(TableInfo.table_name.like(f"%{key_word}%"), TableInfo.table_describe.like(f"%{key_word}%"))).all()
        elif g.select_type == 2:
            g.query_result_field = TableInfo.query.filter(
                or_(TableInfo.field_name.like(f"%{key_word}%"), TableInfo.field_describe.like(f"%{key_word}%"))).all()
        return render_template('bs/df_search.html', form=form)
    return render_template('bs/df_search.html', form=form)


@bs.route('/querydictionary/<field_name>', methods=['GET', 'POST'])
@userLogin
def queryDictionary(field_name):
    print(field_name)
    query_dictionary_data = Dictionary.query.filter_by(field_name=field_name).all()
    if len(query_dictionary_data) == 0:
        return '<p>该字段没有数据字典信息</p>'
    else:
        return render_template('bs/df_modal.html', data=query_dictionary_data)


# df=Database File，数据库文件上传，解析的页面
@bs.route('/dfupload', methods=['GET', 'POST'])
@userLogin
def dfUpload():
    #   针对UF20数据库excel文件的解析方法，支持覆盖导入（先删除，后插入）
    def uf20Parse(sys_no, save_path_file):
        df = xlrd.open_workbook(save_path_file)
        total_list = []
        num = 0
        for sheet in df.sheets():
            column_list = []
            for i in range(sheet.nrows):
                cursor = 1
                sheet.row_values(i)
                if '表名' in sheet.row_values(i) and '中文名' in sheet.row_values(i + 1):
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
        save_path = os.path.join(app.root_path, 'storages', 'DatabaseFile', sys_select)
        save_path_file = os.path.join(save_path, f.filename)
        if not os.path.exists(save_path):
            os.makedirs(save_path, mode=0o777)  # 文件夹权限
        try:
            #   判断是否存在同名文件，如果存在则删除
            if os.path.exists(save_path_file):
                os.remove(save_path_file)
            #   保存文件
            f.save(save_path_file)
            flash('文件上传完成', 'dfupload_success')
        except:
            flash('接口文件上传失败,请重新上传', 'dfupload_error')
            return render_template('bs/df_upload.html', form=form)
        try:
            #   目前版本只支持UF20的数据库解析
            if sys_select == 'UF20':
                #   执行数据库解析，并导入数据库（如果数据库存在相关信息，先删除，后插入）
                uf20Parse(sys_no, save_path_file)
            else:
                flash('当前只支持UF20数据库解析', 'dfupload_error')
                return render_template('bs/df_upload.html', form=form)
        except:
            flash('数据库新增失败，请重试', 'dfupload_error')
            return render_template('bs/df_upload.html', form=form)
        flash(',接口文件解析完成', 'dfupload_success')
        return redirect(url_for('bs.dfMng'))
    return render_template('bs/df_upload.html', form=form)


#   下载数据库文件
@bs.route('/dfdownload/<file_path>')
@userLogin
def dfDownload(file_path):
    #   接口文件下载 send_file方法
    file_name = file_path.rsplit('\\')[-1]
    return send_file(file_path, as_attachment=True, attachment_filename=file_name)


#   si=sericeinfo，系统信息文件上传后的查看管理界面
@bs.route('/simng', methods=['GET', 'POST'])
@userLogin
def siMng():
    g.si = ServiceInfo.query.order_by(ServiceInfo.upload_time.desc()).all()
    return render_template('bs/si_mng.html')


#   si=sericeinfo，系统信息文件上传界面
@bs.route('/siupload', methods=['GET', 'POST'])
@userLogin
def siUpload():
    form = SiUploadForm()
    if form.validate_on_submit():
        data = form.data
        f = form.file.data  # 上传的文件
        #   文件夹
        save_path = os.path.join(app.root_path, 'storages', 'ServiceInfo', ('硬件信息', '系统信息')[data['select'] == 2],
                                 'version-' + data['version'])
        #   文件绝对路径
        save_path_file = os.path.join(save_path, f.filename)
        #   检测数据库是否有同一个版本相同目录文件
        if ServiceInfo.query.filter_by(service_type=data['select'], version=data['version'],
                                       file_path=save_path_file).count() >= 1:
            flash('不允许上传同版本文件，请先删除后上传,或者修改版本', 'siupload_error')
            return render_template('bs/if_upload.html', form=form)
        #   保存文件到服务器，没有目录创建目录
        if not os.path.exists(save_path):
            os.makedirs(save_path, mode=0o777)  # 文件夹权限
        try:
            #   保存文件
            f.save(save_path_file)
            #   数据库写入
            service_info = ServiceInfo(
                service_type=data['select'],
                file_name=f.filename,
                file_path=save_path_file,
                version=data['version'],
            )
            db.session.add(service_info)
            db.session.commit()
        except:
            flash('接口文件上传失败', 'siupload_error')
        flash('接口文件上传完成', 'siupload_success')
        return redirect(url_for('bs.siMng'))
    return render_template('bs/si_upload.html', form=form)


#   下载接口文件
@bs.route('/sidownload/<file_path>')
@userLogin
def siDownload(file_path):
    #   接口文件下载 send_file方法
    file_name = file_path.rsplit('\\')[-1]
    return send_file(file_path, as_attachment=True, attachment_filename=file_name)


#   删除接口文件与数据库信息
@bs.route('/sidelete/<sys_id>')
@userLogin
def siDelete(sys_id):
    file_path = ServiceInfo.query.get(sys_id).file_path
    try:
        #   删除数据库信息
        file_db = ServiceInfo.query.get(sys_id)
        db.session.delete(file_db)
        db.session.commit()
        #   删除服务器文件
        os.remove(file_path)
        flash('删除成功', 'sidelete_success')
    except:
        flash('删除失败，请联系田凌看看', 'sidelete_failed')
    return redirect(url_for('bs.siMng'))


#   删除接口文件与数据库信息
@bs.route('/sipreview/<sys_id>')
@userLogin
def siPreview(sys_id):
    service_type = ServiceInfo.query.get(sys_id).service_type
    if service_type == '1':
        file_path = ServiceInfo.query.get(sys_id).file_path
        file_name = file_path.rsplit('\\')[-1]
        data = siHardExcelPreview(file_path)
        return render_template('bs/si_preview.html', data=data, file_name=file_name, service_type=service_type)
    elif service_type == '2':
        file_path = ServiceInfo.query.get(sys_id).file_path
        file_name = file_path.rsplit('\\')[-1]
        data = siSoftExcelPreview(file_path)
        return render_template('bs/si_preview.html', data=data, file_name=file_name, service_type=service_type)
