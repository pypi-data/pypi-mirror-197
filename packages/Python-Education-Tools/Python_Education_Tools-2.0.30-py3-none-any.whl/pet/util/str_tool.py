import re
from functools import  reduce
'''
s='他的基础工资123.45元，加班234.56元，奖金56.77元，补贴33元！！'
d=re.findall('(\d+\.?\d*)',s)
d=set(d) #去重
table=dict(zip(d,map(lambda x:str(round(float(x)*1.1,2)),d)))
print(table)
print('涨工资前:',s)
s=reduce(lambda x,y:x.replace(y,table[y]),table.keys(),s)
print('涨工资后:',s)
'''


def replace(content,table):
    return reduce(lambda x,y:x.replace(y,table[y]),table.keys(),content)
if __name__ == '__main__':
    s = '他的基础工资123.45元，加班234.56元，奖金56.77元，补贴33元！！'
    d = re.findall('(\d+\.?\d*)', s)
    d = set(d)  # 去重
    table = dict(zip(d, map(lambda x: str(round(float(x) * 1.1, 2)), d)))
    print(table)
    print('涨工资前:', s)
    s = replace(s,table)
    print('涨工资后:', s)