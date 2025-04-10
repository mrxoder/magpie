import json
import os

DATABASE_FILE = './data/database.json'

class DB:
    def __init__(self, db_file=DATABASE_FILE ):
        self.db_file = db_file
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({}, f)
    
    def _read_db(self):
        with open(self.db_file, 'r') as f:
            return json.load(f)
    
    def _write_db(self, data):
        with open(self.db_file, 'w') as f:
            json.dump(data, f)
    
    def create(self, array_k_value):
        data = self._read_db()
        for val_ in array_k_value:
            k = list(val_.keys())[0]
            if k in data:
                continue
            else:
                data[k] = val_[k]
        self._write_db(data)
        return True
    
    def read(self, key):
        data = self._read_db()
        return data.get(key, None)

    def findBy(self, keys):
        data = self._read_db()
        result = []
        for k in keys:
            if k in data.keys():
                result.append( data.get(k) )
        return result
    
    def update(self, k, value ):
        data = self._read_db()
        if not k in data:
            return False
        data[k] = value
        self._write_db(data)
        return True
    
    def delete(self, key):
        data = self._read_db()
        if key in data:
            del data[key]
            self._write_db(data)
            return True
        return False
    
    def get_all(self):
        return self._read_db()


