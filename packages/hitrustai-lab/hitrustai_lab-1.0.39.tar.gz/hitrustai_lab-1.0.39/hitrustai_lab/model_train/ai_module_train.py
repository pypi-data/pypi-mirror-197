import os
import re
import json
import time
import datetime
import pandas as pd
import numpy as np
from decouple import AutoConfig
from sqlalchemy import Column, text, Integer
from sqlalchemy.dialects.mysql import TIMESTAMP

from hitrustai_lab.model_train.core.utils import decrypt_passwd
from hitrustai_lab.apollo.apollo_client import ApolloClient
from hitrustai_lab.apollo.util import check_apollo_change, get_apollo_value

from hitrustai_lab.matrix.model_performance import ModelPerfornance
from hitrustai_lab.orm import Orm, get_orm_profile
from hitrustai_lab.orm.Tables.ModelPerformance import create_model_performance, Base_Model


dict_init_arg = {
    "list_y_test": list,
    "list_y_score": np.array,
    "customer_id_lst": str,
    "training_id_lst": str,
    "model_id_lst": str,
    "profile_id_lst": str,
    "tag_lst": str,
    "training_start_time_lst": str,
    "total_training_time_lst": int,
    "training_start_time_lst": datetime,
    "training_end_time_lst": datetime,
    "number_of_dump_data": int,
    "number_of_training_data": int,
    "number_of_positive_samples_in_training_data": int,
    "number_of_negative_samples_in_training_data": int,
    "number_of_validation_data": int,
    "true_label_column_lst": str,
    "number_of_positive_samples_in_validation_data": int,
    "number_of_negative_samples_in_validation_data": int,
    "return_code": str,
    "reason": str
}


class TrainModelToSQl:
    def __init__(self, host="192.168.10.102", port="3305", user="root", passwd="root16313302", db="diia_test", table_name="int") -> None:
        self.table_name = table_name
        self.orm_profile = get_orm_profile(host=host, port=port, db=db, user=user, pwd=passwd)
        self.orm = Orm(profile=self.orm_profile)

    def performance(self, dict_init_arg: dict):
        mp = ModelPerfornance(score_type='policy_score')
        try:
            result = mp.performance_output(dict_init_arg["list_y_test"], dict_init_arg["list_y_score"])
            result = {
                'customer_id': dict_init_arg["customer_id_lst"],
                'training_id': dict_init_arg["training_id_lst"],
                'model_id': dict_init_arg["model_id_lst"],
                'profile_id': dict_init_arg["profile_id_lst"],
                'tag': dict_init_arg["tag_lst"],
                'model_name': dict_init_arg["model_id_lst"] + "-" + "".join(re.findall(r'\d+', str(datetime.datetime.now()))),
                'training_start_time': dict_init_arg["training_start_time_lst"],
                'training_end_time': dict_init_arg["training_end_time_lst"],
                'total_training_time': dict_init_arg["total_training_time_lst"],
                'training_data_start_date': dict_init_arg["training_data_start_date"],
                'training_data_end_date': dict_init_arg["training_data_end_date"],
                'number_of_dump_data': dict_init_arg["number_of_dump_data"],
                'number_of_training_data': dict_init_arg["number_of_training_data"],
                'number_of_positive_samples_in_training_data': dict_init_arg["number_of_positive_samples_in_training_data"],
                'number_of_negative_samples_in_training_data': dict_init_arg["number_of_negative_samples_in_training_data"],
                'number_of_validation_data': dict_init_arg["number_of_validation_data"],
                'true_label_column': dict_init_arg["true_label_column_lst"],
                'number_of_positive_samples_in_validation_data': dict_init_arg["number_of_positive_samples_in_validation_data"],
                'number_of_negative_samples_in_validation_data': dict_init_arg["number_of_negative_samples_in_validation_data"],
                'threshold': [result['threshold_lst']],
                'tp': [result['tp_lst']],
                'fp': [result['fp_lst']],
                'tn': [result['tn_lst']],
                'fn': [result['fn_lst']],
                'accuracy': [result['accuracy_lst']],
                'ppv': [result['precision_lst']],
                'recall': [result['recall_lst']],
                'f1_score': [result['f1_score_lst']],
                'fnr': [result['fnr_lst']],
                'fpr': [result['fpr_lst']],
                'npv': [result['npv_lst']],
                'fdr': [result['fdr_lst']],
                'for_': [result['for_lst']],
                'tnr': [result['tnr_lst']],
                'auc': result['auc_lst'],
                "return_code": dict_init_arg['return_code'],
                "reason": dict_init_arg['reason']
            }
        except Exception:
            result = {
                'customer_id': dict_init_arg["customer_id_lst"],
                'training_id': dict_init_arg["training_id_lst"],
                'model_id': dict_init_arg["model_id_lst"],
                'profile_id': dict_init_arg["profile_id_lst"],
                'tag': dict_init_arg["tag_lst"],
                'model_name': dict_init_arg["model_id_lst"] + "-" + "".join(re.findall(r'\d+', str(datetime.datetime.now()))),
                'training_start_time': "2000-01-01 00:00:00",
                'training_end_time': "2000-01-01 00:00:00",
                'total_training_time': -1,
                'training_data_start_date': "2000-01-01 00:00:00",
                'training_data_end_date': "2000-01-01 00:00:00",
                'number_of_dump_data': -1,
                'number_of_training_data': -1,
                'number_of_positive_samples_in_training_data': -1,
                'number_of_negative_samples_in_training_data': -1,
                'number_of_validation_data': -1,
                'true_label_column': dict_init_arg["true_label_column_lst"],
                'number_of_positive_samples_in_validation_data': -1,
                'number_of_negative_samples_in_validation_data': -1,
                'threshold': [[]],
                'tp': [[]],
                'fp': [[]],
                'tn': [[]],
                'fn': [[]],
                'accuracy': [[]],
                'ppv': [[]],
                'recall': [[]],
                'f1_score': [[]],
                'fnr': [[]],
                'fpr': [[]],
                'npv': [[]],
                'fdr': [[]],
                'for_': [[]],
                'tnr': [[]],
                'auc': [[]],
                "return_code": dict_init_arg['return_code'],
                "reason": dict_init_arg['reason']
            }   
        return result

    def dict_to_dataframe(self, dict_init_arg: dict, dict_add_column=None):
        self.need_column = self.performance(dict_init_arg)
        if dict_add_column is not None:
            for key in dict_add_column:
                self.need_column[key] = dict_init_arg[key]
        
        df = pd.DataFrame(data=self.need_column)
        df['total_training_time'] = df.total_training_time
        df['training_data_start_date'] = df.training_data_start_date
        df['training_data_end_date'] = df.training_data_end_date

        for col in [
            'threshold', 'tp', 'fp', 'tn', 'fn', 'accuracy', 'ppv', 'recall', 'f1_score',
            'fnr', 'fpr', 'npv', 'fdr', 'for_', 'tnr'
        ]:
            df[col] = df[col].apply(lambda x: json.dumps(x))

        return df

    def insert_db(self, data: dict, dict_add_column=None):
        # if not data:
        #     return
        base_table = create_model_performance(self.table_name)
        if dict_add_column is not None:
            for key in dict_add_column:
                base_table.append_column(dict_add_column[key])
        base_table.append_column(Column("create_time", TIMESTAMP(fsp=6), nullable=False, server_default=text("CURRENT_TIMESTAMP(6)")))
        
        class User(Base_Model):
            __table__ = base_table
        self.orm.create_table(Base_Model, User)
        
        data = self.dict_to_dataframe(data, dict_add_column)
        
        self.orm.data_to_DB(data, User)


class GetConfArg:
    def read_train_conf_env(self):
        config = AutoConfig(search_path=os.getcwd() + "/env")
        # check docker environment exist
        CUSTOMER_ID = os.environ.get('CUSTOMER_ID')
        MODEL_ID = os.environ.get('MODEL_ID')
        TRAINING_ID = os.environ.get('TRAINING_ID')
        KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')

        # check service .env file exist
        kafka_node = config('KAFKA_N', default='0')
        bootstrap_servers = []
        for i in range(int(kafka_node)):
            host = config('KAFKA_HOST_' + str(i + 1), default='')
            port = config('KAFKA_PORT_' + str(i + 1), default='')
            if host == "" or port == "":
                self.init_logger.error('Error: Invalid variable in env. Expected keys [KAFKA_HOST, KAFKA_PORT]')
                os.kill(0, 4)
            bootstrap_servers.append(host + ":" + port)

        self.appollo_info = {
            "servers": bootstrap_servers,
            "customer_id": CUSTOMER_ID,
            "model_id": MODEL_ID,
            "training_id": TRAINING_ID,
            "topic": KAFKA_TOPIC,
            "BATCH_SIZE": int(config('Chunksize', default='100000')),
            "dataset_path": config('SOURCE_PATH_DATASET', default=''),
            "kg_path": config('SOURCE_PATH_KNOWLEDGE', default=''),
            "lib_path": config('SOURCE_PATH_LIB', default=''),
            "KAFKA_USE": config('KAFKA_USE', default=''),
        }

        db_pass = config('DB_PASS', default='')
        password = decrypt_passwd(self.passwd_so_name, db_pass)
        self.SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            config('DB_ENGINE', default='mysql+pymysql'),
            config('DB_USERNAME', default='test'),
            password,
            config('DB_HOST', default='127.0.0.1'),
            config('DB_PORT', default=3306),
            config('DB_NAME', default='testdb')
        )

    def read_train_conf_apollo(self):
        config = AutoConfig(search_path=os.getcwd() + "/env")
        try:
            APOLLO_URL = config('APOLLO_URL')
            APOLLO_APPID = config('APOLLO_APPID')
            APOLLO_CLUSTER = config('APOLLO_CLUSTER')
            APOLLO_SECRET = config('APOLLO_SECRET')
            APOLLO_NAMESPACE_INF = config('APOLLO_NAMESPACE_INF')
            APOLLO_NAMESPACE_MODAL = config('APOLLO_NAMESPACE_MODAL')
        except Exception:
            os.kill(0, 4)
        apollo_client = ApolloClient(
            app_id=APOLLO_APPID,
            cluster=APOLLO_CLUSTER,
            config_url=APOLLO_URL,
            secret=APOLLO_SECRET,
            change_listener=check_apollo_change)

        # check service .env file exist
        KAFKA_N = get_apollo_value(apollo_client, "KAFKA_NODE", APOLLO_NAMESPACE_INF)
        KAFKA_N = KAFKA_N.split(",")
        # kafka_node = len(KAFKA_N)
        bootstrap_servers = []
        for ip in KAFKA_N:
            host, port = ip.split(":")
            if host == "" or port == "":
                self.init_logger.error('Error: Invalid variable in env. Expected keys [KAFKA_HOST, KAFKA_PORT]')
                os.kill(0, 4)
            bootstrap_servers.append(host + ":" + port)
        db_pass = get_apollo_value(apollo_client, "DB_PASS", APOLLO_NAMESPACE_INF)

        password = decrypt_passwd(self.passwd_so_name, db_pass)
        self.SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
            get_apollo_value(apollo_client, "DB_ENGINE", APOLLO_NAMESPACE_INF),
            get_apollo_value(apollo_client, "DB_USERNAME", APOLLO_NAMESPACE_INF),
            password,
            get_apollo_value(apollo_client, "DB_HOST", APOLLO_NAMESPACE_INF),
            get_apollo_value(apollo_client, "DB_PORT", APOLLO_NAMESPACE_INF),
            get_apollo_value(apollo_client, "DB_NAME", APOLLO_NAMESPACE_INF)
        )
        self.appollo_info = {
            "servers": bootstrap_servers,
            "customer_id": get_apollo_value(apollo_client, "CUSTOMER_ID", APOLLO_NAMESPACE_MODAL),
            "model_id": get_apollo_value(apollo_client, "MODEL_ID", APOLLO_NAMESPACE_MODAL),
            "training_id": get_apollo_value(apollo_client, "TRAINING_ID", APOLLO_NAMESPACE_MODAL),
            "topic": get_apollo_value(apollo_client, "TRAINING_ID", APOLLO_NAMESPACE_MODAL),
            "BATCH_SIZE": int(get_apollo_value(apollo_client, "BATCH_SIZE", APOLLO_NAMESPACE_MODAL)),

            "dataset_path": get_apollo_value(apollo_client, "SOURCE_PATH_DATASET", APOLLO_NAMESPACE_MODAL),
            "kg_path": get_apollo_value(apollo_client, "SOURCE_PATH_KNOWLEDGE", APOLLO_NAMESPACE_MODAL),
            "lib_path": get_apollo_value(apollo_client, "SOURCE_PATH_LIB", APOLLO_NAMESPACE_MODAL),
            # "KAFKA_USE": get_apollo_value(apollo_client, "KAFKA_USE", APOLLO_NAMESPACE_MODAL),
            "DB_ENGINE": get_apollo_value(apollo_client, "DB_ENGINE", APOLLO_NAMESPACE_INF),
            "DB_USERNAME": get_apollo_value(apollo_client, "DB_USERNAME", APOLLO_NAMESPACE_INF),
            "DB_PASS": password,
            "DB_HOST": get_apollo_value(apollo_client, "DB_HOST", APOLLO_NAMESPACE_INF),
            "DB_PORT": get_apollo_value(apollo_client, "DB_PORT", APOLLO_NAMESPACE_INF),
            "DB_NAME": get_apollo_value(apollo_client, "DB_NAME", APOLLO_NAMESPACE_INF)
        }


class HitrustaiTrainTemple(GetConfArg):
    def __init__(self, dict_model, init_logger, passwd_so_name="./data/passwd.so", model_name="fraud detect"):
        self.dict_model = dict_model
        self.init_logger = init_logger
        self.passwd_so_name = passwd_so_name
        self.model_name = model_name
        self.dict_init_arg = None
        self.template_output_txt = '''
=================================================
INFO_MODEL_NAME: %s
INFO_TRAINING_ID : %s
INFO_CUSTOMER_ID: %s
INFO_MODEL_ID: %s
DATA_START_DATE: %s
DATA_END_DATE: %s
DATA_TOTAL_ROW: %s
TRAINING_DATE: %s
TRAINING_TIME: %s
TRAINING_RETURN_CODE : %s
TRAINING_REASON : %s
        '''

    def error_arg_dict(self):
        dict_init_arg = {
            "list_y_test": [],
            # "list_y_score": np.array(self.df["total_score_fd7"]),
            "list_y_score": [],
            "customer_id_lst": self.appollo_info["customer_id"],
            "training_id_lst": self.appollo_info["training_id"],
            "model_id_lst": self.appollo_info["model_id"],
            "profile_id_lst": self.appollo_info["customer_id"],
            "tag_lst": self.appollo_info["customer_id"],
            "training_start_time_lst": self.training_start_time_lst,
            "total_training_time_lst": self.total_training_time_lst,

            "training_data_start_date": self.DATA_START_DATE,
            "training_data_end_date": self.DATA_END_DARE,
            "training_end_time_lst": self.training_end_time_lst,
            "number_of_dump_data": -1,
            "number_of_training_data": -1,
            "number_of_positive_samples_in_training_data": -1,
            "number_of_negative_samples_in_training_data": -1,
            "number_of_validation_data": -1,
            "true_label_column_lst": self.dict_model.true_lable_name,
            "number_of_positive_samples_in_validation_data": -1,
            "number_of_negative_samples_in_validation_data": -1,
            "return_code": self.dict_report["return_code"],
            "reason": self.dict_report["reason"]
        }
        return dict_init_arg

    def input_arg_dict(self):
        """
        dict_init_arg = {
            "list_y_test": list,
            "list_y_score": np.array,
            "customer_id_lst": str,
            "training_id_lst": str,
            "model_id_lst": str,
            "profile_id_lst": str,
            "tag_lst": str,
            "training_start_time_lst": str,
            "total_training_time_lst": int,
            "training_start_time_lst": datetime,
            "training_end_time_lst": datetime,
            "number_of_dump_data": int,
            "number_of_training_data": int,
            "number_of_positive_samples_in_training_data": int,
            "number_of_negative_samples_in_training_data": int,
            "number_of_validation_data": int,
            "true_label_column_lst": str,
            "number_of_positive_samples_in_validation_data": int,
            "number_of_negative_samples_in_validation_data": int,
            "return_code": str,
            "reason": str
        }
        """
        
        dict_init_arg = {
            "list_y_test": list(self.dict_model.df[self.dict_model.true_lable_name]),
            # "list_y_score": np.array(self.df["total_score_fd7"]),
            "list_y_score": np.array,
            "customer_id_lst": self.appollo_info["customer_id"],
            "training_id_lst": self.appollo_info["training_id"],
            "model_id_lst": self.appollo_info["model_id"],
            "profile_id_lst": self.appollo_info["customer_id"],
            "tag_lst": self.appollo_info["customer_id"],
            "training_start_time_lst": self.training_start_time_lst,
            "total_training_time_lst": self.total_training_time_lst,

            "training_data_start_date": self.DATA_START_DATE,
            "training_data_end_date": self.DATA_END_DARE,
            "training_end_time_lst": self.training_end_time_lst,
            "number_of_dump_data": self.dict_model.DATA_TOTAL_ROW,
            "number_of_training_data": self.dict_model.DATA_TOTAL_ROW_TRAIN,
            "number_of_positive_samples_in_training_data": self.dict_model.VAL_POSITION_NUMBER,
            "number_of_negative_samples_in_training_data": self.dict_model.VAL_POSITION_NEGATIVE,
            "number_of_validation_data": self.dict_model.DATA_TOTAL_ROW_VAL,
            "true_label_column_lst": self.dict_model.true_lable_name,
            "number_of_positive_samples_in_validation_data": self.dict_model.VAL_POSITION_NUMBER_VAL,
            "number_of_negative_samples_in_validation_data": self.dict_model.VAL_POSITION_NEGATIVE_VAL,
            "return_code": self.dict_report["return_code"],
            "reason": self.dict_report["reason"]
        }
        return dict_init_arg

    def train(self):
        try:
            config = AutoConfig(search_path=os.getcwd() + "/env")
            if config('ENV_METHOD') == "env":
                self.read_train_conf_env()
            else:
                self.read_train_conf_apollo()
            t1 = time.time()
            self.training_start_time_lst = datetime.datetime.now()
            self.dict_report = self.dict_model.train()
            self.total_training_time_lst = time.time() - t1
            self.training_end_time_lst = datetime.datetime.now()
            self.DATA_START_DATE = self.dict_model.DATA_START_DATE
            self.DATA_END_DARE = self.dict_model.DATA_END_DARE
            self.DATA_TOTAL_ROW = self.dict_model.DATA_TOTAL_ROW

            self.dict_init_arg = self.input_arg_dict()

        except Exception as e:
            self.training_start_time_lst = "2000-01-01 00:00:00"
            self.total_training_time_lst = -1
            self.training_end_time_lst = "2000-01-01 00:00:00"
            self.DATA_START_DATE = "2000-01-01 00:00:00"
            self.DATA_END_DARE = "2000-01-01 00:00:00"
            self.DATA_TOTAL_ROW = -1
            
            self.dict_init_arg = self.error_arg_dict()
            self.dict_init_arg["reason"] = e.args[0]
            if self.dict_report["return_code"] == "4001":
                self.dict_init_arg["return_code"] = "9914"

    def insert_db(self, table_name, dict_add_column=None):
        tmts = TrainModelToSQl(
            host=self.appollo_info["DB_HOST"],
            port=self.appollo_info["DB_PORT"],
            user=self.appollo_info["DB_USERNAME"],
            passwd=self.appollo_info["DB_PASS"],
            db=self.appollo_info["DB_NAME"],
            table_name=table_name
        )
        tmts.insert_db(data=self.dict_init_arg, dict_add_column=dict_add_column)

    def output_txt(self, model_name="Fraud Detect", path='./data/lib/output.txt'):
        output_txt = self.template_output_txt % (
            model_name,
            self.dict_init_arg["training_id_lst"],
            self.dict_init_arg["customer_id_lst"],
            self.dict_init_arg["model_id_lst"],
            self.dict_init_arg["training_data_start_date"],
            self.dict_init_arg["training_data_end_date"],
            self.dict_init_arg["number_of_dump_data"],
            self.dict_init_arg["training_start_time_lst"],
            self.dict_init_arg["total_training_time_lst"],
            self.dict_init_arg["return_code"],
            self.dict_init_arg["reason"],
        )
        with open(path, 'a') as f:
            f.write(output_txt + "\n")
        

if __name__ == '__main__':
    from hitrustai_lab.model_train.ai_module_train import TrainModelToSQl
    dict_add_column = {
        "add_column1": Column("add_column1", Integer, primary_key=True),
        "add_column2": Column("add_column2", Integer, primary_key=True)
    }

    tmts = TrainModelToSQl(
        host="192.168.10.203",
        port="3305",
        user="diia",
        passwd="diia16313302",
        db="service_report",
        table_name="test111111"
    )

    tmts.insert_db(data=dict_init_arg, dict_add_column=dict_add_column)
