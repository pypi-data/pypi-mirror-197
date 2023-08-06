

from pymongo import MongoClient
from random import randint
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
from sys import stdout
from dateutil import parser
from psycopg import connect
from os import getenv
from klp_commons.log.structuredMessage import StructuredMessage
from logging import getLogger
from dateutil.parser import parse
from pandas import DataFrame
import traceback
from pickle import load as load_
# from report.cryptology import Cryptology
from pymongo.errors import DuplicateKeyError, BulkWriteError
from json import loads
from os import remove
fmt = StructuredMessage
message = 'mongoDBController'

class ControllerMongoDB:
    """
    for timestamp use :
    
        expiry_date = '2021-07-13T00:00:00.000Z'
        expiry = parser.parse(expiry_date)

    """
    # Variables de clase

    def __init__(self, pad: int = None):
        self.logger = getLogger("ControllerMongo")

        self.MONGODB_URL = getenv("MONGODB_URL")        
        self.data = None
        self.client = None
        self.con_db = None
        self.format_exter = '%Y-%m-%dT%H:%M:%S.%f%z'
        self.format_inter = '%Y-%m-%dT%H:%M:%S'
        self.logger.info("done creating an instance of ControllerMongo")

    def get_con_mongo(self):
        try:
            self.logger.info("createnig connection MongoClient")

            self.client = MongoClient(self.MONGODB_URL,authSource="admin")

        except Exception as e:
            self.logger.error("Exception createnig connection MongoClient seen: " + str(e))
            traceback.print_exc(file = stdout)
            
        self.logger.info("done createnig connection MongoClient")

    def close_con(self):
        try:
            self.logger.info("close_con()  ControllerMongo")

            self.client.close()
        except Exception as e:
            self.logger.error("Exception close_con() ControllerMongo seen: " + str(e))
            traceback.print_exc(file = stdout)
        
        self.logger.info("done close_con()  ControllerMongo")
         
    def get_list_dbs(self):
        return self.client.list_database_names()

    def get_con_db(self,name_db):
        self.get_con_mongo()
        self.con_db  = self.client[name_db]

    def get_con_collect(self,collection_name,db_name="klopp"):
        self.get_con_mongo()
        self.con_db  = self.client[db_name][collection_name]

    def insert_one_fact(self):
        try:
            self.con_db.fact.insert_one(self.data)
        except Exception as e:
            self.logger.exception(e, exc_info=True)
        finally:
            self.client.close()
            
    def exist(self,key,value):
        try:
            return bool(self.con_db.find_one({key:value}))
        except Exception as e:
            self.logger.exception(e, exc_info=True)
        finally:
            self.client.close()
            
    def insert_one_collection(self):
        try:
            self.con_db.insert_one(self.data)
        except Exception as e:
            self.logger.exception(e, exc_info=True)
        finally:
            self.client.close()

    def insert_many_fact(self,categorized):
        
        try:
            self.con_db.fact.insert_many(self.data)

        except (DuplicateKeyError, BulkWriteError) as e:

            self.logger.exception(e, exc_info=True)

            if categorized == True:
                self.con_db.fact.update_many(self.data,upsert=True)

            else :
                self.logger.info("Save into error colecction mongodb ")
                self.insert_error()
                self.logger.info("Done save into error colecction mongodb ")

        except Exception as e:
            self.logger.exception(e, exc_info=True)
        finally:
            self.client.close()

    def insert_error(self):
        try:
            self.con_db.errorDuplicateKey.insert_one({"error":self.data})   
        except Exception as e:
            self.logger.exception(e, exc_info=True)

    def insert_error_ms_report(self):
        try:
            self.con_db.errorMSReport.insert_one({"error":self.data})   
        except Exception as e:
            self.logger.exception(e, exc_info=True)

    def insert_error_ms_cat(self):
        try:
            self.con_db.errorMSCat.insert_one({"error":self.data})   
        except Exception as e:
            self.logger.exception(e, exc_info=True)

    def insert_errorNoFound(self):

        try:

            self.con_db.errorSubcategoryNoFound.insert_one({"error":self.data})   
        except Exception as e:
            self.logger.error(e, exc_info=True)

    def insert_many_analytic(self):
        try:
            self.con_db.analytic.insert_many(self.data)

        except (DuplicateKeyError, BulkWriteError) as e:
            self.logger.error(e, exc_info=True)

            if self.data['categorized'] == True:
                self.con_db.fact.update_many(self.data,upsert=True)
            else :
                self.logger.info("Save into error colecction mongodb ")
                self.insert_error()
                self.logger.info("Done save into error colecction mongodb ")

        except Exception as e:
            self.logger.error(e, exc_info=True)
        finally:
            self.client.close()

    def update_one_fact(self,ref, new_item):
        try:
            query = { "_id": ref}
            new_item = {'$push': {'history-track': new_item}}
            self.con_db.fact.update_one(query,new_item)
        
        except Exception as e:
            self.logger.error(e, exc_info=True)
        finally:
            self.client.close()

    def set_document(self,data):
        self.data = data  

    def ingesta_mongo(self,key,pad,fact_path,path_analytic):
        import datetime
        from utils.utils import divide_chunks

        crypto = Cryptology(pad)

        crypto.set_key(key)


        # Load data (deserialize)
        with open(fact_path, 'rb') as handle:
            data = load_(handle)

        fact = crypto.decrypt(data)

        self.data = loads(fact)

        for item in self.data:
            item['created_at'] = datetime.strptime(item['created_at'].split('+')[0].split('.')[0], self.format_extern).replace(microsecond=0).isoformat()


        docs_array = divide_chunks(list(self.data))
        for item in docs_array:
            self.data = item
            self.get_con_db('klopp')
            self.insert_many_fact()

        # Load data (deserialize)
        with open(path_analytic, 'rb') as handle:
            data = load_(handle)

        analytic = crypto.decrypt(data)
        self.data = loads(analytic)

        docs_array = divide_chunks(list(self.data))
        for item in docs_array:
            self.data = item
            self.get_con_db('klopp')
            self.insert_many_analytic()


        


        remove(fact_path)
        remove(path_analytic)