"""
Message sending channel abstract class
"""
import os
import sqlite3
import time
import csv

class bot(object):
    def startup(self):
        """
        init channel
        """
        raise NotImplementedError

    def handle(self, msg):
        """
        process received msg
        :param msg: message object
        """
        raise NotImplementedError

    def send(self, msg, receiver):
        """
        send message to user
        :param msg: message content
        :param receiver: receiver channel account
        :return:
        """
        raise NotImplementedError

    def put_in_db_from_group(self, query):
        print('receive group handler, query is:', query)
        try:
            db_Path = os.path.dirname(os.getcwd()) + '\wechat-auto\db\Eqp_test.db'
            #print('db_Path:', db_Path)
            db_Path = db_Path.replace('\\', '/')
            #print('db_Path:', db_Path)
            conn = sqlite3.connect(db_Path)
            cur = conn.cursor()
            #print('db connected:', db_Path)
        except Exception as e:
            print(e)
        try:
            create_tb_cmd = '''
            CREATE TABLE IF NOT EXISTS eqp_trace_log
            (EqpID varchar(64),
            Event varchar(64),
            RecordMan varchar(64),
            RecordTime varchar(64),
            RecordIndex varchar(64));
            '''
            cur.execute(create_tb_cmd)
            #print("Create table succeed")
        except:
            #print("Create table failed")
            return "404"
        data = str(query).split("＃")
        #print('data 1:', data)
        data[2] = data[2][4:]
        #print('data 2:', data)
        data[3] = data[3][3:]
        #print('data 3:', data)
        data.append(time.time())
        print('data ready:', data)
        insert_tb_cmd = '''insert into eqp_trace_log(EqpID, Event, RecordMan, RecordTime, RecordIndex)
        values (?,?,?,?,?);'''
        cur.execute(insert_tb_cmd, (data[0], data[1], data[2], data[3], data[4]))
        conn.commit()
        #select_tb_cmd = '''select * from eqp_trace_log'''
        #results = cur.execute(select_tb_cmd)
        #all_logs = results.fetchall()
        #for log in all_logs:
        #    print(log)
        conn.close()
        print('data put in finished:', data[4])
        return str(data[4])

    def read_db(self):
        try:
            db_Path = os.path.dirname(os.getcwd()) + '\wechat-auto\db\Eqp_test.db'
            xls_Path = os.path.dirname(os.getcwd()) + '\wechat-auto\export\Eqp_export.csv'
            conn = sqlite3.connect(db_Path)
            cur = conn.cursor()
            cur.execute('select * from eqp_trace_log')
            with open(xls_Path, 'w', newline='') as out_csv_file:
                csv_out = csv.writer(out_csv_file)
                # write header
                csv_out.writerow([d[0] for d in cur.description])
                # write data
                for result in cur:
                    csv_out.writerow(result)
            print('csv ready')
            cur.close()
            return xls_Path
        except Exception as e:
            print(e)
            return "404"