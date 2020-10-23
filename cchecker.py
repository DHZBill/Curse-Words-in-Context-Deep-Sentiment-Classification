import re
import pandas as pd
import math

#default regex for 'fuck'
reg_exp = '[\S]*f+u+c+k+[\S]*'
csv_file = 'curse-words-list.csv'
df_orig = pd.read_csv(csv_file)
df_reg = df_orig.copy()


'''
function to create regex for a given curse word
'''
def create_regex(cword='fuck'):
    if isinstance(cword, str):
        return str('[\S]*' + '+'.join(cword[i:i + 1] for i in range(0, len(cword))) + '[\S]*')
    else:
        return ''

'''
apply create_regex to every single element of df_reg, data frame for all curse words
'''
df_reg = df_reg.applymap(create_regex)

#sanity check
#print(df_reg)

'''
checks data frame of all regexes for curse words to see if token is a curse word
'''
def is_curse_word(token='', category='general', cwords=df_reg):
    for i in df_reg[category]:
        if len(i) == 0:
            break
        elif re.match(i, token):
            return True
    return False

print(is_curse_word(token='ass'))

'''
Sanity check
print(re.findall(reg_exp, "motherfucker!!!!!"))
'''
