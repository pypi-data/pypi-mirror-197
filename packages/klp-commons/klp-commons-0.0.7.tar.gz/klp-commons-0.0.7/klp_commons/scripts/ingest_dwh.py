
from datetime import datetime
from datetime import date
import numpy as np
import pandas as pd
from datetime import datetime,timedelta

from klp_commons.controllers.controller_redshift import ControllerRedShift
from klp_commons.controllers.controller_mongodb import ControllerMongoDB
from klp_commons.controllers.controller_postgresdb import ControllerPostgresDB
from klp_commons.datadict.struct_dicts import Transaction_

import logging

logger = logging.getLogger(__name__)


null = None
true = True
false = False

class Summary:
    """
    """

    # Variables de clase

    def __init__(self,from_date_str = None, num_days= 1):
        self.MongoDB = ControllerMongoDB()
        self.MongoDB.get_con_collect(collection_name='fact')

        self.num_days = num_days
        self.last_period = None
        self.from_date = from_date_str
        self.to_date = None
        self.set_date_range()
        
    def set_date_range(self):
        
        self.from_date = datetime.strptime(self.from_date , '%Y-%m-%d')
        self.to_date = self.from_date - timedelta(days=self.num_days)
        self.last_period = self.from_date + timedelta(days=self.num_days)
        print("self.from_date :", self.from_date )
        print("self.to_date :", self.to_date )
        print("self.last_period", self.last_period )
        
    def agg_master(self):
        self.query_summary_category = [
            # { "$unwind": "$history-track" },
            {
            "$match": {
                    "$or":[
                        {"created_at": {'$gte':self.to_date,'$lt': self.from_date}},
                        {"created_at_homologation": {'$gte':self.to_date,'$lt': self.from_date}}
                        ],
                    "$and": [ { "history-track.validated": True}]
                    }
                        },
        {'$group': 
                 {'_id': {
                    "user_uid": "$user_uid",
                    "transaction_uid":"$_id",
                    "currency":"$currency",
                    "lang_code":"$lang_code",
                    "country_code":"$country_code",
                    "type_flow":"$type_flow",
                    "message_type_head":"$message_type",
                    "description":"$source_description",
                    "created_at_homologation":"$created_at_homologation",
                    "created_at_head": "$created_at" ,
                    "account_uid":"$account_id",
                    "bank_name":"$account_institution_name",
                    "account_type" :"$account_type",
                    "bank_type" :"$account_institution_type",

                    "message_type_history":"$history-track.message_type",
                    "message_type_old":"$history-track.type" ,

                    "amount" :"$amount",
                    "model_nlp_version":"$history-track.model_nlp_version", # pre
                    "model_classification_version":"$history-track.model_classification_version",
                    "model_collective_version":"$history-track.model_collective_version",
                    "model_nickname_version":"$history-track.model_nickname_version",
                    "clean_description": "$history-track.clean_description",
                    "classified_date":"$history-track.classification_datetime",

                    "validated":"$history-track.validated", ##validated

                    "approved_asset":"$history-track.approved_asset",
                    "approved_business":"$history-track.approved_business",
                    "approved_category":"$history-track.approved_cat",
                    "approved_frequency":"$history-track.approved_frequency",
                    "approved_is_essential":"$history-track.approved_is_essential",
                    "approved_is_membership":"$history-track.approved_is_membership",
                    "approved_nickname":"$history-track.approved_nickname",
                    "approved_person":"$history-track.approved_person",
                    "approved_special_moment":"$history-track.approved_special_moment",
                    "approved_subcategory":"$history-track.details.approved_subcat",
                    "approved_is_loan_received":"$history-track.details.approved_is_loan_received",
                    "approved_is_loan_requested":"$history-track.details.approved_is_loan_requested",
                    "approved_income_source_uid":"$history-track.details.approved_income_source_uid",
                    
                    "category_custom_type":"$history-track.category_custom_type",
                    "subcategory_custom_type":"$history-track.subcategory_custom_type",
                     
                    "created_at":"$history-track.details.created_at",
                    "updated_at":"$history-track.details.updated_at",
                     
                     
                    "asset_uid_def_algo":"$history-track.details.asset_uid_def_algo",
                    "business_uid_def_algo":"$history-track.details.business_uid_def_algo",
                    "cat_uid_def_algo":"$history-track.details.cat_uid_def_algo",
                    "frequency_uid_def_algo":"$history-track.details.frequency_uid_def_algo",
                    "income_source_uid_def_algo":"$history-track.details.income_source_uid_def_algo",
                    "is_essential_def_algo":"$history-track.details.is_essential_def_algo",
                    "is_loan_received_def_algo":"$history-track.details.is_loan_received_def_algo",
                    "is_loan_requested_def_algo":"$history-track.details.is_loan_requested_def_algo",
                    "is_membership_def_algo":"$history-track.details.is_membership_def_algo",
                    "nickname_algo":"$history-track.details.nickname_algo",
                    "person_uid_def_algo":"$history-track.details.person_uid_def_algo",
                    "special_moment_uid_def_algo":"$history-track.details.special_moment_uid_def_algo",
                    "subcat_uid_def_algo":"$history-track.details.subcat_uid_def_algo",
                     

                    "asset_uid_def_usr":"$history-track.details.asset_uid_def_usr",
                    "asset_uid_def_usr":"$history-track.details.asset_uid_def_usr",
                    "business_uid_def_usr":"$history-track.details.business_uid_def_usr",
                    "cat_uid_def_usr":"$history-track.details.cat_uid_def_usr",
                    "frequency_uid_def_usr":"$history-track.details.frequency_uid_def_usr",
                    "income_source_uid_def_usr":"$history-track.details.income_source_uid_def_usr",
                    "is_essential_def_usr":"$history-track.details.is_essential_def_usr",
                    "is_loan_received_def_usr":"$history-track.details.is_loan_received_def_usr",
                    "is_loan_requested_def_usr":"$history-track.details.is_loan_requested_def_usr",
                    "is_membership_def_usr":"$history-track.details.is_membership_def_usr",
                    "nickname_usr":"$history-track.details.nickname_usr",
                    "nickname_user":"$history-track.details.nickname_user", #user
                    "person_uid_def_usr":"$history-track.details.person_uid_def_usr",
                    "special_moment_uid_def_usr":"$history-track.details.special_moment_uid_def_usr",
                    "subcat_uid_def_usr":"$history-track.details.subcat_uid_def_usr",
            
                    "asset_uid_def_usr_":"$history-track.details.info.asset_uid",
                     "business_uid_def_usr_":"$history-track.details.info.business_uid",
                     "created_at_def_usr_":"$history-track.details.info.created_at",
                     "frequency_uid_def_usr_":"$history-track.details.info.frequency_uid",
                     "income_source_uid_def_usr_":"$history-track.details.info.income_source_uid",
                     "is_essential_def_usr_":"$history-track.details.info.is_essential",
                     "is_loan_received_def_usr_":"$history-track.details.info.is_loan_received",
                     "is_loan_requested_def_usr_":"$history-track.details.info.is_loan_requested",
                     "is_membership_def_usr_":"$history-track.details.info.is_membership",
                     "nickname_usr_":"$history-track.details.info.name",
                     "person_uid_def_usr_":"$history-track.details.info.person_uid",
                     "special_moment_uid_def_usr_":"$history-track.details.info.special_moment_uid",

                     "asset_uid_def_usr_info":"$history-track.info.asset_uid",
                     "business_uid_def_usr_info":"$history-track.info.business_uid",
                     "created_at_def_usr_info":"$history-track.info.created_at",
                     "frequency_uid_def_usr_info":"$history-track.info.frequency_uid",
                     "income_source_uid_def_usr_info":"$history-track.info.income_source_uid",
                     "is_essential_def_usr_info":"$history-track.info.is_essential",
                     "is_loan_received_def_usr_info":"$history-track.info.is_loan_received",
                     "is_loan_requested_def_usr_info":"$history-track.info.is_loan_requested",
                     "is_membership_def_usr_info":"$history-track.info.is_membership",
                     "person_uid_def_usr_info":"$history-track.info.person_uid",
                     "special_moment_uid_def_usr_info":"$history-track.info.special_moment_uid",
                     
                    "asset_uid_def_collect":"$history-track.details.asset_uid_def_collect",
                    "business_uid_def_collect":"$history-track.details.business_uid_def_collect",
                    "cat_uid_def_collect":"$history-track.details.category_uid_def_collect",
                    "frequency_uid_def_collect":"$history-track.details.frequency_uid_def_collect",
                    "income_source_uid_def_collect":"$history-track.details.income_source_uid_def_collect",
                    "is_essential_def_collect":"$history-track.details.is_essential_def_collect",
                    "is_loan_received_def_collect":"$history-track.details.is_loan_received_def_collect",
                    "is_loan_requested_def_collect":"$history-track.details.is_loan_requested_def_collect",
                    "is_membership_def_collect":"$history-track.details.is_membership_def_collect",
                    "nickname_collect":"$history-track.details.nickname_collect",
                    "person_uid_def_collect":"$history-track.details.person_uid_def_collect",
                    "special_moment_uid_def_collect":"$history-track.details.special_moment_uid_def_collect",
                    "subcat_uid_def_collect":"$history-track.details.subcategory_uid_def_collect",
                       },
                'count': {"$sum": 1}
                }
            }
        ]
       
        return pd.json_normalize(pd.DataFrame(list( self.MongoDB.con_db.aggregate(self.query_summary_category) ))['_id']) 

MongoDB = ControllerMongoDB()
PGDB = ControllerPostgresDB()
RedShift = ControllerRedShift()

RedShift.get_conection()

today = date.today()
front_date = today.strftime("%Y-%m-%d")

print(today)
print("front_date: " , front_date)

s = Summary(front_date,num_days = 240)
r = s.agg_master()


r['business_uid_def_usr'] = r['business_uid_def_usr'].apply(lambda x: x) + r['business_uid_def_usr_'].apply(lambda x: x) + r['business_uid_def_usr_info'].apply(lambda x: x)

del r['business_uid_def_usr_']
del r['business_uid_def_usr_info']


r['asset_uid_def_usr'] = r['asset_uid_def_usr'].apply(lambda x: x) + r['asset_uid_def_usr_'].apply(lambda x: x) + r['asset_uid_def_usr_info'].apply(lambda x: x)

del r['asset_uid_def_usr_info']
del r['asset_uid_def_usr_']

r['frequency_uid_def_usr'] = r['frequency_uid_def_usr'].apply(lambda x: x) + r['frequency_uid_def_usr_'].apply(lambda x: x) + r['frequency_uid_def_usr_info'].apply(lambda x: x)

del r['frequency_uid_def_usr_info']
del r['frequency_uid_def_usr_']

r['income_source_uid_def_usr'] = r['income_source_uid_def_usr'].apply(lambda x: x) + r['income_source_uid_def_usr_'].apply(lambda x: x) + r['income_source_uid_def_usr_info'].apply(lambda x: x)

del r['income_source_uid_def_usr_info']
del r['income_source_uid_def_usr_']


r['is_loan_received_def_usr'] = r['is_loan_received_def_usr'].apply(lambda x: x) + r['is_loan_received_def_usr_'].apply(lambda x: x) + r['is_loan_received_def_usr_info'].apply(lambda x: x)

del r['is_loan_received_def_usr_info']
del r['is_loan_received_def_usr_']

r['is_loan_requested_def_usr'] = r['is_loan_requested_def_usr'].apply(lambda x: x) + r['is_loan_requested_def_usr_'].apply(lambda x: x) + r['is_loan_requested_def_usr_info'].apply(lambda x: x)

del r['is_loan_requested_def_usr_info']
del r['is_loan_requested_def_usr_']


r['is_membership_def_usr'] = r['is_membership_def_usr'].apply(lambda x: x) + r['is_membership_def_usr_'].apply(lambda x: x) + r['is_membership_def_usr_info'].apply(lambda x: x)

del r['is_membership_def_usr_info']
del r['is_membership_def_usr_']


r['person_uid_def_usr'] = r['person_uid_def_usr'].apply(lambda x: x) + r['person_uid_def_usr_'].apply(lambda x: x) + r['person_uid_def_usr_info'].apply(lambda x: x)

del r['person_uid_def_usr_info']
del r['person_uid_def_usr_']


r['special_moment_uid_def_usr'] = r['special_moment_uid_def_usr'].apply(lambda x: x) + r['special_moment_uid_def_usr_'].apply(lambda x: x) + r['special_moment_uid_def_usr_info'].apply(lambda x: x)

del r['special_moment_uid_def_usr_info']
del r['special_moment_uid_def_usr_']


for col in sorted(r.columns.tolist()):
    r[col] = r.explode(col).reset_index()[col]

    
#r[cols].set_index(['nickname_def_usr','category_uid_def_algo']).apply(pd.Series.explode).reset_index()
# .sort_values(by=['created_at_head'], ascending = False)
print("shape: ", r.shape)

r.replace(np.nan, None, inplace=True)
r.replace(pd.NaT, None, inplace=True)
tmp = {'created_at_homologation': pd.NaT}

print(r.columns.tolist())

for idx ,item in enumerate(r.to_dict(orient='records')):
    print(idx, ": ",item['transaction_uid'])
    print("... ")
    if 'classification_datetime' in item:
        item['classified_at'] = item['classification_datetime']

    if not item['lang_code']:
        item['language_code'] = 'es-MX'
    else :
        item['language_code'] = 'es-MX'
        

    # Dict to necessary data
    transaction_dict = Transaction_().get()
    transaction_dict.update(item)


    transaction_dict['message_type'] = item['message_type_old']
    transaction_dict['flow_type'] = ''
    
    if not transaction_dict['clean_description']:
        transaction_dict['clean_description'] = ''


    if not transaction_dict['source_description']:
        transaction_dict['source_description'] = ''

    if not transaction_dict['model_classification_version']:
        transaction_dict['model_classification_version'] = ''

    if not transaction_dict['model_nickname_version']:
        transaction_dict['model_nickname_version'] = ''

    if not transaction_dict['model_nlp_version']:
        transaction_dict['model_nlp_version'] = ''

    if not transaction_dict['model_collective_version']:
        transaction_dict['model_collective_version'] = ''

        
    format_inter = '%Y-%m-%dT%H:%M:%S'
    
    if not transaction_dict['original_created_date'] or transaction_dict['original_created_date'] is pd.NaT:
        transaction_dict['original_created_date'] = datetime.strptime('2000-01-01T00:00:00',format_inter).replace(microsecond=0).isoformat()


    if not transaction_dict['created_at_homologation'] or transaction_dict['created_at_homologation'] is pd.NaT:
        transaction_dict['created_at_homologation'] = datetime.strptime('2000-01-01T00:00:00',format_inter).replace(microsecond=0).isoformat()

    if not item['created_at_head'] or item['created_at_head'] is pd.NaT:
        item['created_at_head'] = datetime.strptime('2000-01-01T00:00:00',format_inter).replace(microsecond=0).isoformat()
        
    if not transaction_dict['classified_at']:
        transaction_dict['classified_at'] = datetime.strptime('2000-01-01T00:00:00',format_inter).replace(microsecond=0).isoformat()

    if not transaction_dict['updated_at']:
        transaction_dict['updated_at'] = datetime.strptime('2000-01-01T00:00:00',format_inter).replace(microsecond=0).isoformat()
        
        
    if not transaction_dict['created_at']:
        transaction_dict['created_at'] = datetime.strptime('2000-01-01T00:00:00',format_inter).replace(microsecond=0).isoformat()
        
        
    if not  transaction_dict['message_type'] :
        transaction_dict['message_type'] = 'NO_FOUND'
    # print("transaction_dict['created_at']:::::::::::::", transaction_dict['created_at'])
    # if transaction_dict['created_at'] is pd.NaT:
    #    print("siiiiiii")
   

    keys = Transaction_().get().keys()

    rm_list = list()
    for key in transaction_dict.keys():
        if not key in keys:
            #print("No key : ", key)
            rm_list.append(key)

    for key in rm_list:
        del transaction_dict[key]

    # if message['type'] == 'report-expense-created':
    MongoDB.get_con_collect(collection_name = 'fact',db_name="klopp")
    
    
    user_dict = None
    # new user ?
    #if not MongoDB.exist('user_uid',item['user_uid']):
    user_dict ={"user_uid":item['user_uid'],
                "postcode":None
                }
    
    if not 'account_uid' in item:
        item['account_uid'] = '123'
    
    if item['account_uid'] is None:
        item['account_uid'] = '123'

    account_dict ={
                    'account_uid': item['account_uid'],
                    'bank_name':  item['bank_name'],
                    'account_type': item['account_type'],
                    'bank_type': item['bank_type']
                    }
    RedShift.insert_dim_user(dict_values = user_dict)
    RedShift.insert_dim_account(dict_values = account_dict)
    
    print("****************************************\n")
    print(account_dict)
    print("****************************************\n")
    print(user_dict)
    print("****************************************\n")
    print(transaction_dict)
    print("****************************************\n")


    date_dict = RedShift.date_decomposition(str(item['created_at_head']).replace(" ","T").split(".")[0])
    table_name = 'dim_dates'
    column_name = 'transaction_date'

    if not RedShift.exists(table_name,column_name ,value = str(date_dict['transaction_date']) ):
        RedShift.insert_dim_dates(dict_values = date_dict)


    fact_transactions_dict = dict ()
    fact_transactions_dict['transaction_date'] = str(date_dict['transaction_date'])
    fact_transactions_dict['transaction_uid'] = item['transaction_uid']
    fact_transactions_dict['user_uid'] = item['user_uid']
    fact_transactions_dict['account_uid'] = item['account_uid']
    fact_transactions_dict['amount'] = item['amount']


 
    print("\nfact_transactions_dict: ")
    print(fact_transactions_dict)
    print("----------------------------------------------")

    # Validación o updated de una transacción 
    # poner la bandera de Categorización automática
    RedShift.insert_dim_transaction(dict_values = transaction_dict)

    RedShift.insert_fact_transactions(dict_values = fact_transactions_dict)
