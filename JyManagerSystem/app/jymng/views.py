from app.jymng import jymng


#   jy=交易系统研发中心，该view管理研发中心的公告、知识分享、监管信息等信息
@jymng.route('/announcemng')
def announceMng():
    return "announcemng"
