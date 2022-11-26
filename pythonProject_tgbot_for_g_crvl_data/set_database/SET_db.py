import sqlite3
import json
from data_db_class import add_to_data


db = add_to_data('Cripto_base.db')
name_db = db.name.name_db_table_users


class Connection_to_DB:
    def __init__(self):
        self.conn = sqlite3.connect(name_db)
        self.cursor = self.conn.cursor()


    def reg(self, name, email, pass_, user_id):
        try:
            id_check = self.cursor.execute('SELECT `user_id` FROM `Cripto_users` WHERE `user_e-mail` = ?',(email,))
            user_id_check = [i for i in id_check]
            try:
                if user_id_check[0][0] == user_id:
                    print('<-- [You] are registered already!!! -->')
                else:
                    raise KeyError
            except:
                self.cursor.execute('INSERT INTO `Cripto_users` (`user_name`, `user_e-mail`, `user_pass`, `user_id`) VALUES (?,?,?,?)',(name, email, pass_, user_id))
                self.conn.commit()
                print('The table was provide data is successfully!!!')
        except Exception as ex:
            print('[14] -- <-- db table data is not correct  -->' + str(ex))


class Set_Table:
    def __init__(self,table_name):
        self.table_name = table_name
        self.conn = sqlite3.connect(name_db)
        self.cursor = self.conn.cursor()


    def add(self,user_id, *args, **kwargs:dict):
        try:
            attr = list('`' + i + '`' for i in args)
            values = list(kwargs.get(i) for i in args)
            values.insert(0,str(user_id))

            t = ','.join(attr)
            s = '?,'*len(values)

            self.cursor.execute(f'INSERT INTO `{self.table_name}` (`user_id`,{t}) VALUES ({s[:-1]})', values)
            self.conn.commit()
            self.conn.executemany()

            print(f'<--- [DATA]({values}) has added and commited successfully!!! --->')
        except Exception as ex:
            print('<--- [28] DATA is not correct or has been existing!!! ---> ' + str(ex))


    def select_from_db(self, user_id:int, key:str):
        return self.conn.execute(f'SELECT `{key}` FROM `{self.table_name}` WHERE `user_id` = ?', (user_id,)).fetchall()


    def select_to_json(self, user_id, *args:str, file_name='data_db.json') -> list:
        data_dict = {}
        data_list = []
        user_name = self.conn.execute(f'SELECT `user_name` FROM `{self.table_name}` WHERE `user_id` = ?', (user_id,)).fetchone()[0]
        data_dict[user_name] = {}

        for i in args:
            try:
                data = self.conn.execute(f'SELECT `{i}` FROM `{self.table_name}` WHERE `user_id` = ?', (user_id,)).fetchone()[0]
                data_dict[user_name][i] = data
                data_list.append(data)
            except Exception as ex:
                print('<-- [37] DATA is not correct!!! -->' + str(ex))
                break

        with open(file_name, 'w') as file:
            json.dump(data_dict, file, indent=4)
            print('[DATA] is coommiting successfully!!!')

        return data_list


    def select_from_json(self, file_path:str, key:str, *args) -> list:
        try:
            with open(file_path, 'r') as file:
                s = json.load(file)
        except Exception as ex:
            print('[DATA] <----- File path is not defind!!! ----->')
        return [s[key][i] for i in args]


    def chek_in(self, key:str, user_id:int) -> bool:
        return bool(self.conn.execute(f'SELECT `{key}` FROM `{self.table_name}` WHERE `user_id` = ?', (user_id,)).fetchone())


if __name__=='__main__':
    conn = Connection_to_DB()
    #conn.reg('kiria2', 'nayt116@bk.ru', 'qwert1233234', 1232324000)
    set_tb = Set_Table('Admin_users')
    d = {
        'e-mail': 'some_email@gmail.com',
    }
    #set_tb.add(13516446500, *d.keys(), **d)
    #set_tb.select_to_json(1232324000, 'user_name', 'user_pass', 'user_e-mail')
    #set_tb.select_from_json('data_db.json', 'Oleg', 'user_name', 'user_pass', 'user_e-mail', 'user_datetime_reg')
    #print(set_tb.select_from_db('user_name', 13516446500))
    #print(set_tb.chek_in('user_id', 13516446500))