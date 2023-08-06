from datetime import datetime, timezone
import os
import queue
import threading
import time
import json
import requests
import signal
import sys
import traceback
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

try:
    import thread
except ImportError:
    import _thread as thread

from pymongo import MongoClient, ASCENDING, DESCENDING
from logger import Logger

LL9 = 1000000000

class MongoClientTradeGateway(object):
    def __init__(self, config_path, endtime):
        
        self.load_gateway_setting(config_path)
        self.logger = Logger.get_logger(self.logname, self.log_file_path)
        self.gen_local_id()
        self.endtime = endtime
        self.is_stopped = False
        self.start_mongodb()
        
        self.thread_pool = ThreadPoolExecutor(10)
        self.buy_orderlock = threading.Lock()
        self.sell_orderlock = threading.Lock()
        self.cancel_orderlock = threading.Lock()
        
        self.order_dbids = []
        self.sell_order_dbids = []
        self.cancel_order_ids = []
        
        self.date = self.get_date_today()
        
        
    def error_handler(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self,*args, **kwargs)
            except Exception as e:
                err = traceback.format_exc()
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
                self.logger.error(f'[{wrapper}] (exception){err}')
                self.send_to_user(err)
                return 'error'
        return wrapper
        
    def load_gateway_setting(self, config_path):
        try:
            #固定配置文件的名字
            config_filename = os.path.join(config_path, 'atx_server_config.json')
            #f = open(config_filename, encoding="utf-8")
            f = open(config_filename, encoding='gbk')
            setting = json.load(f)
            
            log_path = setting['log_filepath']
            self.log_file_path = log_path.replace('/', '\\')
            self.url_list = setting.get('url_list')

            self.logname = setting['logname']
            self.scan_interval = setting['scan_interval']
            
            self.accounts_config = setting['accounts']
            self.accounts_run = setting['run']
            
            self.config = {}
            self.account_id = {}
            self.account_id_to_acc = {}
            self.product_names = {}
            self.log_account_names = {}
            self.tgnames = {}
            self.mongo_host = {}
            self.mongo_port = {}
            self.tradingaccount_user = {}
            self.tradingaccount_pwd = {}
            self.tradinglog_user = {}
            self.tradinglog_pwd = {}
            self.target_account_names = {}
            self.target_account_names_to_acc = {}
            for acc in self.accounts_run:
                self.config[acc] = setting['accounts'][acc]
                config = self.config[acc]
                self.account_id[acc] = config['account_id']
                self.account_id_to_acc[config['account_id']] = acc
                self.product_names[acc] = config['product_name']
                self.log_account_names[acc] = config['account_name']
                self.tgnames[acc] = config['equity_tg_name']
                self.target_account_names[acc] = config['equity_tg_name'] + "@" + config['account_name']
                self.target_account_names_to_acc[self.target_account_names[acc]] = acc
                self.mongo_host[acc] = config['mongoHost']
                self.mongo_port[acc] = config['mongoPort']
                datadbuser = config['databaseUser']
                self.tradingaccount_user[acc] = datadbuser['tradingAccount']['user']
                self.tradingaccount_pwd[acc] = datadbuser['tradingAccount']['password']
                self.tradinglog_user[acc] = datadbuser['tradingLog']['user']
                self.tradinglog_pwd[acc] = datadbuser['tradingLog']['password']
            
        except Exception as e:
            err = traceback.format_exc()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
            print(f"load config failed! (exception){err}")
            exit(0)
    
    def start_mongodb(self):
        try:
            self.db_client = {}
            self.order_info_db = {}
            self.tradelog_db = {}
            for acc in self.accounts_run:
                self.db_client[acc] = MongoClient(
                    self.mongo_host[acc], self.mongo_port[acc], connectTimeoutMS=10000)
                db_client = self.db_client[acc]
                if self.tradingaccount_user[acc] != '' and self.tradingaccount_pwd[acc] != '':
                    db_client["tradingAccount"].authenticate(
                        self.tradingaccount_user[acc], self.tradingaccount_pwd[acc], mechanism='SCRAM-SHA-1')
                self.order_info_db[acc] = db_client["tradingAccount"]
                
                if self.tradinglog_user[acc] != '' and self.tradinglog_pwd[acc] != '':
                    db_client["tradingLog"].authenticate(
                        self.tradinglog_user[acc], self.tradinglog_pwd[acc], mechanism='SCRAM-SHA-1')
                db_client.server_info()
                self.tradelog_db[acc] = db_client["tradingLog"] 
                
            #for test
            #self.db_client = MongoClient()
            #test for req_position
            #self.db_client_test = MongoClient("127.0.0.1", 27017, connectTimeoutMS=10000)
            #self.test_trading_account = self.db_client_test['tradingAccount']
        except Exception as e:
            err = traceback.format_exc()
            self.send_to_user(err)
            self.logger.error(f'[init] DB_connect_failed! (exception){err}')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
            exit()

    #通过tradingAccount.accountinfo表获取产品属性
    def get_account_info(self):
        for acc in self.accounts_run:
            product_name = self.product_names[acc]
            query = {"product_name": product_name}
            account_info_collection = self.order_info_db[acc]['account_info']
            account_info = account_info_collection.find_one(query)
            if account_info == None:
                self.logger.error(
                    f"[get_account_info] can't_find_account_info (product_name){product_name}")
                continue
            tgname = account_info['equity_tg_name']
            self.tgnames[acc] = tgname
            log_accountname = account_info['account_name']
            self.log_account_names[acc] = log_accountname
            target_accountname = tgname + '@' + log_accountname
            self.target_account_names[acc] = target_accountname # 下单时用self
            self.logger.info(
                f"[get_account_info] (tg_name){self.tgnames} (logacc_name){self.log_account_names} (target_accountnames){self.target_account_names}") 

    def send_to_user(self, error):
        try:
            if self.url_list == None:
                self.logger.info("[send_to_user] send_message_failed")
                return
            url = self.url_list

            payload_message = {
                "msg_type": "text",
                "content": {
                    "text": f'ERROR! (exception){error}'
                }
            }
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=json.dumps(payload_message))
            self.logger.info(f"[send_to_user] (response){response}")
        except Exception as e:
            err = traceback.format_exc()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=None, file=sys.stdout)
            self.logger.error(f'[send_to_user] send_message_failed(exception){err}')
    
    def signal_handler(self, signum=None, frame=None):
        self.is_stopped = True
    
    def gen_local_id(self):
        self.id_base = 1377779200 * LL9
        self.sp = time.time_ns()
        self.local_id = self.sp - self.id_base

    def gen_order_id(self):
        self.local_id += 1
        return self.local_id
    
    def get_date_today(self):
        dt = datetime.now()
        date = str(dt.strftime("%Y%m%d"))
        self.logger.info("[get_date_today] (date){date}")
        return date
    
    @error_handler
    def date_change(self):
        while not self.is_stopped:
                dt = datetime.now()
                time_now = time.strftime("%H:%M", time.localtime())
                if time_now == self.endtime:
                    self.close()                 
                else:
                    self.logger.info(f"[date_change] not_closed (now){dt}")
                time.sleep(60) 
    
    def close(self):
        self.is_stopped = True
        print (f"[close] (close_time){self.endtime}")
        self.logger.info(f"[close] (setting_close_time){self.endtime}")
        os._exit(0)
        

