import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
from pypinyin import lazy_pinyin, Style
import re
from scipy.sparse import csc_matrix
from unicodedata import normalize

# == 讀檔 >>> 取代 =========================================================
df = pd.read_csv( input('輸入檔名路徑:') )
name = input('檔案後綴:')
print('...')

df.content = df.content.apply( lambda x: normalize('NFKC', x) ) \
                       .str.lower() \
                       .str.replace(r'[\t\n\r\f\v!?,.]', '\n') \
                       .str.replace( '+'  , '加')\
                       .str.replace(r'[# ]', '') \
                       .str.replace( 'line', '#')\
                       .str.replace(r'[a-z0-9]', '1')

# == 聲母化 >>> 第一份 csv =================================================
def initialization(string, style=Style.BOPOMOFO_FIRST):
    return ''.join(  lazy_pinyin(string, style=style)  )

df['initials'] = df.content.apply(initialization)

feature = pd.DataFrame(df.content.apply(len).values, columns=['len'])

for feat in ['群', 'line']:
    feature[f'{feat}'] = df.content.str.contains(feat).astype(int)

for feat in [ '1{5,}', 'ㄕㄊ', 'ㄐㄨ?ㄌ', 'ㄑㄗ', 'ㄊㄌ', '\(1{3,4}\)' ]:
    feature[f'{feat}'] = df.initials.str.contains(feat).astype(int)
    
feature.to_csv(f'data/feature_{name}.csv', index=False, header=True)

# == 注音化 >>> 第二份 txt =================================================
word = re.compile(r'([ㄅ-ㄩ]+)([ˊˇˋ˙]?)').fullmatch
sent = re.compile(r'(\n+)|(\#)|([ㄅ-ㄩ])|([a-z0-9]+)').finditer  
ZERO = np.zeros(shape=(41,), dtype=np.int32)

def bopomofo2vec(group): 
    vec = ZERO.copy()
    for c in group(1):
        vec[ord(c) - 12549] = 1
    if group(2):
        vec[-2] = 1 + '˙ˊˇˋ'.index(group(2))
    return vec

def sentence_encode(chinese, style=Style.BOPOMOFO):
    seq = [ ZERO ]
    for string in lazy_pinyin(chinese, style=style):
        bopomo_match = word(string)
        if bopomo_match:               # 如果是一組拼音
            seq.append( bopomofo2vec(bopomo_match.group) )
        else:
            for match in sent(string):
                code = ZERO.copy()
                if match.group(1):     # `\n+`   ---> 37
                    code[37] = 1
                elif match.group(2):   # `line` ---> 38
                    code[38] = 1
                elif match.group(3):   # `ㄇ`   --->  3
                    code[ ord(match.group(3)) - 12549] = 1
                else:                  # `a123` --->  4
                    code[-1] = len(match.group(4))
                seq.append( code )
    return csc_matrix(seq)

bopomofo_encoding = list( df.content.apply(sentence_encode) )

with open(f'data/bopomofo_{name}.txt', 'wb') as file:
    pickle.dump(bopomofo_encoding, file)