class string(str):
    def rep(self,substring):
        self = string(self.replace(substring,''))
        return self

    def repsies(self,*args):
        for arg in args:
            self = self.rep(arg)
        return self

    def ad(self, value):
        self = string(self + getattr(self, 'delim', "")  + value)
        return self

    def delim(self, value):
        self.delim = value

    def pre(self, value):
        self = string(value + getattr(self, 'delim', "")  + self)
        return self

    def pres(self, *args):
        for arg in args:
            self = self.pre(arg)
        return self

    @property
    def empty(self):
        return self is None or self.strip() == '' or self.strip().lower() == 'nan'

    @property
    def notempty(self):
        return not self.empty

    def format(self, numstyle='06'):
        return format(int(self),numstyle)

    def splitsies(self,*args,joiner=":"):
        output_list = []
        for splitter_itr, splitter in enumerate(args):
            if splitter_itr == 0:
                output_list = self.split(splitter)
            else:
                temp_list = string(joiner.join(output_list)).splitsies(splitter,joiner=joiner)
                output_list = []
                for temp_item in temp_list:
                    for temp_split_item in temp_item.split(joiner):
                        output_list.append(temp_split_item)

        return output_list

    def tohash(self, hash_type='sha512', encoding='utf-8'):
        import hashlib
        return getattr(hashlib, hash_type)(self.encode(encoding)).hexdigest()

    def tobase64(self, encoding='utf-8'):
        import base64
        return base64.b64encode(self.encode(encoding)).decode(encoding)

    @staticmethod
    def frombase64(string, encoding='utf-8'):
        import base64
        return base64.b64decode(string.encode(encoding)).decode(encoding)

import pandas as pd
class frame(pd.DataFrame):
    def __init__(self,*args,**kwargs):
        super(frame,self).__init__(*args,**kwargs)
    def col_exists(self,column):
        return column in self.columns

    def col_no_exists(self,column):
        return not(self.col_exists(column))

    def column_decimal_to_percent(self,column):
        self[column] = round(round(
            (self[column]),2
        ) * 100,0).astype(int).astype(str).replace('.0','') + "%"

    def move_column(self, column, position):
        if self.col_no_exists(column):
            return
        colz = [col for col in self.columns if col != column]
        colz.insert(position, column)
        self = frame(self[colz])

    def rename_column(self, columnfrom, columnto):
        if self.col_no_exists(columnfrom):
            return
        self.rename(columns={columnfrom: columnto},inplace=True)

    def rename_value_in_column(self, column, fromname, fromto):
        if self.col_no_exists(column):
            return
        self[column] = self[column].str.replace(fromname, fromto)
 
    def arr(self):
        self_arr = self.to_dict('records')
        return self_arr

    def add_confusion_matrix(self,TP:str='TP',FP:str='FP',TN:str='TN',FN:str='FN', use_percent:bool=False):
        prep = lambda x:frame.percent(x, 100) if use_percent else x

        self['Precision_PPV'] = prep(self[TP]/(self[TP]+self[FP]))
        self['Recall'] = prep(self[TP]/(self[TP]+self[FN]))
        self['Specificity_TNR'] = prep(self[TN]/(self[TN]+self[FP]))
        self['FNR'] = prep(self[FN]/(self[FN]+self[TP]))
        self['FPR'] = prep(self[FP]/(self[FP]+self[TN]))
        self['FDR'] = prep(self[FP]/(self[FP]+self[TP]))
        self['FOR'] = prep(self[FN]/(self[FN]+self[TN]))
        self['TS'] = prep(self[TP]/(self[TP]+self[FP]+self[FN]))
        self['Accuracy'] = prep((self[TP]+self[TN])/(self[TP]+self[FP]+self[TN]+self[FN]))
        self['PPCR'] = prep((self[TP]+self[FP])/(self[TP]+self[FP]+self[TN]+self[FN]))
        self['F1'] = prep(2 * ((self['Precision_PPV'] * self['Recall'])/(self['Precision_PPV'] + self['Recall'])))

        return self

    @staticmethod
    def percent(x,y):
        return ("{0:.2f}").format(100 * (x / float(y)))

    @staticmethod
    def from_json(string):
        return frame(pd.read_json(string))

    @staticmethod
    def from_arr(arr):
        def dictionaries_to_pandas_helper(raw_dyct,deepcopy:bool=True):
            from copy import deepcopy as dc
            dyct = dc(raw_dyct) if deepcopy else raw_dyct
            for key in list(raw_dyct.keys()):
                dyct[key] = [dyct[key]]
            return pd.DataFrame.from_dict(dyct)

        return frame(
            pd.concat( list(map( dictionaries_to_pandas_helper,arr )), ignore_index=True )
        )

    @property
    def roll(self):
        self.current_index=0
        while self.current_index < self.shape[0]:
            x = self.iloc[self.current_index]
            self.current_index += 1
            yield x

    def tobase64(self, encoding='utf-8'):
        import base64
        return base64.b64encode(self.to_json().encode(encoding)).decode(encoding)

    @staticmethod
    def frombase64(string, encoding='utf-8'):
        import base64
        return frame.from_json(base64.b64decode(string.encode(encoding)).decode(encoding))
