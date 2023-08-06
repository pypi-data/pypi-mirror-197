import pymysql
from sshtunnel import SSHTunnelForwarder
from ddreport.exceptd import exceptContentObj


class PytestMysql:
    def __init__(self, db, db_ssh=None):
        self.__SSH = False
        if db_ssh:
            self.__SSH = True
            ssh_address_or_host, ssh_username = (db_ssh["host"], db_ssh['port']), db_ssh['user']
            remote_bind_address = (db['host'], db['port'])
            ssh_db_config = {"ssh_address_or_host": ssh_address_or_host, "ssh_username": ssh_username, "remote_bind_address": remote_bind_address}
            if db_ssh.get('password'):
                ssh_db_config['ssh_password'] = db_ssh.get('password')
            else:
                ssh_db_config['ssh_pkey'] = db_ssh.get('pkey') or None
            self.__server = SSHTunnelForwarder(**ssh_db_config)
        self.__condb(db)

    # 抛出异常
    def __execptions(self, err):
        exceptContentObj.raiseException({"错误详情": err})

    def __condb(self, db):
        try:
            data = {**db, **{'charset': 'utf8', 'cursorclass': pymysql.cursors.DictCursor, 'autocommit': True}}
            if self.__SSH is True:
                self.__server.start()
                data['host'], data['port'] = "127.0.0.1", self.__server.local_bind_port  # 重新赋值
            self.__conn = pymysql.connect(**data)
            self.__conn.ping(reconnect=True)
            self.__cursor = self.__conn.cursor()
        except Exception:
            self.__conn = None

    def query(self, selector):
        if self.__conn:
            self.__cursor.execute(selector)
            res = self.__cursor.fetchall()
            # self._colse()
            return res or []
        else:
            self.__execptions("Mysql Connection timed out: Connect failed")
            # return "Connection timed out: Connect failed"

    def off(self):
        if self.__conn:
            self.__cursor.close()  # 关闭游标
            self.__conn.close()  # 关闭数据库连接
            if self.__SSH is True:
                self.__server.close()


# db = {"host": "10.107.14.55", "port": 3306, "user": "root", "password": "123456"}
# db_ssh = {"host": "10.42.101.101", "port": 22, "user": "root", "password": None, "pkey": "kube_dev"}
#
# DB = DBMysql(db, db_ssh)
# a = DB.query("SET global sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'")
# print(a)
#
# a1 = DB.query("select version()")
# print(a1)
#
# DB.db_colse()
