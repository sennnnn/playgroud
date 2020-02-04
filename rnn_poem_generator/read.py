import os
import time

from util import Tokenizer,write_dict
from collections import Counter

data_raw = "dataset/poetry.txt"

vocabulary_data_path = "dataset/vocabulary_list.txt"

vocabulary_vector_data_path = "dataset/vocabulary_vector_list.txt"

error_char = ['(',')','（','）','<','>','《','》','_','[',']','【','】']  # 禁用词汇

min_word_frequency = 8

max_sentence_length = 100

min_sentence_length = 20

# 数据集读取，一行就是一首诗
records = open(data_raw,"r",encoding='utf-8')
poems = records.readlines()
poems = [line.replace('：',':') for line in poems]

def word_to_id(word, id_dict):
    if word in id_dict.keys():
        return id_dict[word]
    else:
        return id_dict['<unknown>']

def if_contain_char(string, char_list):
    for char in char_list:
        if(char in string):
            return True
    return False

print("古诗总数:{}".format(len(poems)))
poems_useful = []
for line in poems:
    line = line.strip()
    if(line.count(':') != 1):
        continue
    try:
        title, content = line.split(":")
    except:
        continue
    content = content.strip().replace(' ','')
    content = content.replace('\n','')
    # 包含非法字符的古诗内容丢弃
    if(if_contain_char(content,error_char)):
        continue
    # 太短，太长的古诗内容丢弃
    length = len(content)
    if(length > max_sentence_length or length < min_sentence_length):
        continue
    # 筛选完毕，加入列表
    poems_useful.append(content)

print("有效的古诗总数:{}".format(len(poems_useful)))

# 按长短来排个序
poems_useful = sorted(poems_useful, key=lambda x: len(x))

word_list = []
num = 0
for poem in poems_useful:
    # start = time.time()
    word_list.extend([word for word in poem])
    # end = time.time()
    # num += 1
    # print("一首多少秒:%.3f，第%d首"%(end-start,num))
# 统计出现次数
counter = Counter(word_list)
# 排序
sorted_word_list = sorted(counter.items(), key=lambda x:int(x[1]), reverse=True)
# 筛选掉出现频次太少的单词
sorted_word_list_selected = [x for x in sorted_word_list if(x[1] >= min_word_frequency)]
# 就算这样也是已经排好序的列表了
word_list = ['[PAD]','[UNK]','[CLS]','[SEP]'] + [x[0] for x in sorted_word_list_selected]
print("词汇表中词有效总数:{}".format(len(word_list)))

with open(vocabulary_data_path, 'w',encoding='utf-8') as f:
    for word in word_list:
        f.write(word + '\n')

# 单词:id 字典
word_id_dict = dict(zip(word_list,range(len(word_list))))
write_dict(word_id_dict,'word_id_dict.txt')
# tokenizer = Tokenizer(word_id_dict)
# print(word_id_dict.items())
# # 将单词转化为词向量
# poems_useful_id = []
# for poem in poems_useful:
#     poems_useful_id.append([str(word_to_id(word, word_id_dict)) for word in poem])
# # 将词向量写入文件

# with open(vocabulary_vector_data_path,'w',encoding='utf-8') as f:
#     for voc_vec in poems_useful_id:
#         f.write(''.join(voc_vec) + '\n')