import json
import os

DATABASE_FILENAME = 'db00000'
DATABASE_PART     = 'part00000'
DATABASE_PATH     =  os.path.dirname( os.path.abspath(__file__) ) + '/../data/'
FILE_DIRECTORY    =  DATABASE_PATH + "files/"
LIMIT_PER_PART    =  100
DATABASE_PART_IDX     = 'part00000.idx'

class JSONFILE:
    def __init__(self, db_file, default_data={}):
        self.db_file = db_file
        self._ensure_db_exists( default_data )
    
    def _ensure_db_exists(self, default_data={}):
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump(default_data, f)
    
    def _read_db(self):
        with open(self.db_file, 'r') as f:
            return json.load(f)
    
    def _write_db(self, data):
        with open(self.db_file, 'w') as f:
            json.dump(data, f)

class JSONDB:
    def __init__(self):
        self.part_file_ = JSONFILE( DATABASE_PATH + DATABASE_PART, { 'last':0, '0': [] } )
        self.part_idx_file_ = JSONFILE( DATABASE_PATH + DATABASE_PART_IDX )
        self.part_file_content = self.part_file_._read_db()
        self.part_indexes = self.part_idx_file_._read_db()

    def _update_part( self ):
        self.part_file_._write_db( self.part_file_content )
        self.part_idx_file_._write_db( self.part_indexes )

    def create( self, array_k_value, overwrite=False ):
        last_part = self.part_file_content['last']
        current_part_file = JSONFILE( DATABASE_PATH + DATABASE_FILENAME + str(last_part) )
        current_part_content = current_part_file._read_db()

        update_part = False
        for val_ in array_k_value:
            while len( current_part_content.keys() ) >= LIMIT_PER_PART:
                if update_part:
                   current_part_file._write_db( current_part_content )
                   update_part = False

                last_part = int(last_part) + 1
                self.part_file_content['last'] = last_part 
                current_part_file = JSONFILE( DATABASE_PATH + DATABASE_FILENAME + str(last_part) )
                current_part_content = current_part_file._read_db()
                
                if not str(last_part) in self.part_file_content.keys():
                   self.part_file_content[ str(last_part) ] = []

            k = list(val_.keys())[0]
            if k in self.part_indexes.keys():
                if overwrite:
                    tmp_part_file = JSONFILE( DATABASE_PATH + DATABASE_FILENAME + str(self.part_indexes[k]) )
                    tmp_part_content = tmp_part_file._read_db()
                    tmp_part_content[k] = val_[k]
                    tmp_part_file._write_db( tmp_part_content )
                else:
                    continue
            else:
                current_part_content[k] = val_[k]
                self.part_indexes[k] = str( last_part )
                self.part_file_content[str( last_part )].append( k )
                update_part = True

        if update_part:
            current_part_file._write_db( current_part_content )

        self._update_part()

    def get( self, key ):
        if key in self.part_indexes.keys():
            tmp_part_file = JSONFILE( DATABASE_PATH + DATABASE_FILENAME + str(self.part_indexes[key]) )
            tmp_part_content = tmp_part_file._read_db()
            return tmp_part_content[ key ]
        else:
            return None
    
    def count_data( self ):
        last = int(self.part_file_content['last']) + 1
        total = 0
        for i in range(last):
            tmp_part_file = JSONFILE( DATABASE_PATH + DATABASE_FILENAME + str(i) )
            tmp_part_content = tmp_part_file._read_db()
            total += len( tmp_part_content.keys() )

        return total

    def allKeys( self ):
        idx = self.part_indexes
        return idx

    def delete( self, key ):
        if key in self.part_indexes.keys():
            tmp_part_file = JSONFILE( DATABASE_PATH + DATABASE_FILENAME + str(self.part_indexes[key]) )
            tmp_part_content = tmp_part_file._read_db()

            del tmp_part_content[ key ]

            part_n = self.part_indexes[key]
            self.part_file_content[ str(part_n) ].pop( self.part_file_content[ str( part_n ) ].index(key) )

            del self.part_indexes[ key ]

            #flush
            tmp_part_file._write_db( tmp_part_content )
            self.part_file_._write_db( self.part_file_content )
            self.part_idx_file_._write_db( self.part_indexes )

            return True
        else:
            return False
    
    def update( self, array_k_value ):
        classified = {}
        for row in array_k_value:
            key = list(row.keys())[0]
            if not key in self.part_indexes.keys():
                continue

            part_ = str(self.part_indexes[key])
            if part_ in classified.keys():
                classified[ part_ ].append( row )
            else:
                classified[ part_ ] = [ row ]

        for i in classified.keys():
            tmp_part_file = JSONFILE( DATABASE_PATH + DATABASE_FILENAME + str(self.part_indexes[key]) )
            tmp_part_content = tmp_part_file._read_db()

            for row in classified[i]:
                key = list(row.keys())[0]
                value = row[key]
                tmp_part_content[ key ] = value

            tmp_part_file._write_db( tmp_part_content )
