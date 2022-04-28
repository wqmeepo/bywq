from app.bs import bs
from app import db
from app.bs.forms import BusinSysInfoForm, InterfaceFileForm, DbFileForm, DfFieldSearchForm, SiUploadForm, \
    IfFieldSearchForm
from app.models import UF20TableInfo, BusinSysInfo, InterfaceFile, ServiceInfo, Dictionary, InterfaceFuncInfo, \
    AnnounceInfo, OsTableInfo
from flask import render_template, url_for, redirect, flash, g, send_file
from sqlalchemy import or_, and_
import os
import time
import xlrd
from app.functions.iterExcel import siHardExcelPreview, siSoftExcelPreview, uf20InterfaceFileSearch
from app.jymng.views import jyUserLogin
from app.home.views import userLogin


#   bs=Business system，业务系统，该view管理所有业务系统相关页面
@bs.route('/')
@jyUserLogin
def index():
    announce_info = AnnounceInfo.query.filter(or_(AnnounceInfo.to_who == "1", AnnounceInfo.to_who == "3")).order_by(
        AnnounceInfo.modify_time.desc()).limit(3).all()
    return render_template('bs/bs_index.html', announce_info=announce_info)


@bs.route('/bsmap')
@jyUserLogin
def bsMap():
    g.bs_query_data = BusinSysInfo.query.all()
    return render_template('bs/bs_map.html')


#   系统对应映射关系设置界面
@bs.route('/bsmapset', methods=['GET', 'POST'])
@jyUserLogin
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
@jyUserLogin
def ifMng():
    g.bs = db.session.query().filter(BusinSysInfo.sys_no == InterfaceFile.sys_no).with_entities(BusinSysInfo.sys_no,
                                                                                                BusinSysInfo.sys_name,
                                                                                                BusinSysInfo.manager).distinct().all()
    g.interface = InterfaceFile.query.order_by(InterfaceFile.upload_time.desc()).all()
    return render_template('bs/if_mng.html')


#   if=interface，接口文件上传界面
@bs.route('/ifupload', methods=['GET', 'POST'])
@jyUserLogin
def ifUpload():
    def uf20InterfaceFileParse(sys_no, file_path):
        df = xlrd.open_workbook(file_path)
        func_list = df.sheet_by_name('功能列表')
        # hyperlink_map结果为所有有超链接的字段形成的字典{(x,y):'链接',}
        for i, j in func_list.hyperlink_map.items():
            data = func_list.row_values(i[0])
            interface_func_Info = InterfaceFuncInfo(
                sys_no=sys_no,
                file_path=file_path,
                func_no=data[1],
                func_name=data[5],
                func_describe=data[6],
                func_no_old=data[2],
                func_range=data[3],
                product_range=data[4],
                func_status=data[7],
                func_return=data[8],
                hyperlink_position=str(j.textmark.split('!C')[1])
            )
            db.session.add(interface_func_Info)
            db.session.commit()

    g.bs = BusinSysInfo.query.all()  # 用于传到前端进行展示
    form = InterfaceFileForm()
    if form.validate_on_submit():
        data = form.data
        f = form.file.data  # 上传的文件
        #   获取映射系统名称
        sys_select = BusinSysInfo.query.filter_by(sys_no=data['select']).first().sys_name
        #   文件夹
        from manage import app
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
            #   数据库写入(interfacefile表)
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
        if 'uf2' in sys_select or 'UF2' in sys_select or 'O3' in sys_select or 'o3' in sys_select:
            while not os.path.exists(save_path_file):
                time.sleep(1)
            uf20InterfaceFileParse(data['select'], save_path_file)
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


# if=interface,接口信息搜索
@bs.route('/ifsearch', methods=['GET', 'POST'])
@jyUserLogin
def ifSearch():
    g.bs = BusinSysInfo.query.all()
    form = IfFieldSearchForm()
    if form.validate_on_submit():
        data = form.data
        sys_no = data['select_sys']
        key_word = data['keyword'].strip(' ')
        select_type = data['select_type']
        g.sys = BusinSysInfo.query.filter_by(sys_no=sys_no).first()
        if select_type == 1:
            g.query_result = InterfaceFuncInfo.query.filter(
                and_(InterfaceFuncInfo.sys_no == sys_no,
                     or_(InterfaceFuncInfo.func_no.like(f"%{key_word}%"),
                         InterfaceFuncInfo.func_no_old.like(f"%{key_word}%")))
            ).all()
            return render_template('bs/if_search.html', form=form)
        elif select_type == 2:
            g.query_result = InterfaceFuncInfo.query.filter(
                and_(InterfaceFuncInfo.sys_no == sys_no,
                     or_(InterfaceFuncInfo.func_name.like(f"%{key_word}%"),
                         InterfaceFuncInfo.func_describe.like(f"%{key_word}%")))
            ).all()
            return render_template('bs/if_search.html', form=form)
    return render_template('bs/if_search.html', form=form)


#   ajax用，查询接口详细信息
@bs.route('/if_func_query/<func_no>', methods=['GET', 'POST'])
@userLogin
def ifFuncQuery(func_no):
    file_path = InterfaceFuncInfo.query.filter_by(func_no=func_no).first().file_path
    data = uf20InterfaceFileSearch(func_no, file_path)
    return render_template('bs/if_preview.html', data=data)


#   删除接口文件与数据库信息
@bs.route('/ifdelete/<sys_id>')
@jyUserLogin
def ifDelete(sys_id):
    file_path = InterfaceFile.query.get(sys_id).file_path
    try:
        #   删除数据库信息
        file_db = InterfaceFile.query.get(sys_id)
        InterfaceFuncInfo.query.filter_by(file_path=file_path).delete()
        db.session.delete(file_db)
        db.session.commit()
        #   删除服务器文件
        os.remove(file_path)
    except:
        flash('删除失败，请联系田凌看看', 'ifdelete_failed')
    return redirect(url_for('bs.ifMng'))


# df=Database File，数据库文件上传解析后管理页面
@bs.route('/dfmng', methods=['GET', 'POST'])
@jyUserLogin
def dfMng():
    g.bs = BusinSysInfo.query.all()
    #   group_by一下TableInfo表，因为这个表是按字段导入
    g.df = UF20TableInfo.query.with_entities(UF20TableInfo.sys_no, UF20TableInfo.file_path).group_by(
        UF20TableInfo.sys_no,
        UF20TableInfo.file_path).all()
    g.df_os = OsTableInfo.query.with_entities(OsTableInfo.sys_no, OsTableInfo.file_path).group_by(
        OsTableInfo.sys_no,
        OsTableInfo.file_path).all()
    return render_template('bs/df_mng.html')


# df=Database File，数据库信息检索
@bs.route('/dfsearch', methods=['GET', 'POST'])
@jyUserLogin
def dfSearch():
    g.bs = BusinSysInfo.query.all()
    form = DfFieldSearchForm()
    sys_name = 'unsearch'
    if form.validate_on_submit():
        data = form.data
        sys_no = data['select_sys']
        select_type = data['select_type']
        key_word = data['keyword'].strip(' ')
        g.sys = BusinSysInfo.query.filter_by(sys_no=sys_no).first()
        if 'UF20' in g.sys.sys_name and '多金融' not in g.sys.sys_name or \
                'UF2.0' in g.sys.sys_name and '多金融' not in g.sys.sys_name:
            if select_type == 1:
                g.query_result = UF20TableInfo.query.filter(
                    and_(UF20TableInfo.sys_no == sys_no, UF20TableInfo.db_name.notlike(f"%HS_PROD%"),
                         or_(UF20TableInfo.table_name.like(f"%{key_word}%"),
                             UF20TableInfo.table_describe.like(f"%{key_word}%")))
                ).all()
            elif select_type == 2:
                g.query_result = UF20TableInfo.query.filter(
                    and_(UF20TableInfo.sys_no == sys_no, UF20TableInfo.db_name.notlike(f"%HS_PROD%"),
                         or_(UF20TableInfo.field_name.like(f"%{key_word}%"),
                             UF20TableInfo.field_describe.like(f"%{key_word}%")))
                ).all()
            sys_name = 'UF20'
            return render_template('bs/df_search.html', form=form, sys_name=sys_name)
        elif '多金融' in g.sys.sys_name:
            if select_type == 1:
                g.query_result = UF20TableInfo.query.filter(
                    and_(UF20TableInfo.sys_no == sys_no, UF20TableInfo.db_name.like(f"%HS_PROD%"),
                         or_(UF20TableInfo.table_name.like(f"%{key_word}%"),
                             UF20TableInfo.table_describe.like(f"%{key_word}%")))
                ).all()
            elif select_type == 2:
                g.query_result = UF20TableInfo.query.filter(
                    and_(UF20TableInfo.sys_no == sys_no, UF20TableInfo.db_name.like(f"%HS_PROD%"),
                         or_(UF20TableInfo.field_name.like(f"%{key_word}%"),
                             UF20TableInfo.field_describe.like(f"%{key_word}%")))
                ).all()
            sys_name = 'UF20'
            return render_template('bs/df_search.html', form=form, sys_name=sys_name)
        elif '法人清算' in g.sys.sys_name:
            key_word = key_word.upper()
            if select_type == 1:
                g.query_result = OsTableInfo.query.filter(
                    and_(OsTableInfo.sys_no == sys_no, or_(OsTableInfo.table_name.like(f"%{key_word}%"),
                                                           OsTableInfo.table_describe.like(f"%{key_word}%")))).all()
            elif select_type == 2:
                g.query_result = OsTableInfo.query.filter(
                    and_(OsTableInfo.sys_no == sys_no, or_(OsTableInfo.field_name.like(f"%{key_word}%"),
                                                           OsTableInfo.field_describe.like(f"%{key_word}%")))).all()
            sys_name = '法人清算'
            return render_template('bs/df_search.html', form=form, sys_name=sys_name)
        elif 'O32' in g.sys.sys_name or 'o32' in g.sys.sys_name:
            key_word = key_word.upper()
            if select_type == 1:
                g.query_result = OsTableInfo.query.filter(
                    and_(OsTableInfo.sys_no == sys_no, or_(OsTableInfo.table_name.like(f"%{key_word}%"),
                                                           OsTableInfo.table_describe.like(f"%{key_word}%")))).all()
            elif select_type == 2:
                g.query_result = OsTableInfo.query.filter(
                    and_(OsTableInfo.sys_no == sys_no, or_(OsTableInfo.field_name.like(f"%{key_word}%"),
                                                           OsTableInfo.field_describe.like(f"%{key_word}%")))).all()
            sys_name = 'O32'
            return render_template('bs/df_search.html', form=form, sys_name=sys_name)
        else:
            return render_template('bs/df_search.html', form=form, sys_name=sys_name)
    return render_template('bs/df_search.html', form=form, sys_name=sys_name)


# ajax用，查询字典字段信息
@bs.route('/querydictionary/<field_name>', methods=['GET', 'POST'])
@userLogin
def queryDictionary(field_name):
    query_dictionary_data = Dictionary.query.filter_by(field_name=field_name).all()
    if len(query_dictionary_data) == 0:
        return '<p>该字段没有数据字典信息</p>'
    else:
        return render_template('bs/df_modal.html', data=query_dictionary_data)


# df=Database File，数据库文件上传，解析的页面
@bs.route('/dfupload', methods=['GET', 'POST'])
@jyUserLogin
def dfUpload():
    #   针对UF20数据库excel文件的解析方法，支持覆盖导入（先删除，后插入），写的比较烂，后续再优化
    def uf20Parse(sys_no, save_path_file):
        df = xlrd.open_workbook(save_path_file)
        total_list = []
        num = 0
        # 解析
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
        # 删除+新增
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
                        table_delete = UF20TableInfo.query.filter_by(sys_no=sys_no, table_name=list_sheet[i + 2]).all()
                        for each in table_delete:
                            db.session.delete(each)
                        k += 2
                    db.session.commit()

                    while j <= i + count:
                        if j + 1 > i + count:
                            break
                        table_info = UF20TableInfo(
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

    #   针对o32数据库excel文件的解析方法，覆盖导入（先删除，后插入）
    def o32Parse(sys_no, save_path_file):
        df = xlrd.open_workbook(save_path_file)
        for sheet in df.sheets():
            for i in range(sheet.nrows):
                if 'table_name' in sheet.row_values(i):
                    count = 3
                    while len(sheet.row_values(i + count)) != sheet.row_values(i + count).count(''):
                        os_table_info = OsTableInfo(
                            sys_no=sys_no,
                            table_name=sheet.row_values(i)[2],
                            table_describe=sheet.row_values(i)[4],
                            db_user_name='trade',
                            field_name=sheet.row_values(i + count)[2],
                            field_describe=sheet.row_values(i + count)[3],
                            busin_sys=sheet.name,
                            file_path=save_path_file,
                            remark=sheet.row_values(i + count)[9]
                        )
                        db.session.add(os_table_info)
                        count += 1
                        if str(i + count) == str(sheet.nrows - 1):
                            break
                db.session.commit()

    g.bs = BusinSysInfo.query.all()
    form = DbFileForm()
    if form.validate_on_submit():
        data = form.data
        sys_no = data['select']
        f = form.file.data
        sys_select = BusinSysInfo.query.filter_by(sys_no=sys_no).first().sys_name
        from manage import app
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
        # try:
        #   UF20的数据库解析，包含UF20与UF20多金融系统
        if 'UF20' in sys_select:
            #   执行数据库解析，并导入数据库（如果数据库存在相关信息，先单独删除，后单独插入）
            uf20Parse(sys_no, save_path_file)
        elif 'O32' in sys_select:
            #   执行数据库解析，并导入数据库（如果数据库存在相关信息，先全量删除，后全量插入）
            os_table_all_o32 = OsTableInfo.query.filter(OsTableInfo.sys_no == sys_no).all()
            for each in os_table_all_o32:
                db.session.delete(each)
            db.session.commit()
            o32Parse(sys_no, save_path_file)
        else:
            flash('当前只支持O32与UF20数据库解析', 'dfupload_error')
            return render_template('bs/df_upload.html', form=form)
        # except:
        #     flash('数据库新增失败，请重试', 'dfupload_error')
        #     return render_template('bs/df_upload.html', form=form)
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


#   si=serviceinfo，系统信息文件上传后的查看管理界面
@bs.route('/simng', methods=['GET', 'POST'])
@jyUserLogin
def siMng():
    g.si = ServiceInfo.query.order_by(ServiceInfo.upload_time.desc()).all()
    return render_template('bs/si_mng.html')


#   si=serviceinfo，系统信息文件上传界面
@bs.route('/siupload', methods=['GET', 'POST'])
@jyUserLogin
def siUpload():
    form = SiUploadForm()
    if form.validate_on_submit():
        data = form.data
        f = form.file.data  # 上传的文件
        #   文件夹
        from manage import app
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


#   si=serviceinfo，下载软硬件文件
@bs.route('/sidownload/<file_path>')
@jyUserLogin
def siDownload(file_path):
    #   接口文件下载 send_file方法
    file_name = file_path.rsplit('\\')[-1]
    return send_file(file_path, as_attachment=True, attachment_filename=file_name)


#   si=serviceinfo，删除软硬件信息文件
@bs.route('/sidelete/<sys_id>')
@jyUserLogin
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


#   si=serviceinfo，解析excel并预览软硬件信息文件
@bs.route('/sipreview/<sys_id>')
@jyUserLogin
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


#   公告预览
@bs.route('/announcepreview/<sys_id>', methods=['GET', 'POST'])
@jyUserLogin
def announcePreview(sys_id):
    announce_info = AnnounceInfo.query.get(sys_id).announce_body
    return announce_info


# split过滤器 for jinja2
@bs.app_template_filter('jinjaSplit')
def jinjaSplit(jinjiaString: str, splitString: str):
    return jinjiaString.split(splitString)
