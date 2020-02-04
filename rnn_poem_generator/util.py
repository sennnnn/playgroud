import os
import numpy as np


def one_hot(nparray, depth=0, on_value=1, off_value=0):
    if depth == 0:
        depth = np.max(nparray) + 1
    # 深度应该符合one_hot条件，其实keras有to_categorical(data,n_classes,dtype=float..)弄成one_hot
    assert np.max(nparray) < depth, "the max index of nparray: {} is larger than depth: {}".format(np.max(nparray), depth)
    shape = nparray.shape
    out = np.ones((*shape, depth),np.uint8) * off_value
    indices = []
    for i in range(nparray.ndim):
        tiles = [1] * nparray.ndim
        s = [1] * nparray.ndim
        s[i] = -1
        r = np.arange(shape[i]).reshape(s)
        if i > 0:
            tiles[i-1] = shape[i-1]
            r = np.tile(r, tiles)
        indices.append(r)
    indices.append(nparray)
    out[tuple(indices)] = on_value
    return out

def write_dict(dict_, filepath):
    """
    将 dict 保存为文件。
    关键是要能够以一种可以区分键值的存储方式存储。
    Args:
        dict_:待保存的字典数据，加个 _ 为了避免和内置函数重名。
        filepath:用于保存字典的文件路径。
    Return:
        None
    """
    if(os.path.exists(filepath)):
        f = open(filepath,'a',encoding='utf-8')
    else:
        f = open(filepath,'w',encoding='utf-8')
    for key,val in dict_.items():
        f.write("{}:{}\n".format(key,val))

def read_dict(filepath):
    """
    每一行的字符串格式为：
    "键:值\n"
    依照这个方式读取即可。
    Args:
        filepath:待读取的字典保存文件。
    Return:
        dict_:读取到的字典数据。
    """
    f = open(filepath,'r',encoding='utf-8')
    lines = f.readlines()
    dict_ = {}
    for line in lines:
        key,val = line.strip().split(':')
        dict_[key] = val
    return dict_

class Generator:
    """
    训练数据生成器
    """

    def __init__(self, data, batch_size, tokenizer, random=False):
        # 数据集
        self.data = data
        # batch size
        self.batch_size = batch_size
        # 单 epoch 迭代步数
        self.one_epoch_steps = int(len(data)/batch_size)
        # 是否对数据进行随机处理
        self.random = random
        self.tokenizer = tokenizer

    def sequence_padding(self, data, length=None, padding=None):
        """
        将数据填充到相同长度，与计算机视觉中控制输入图片长宽是一个意思。
        Args:
            self:调用成员函数的类的实例化对象。
            data:待填充数据。
            length:填充后长度。
            padding:填充值。
        Return:
            padding_after_data:填充后数据。
        """
        # 计算填充长度
        if length is None:
            length = max(map(len, data))
        # 获取用于填充的数据
        if padding is None:
            padding = int(self.tokenizer.word_to_id('[PAD]'))
        length = max(len(data), length)
        padding_after_data = []
        for line in data:
            padding_length = length - len(line)
            # 不足就补充
            if(padding_length > 0):
                padding_after_data.append(np.concatenate([line, [padding]*padding_length]))
            # 超过就截断
            else:
                padding_after_data.append(line[:length])
        return np.array(padding_after_data)
        
    def __len__(self):
        return self.steps

    def __iter__(self):
        length = len(self.data)
        # 是否随机混洗
        if(self.random):
            np.random.shuffle(self.data)
        for start in range(0, total, self.batch_size):
            end = min(start + self.batch_size, length)
            batch = []
            # 对单首古诗编码
            for one in data[start:end]:
                batch.append(self.tokenizer.encode(one))
            # 填充为同一长度
            batch = self.sequence_padding(batch)
            yield batch[:, :-1], one_hot(batch[:, 1:], tokenizer.vocabulary_size)
            del batch

    def for_fit(self):
        """
        创建一个生成器
        """
        # 以 epoch 为界而重新迭代数据。
        # __iter__() 返回的就是一个生成器，而 from 只是将生成器拆开了而已。
        while True:
            yield from self.__iter__()

class Tokenizer:
    """
    分词器
    """

    def __init__(self, word_id_dict):
        # 词:编号
        self._word_id_dict = word_id_dict
        # 编号:词
        self._id_word_dict = {id:world for world,id in word_id_dict.items()}
        # 词汇表大小
        self.vocabulary_size = len(word_id_dict)
    
    def id_to_word(self, id):
        """
        编号到词的映射。
        Args:
            self:调用此成员函数的类的实例化对象。
            id:用来查找词的编号。
        Return:
            word:通过编号查找到的词。
        """
        return self._id_word_dict[id]
    
    def word_to_id(self, word):
        """
        词到编号的映射。
        Args:
            self:调用此成员函数的类的实例化对象。
            word:希望数字化的词。
        Return:
            id:词数字化后的id。
        """
        return self._word_id_dict[word]

    def encode(self, string):
        """
        将字符串编码成数字序列。
        Args:
            self:调用此成员函数的类的实例化对象。
            string:待编码字符串。
        Return:
            ids:编码序列
        """
        # 开始标记
        ids = [self._word_id_dict['CLS']]
        for char in string:
            ids.append(self._word_id_dict[char])
        # 结束标记
        ids.append(self._word_id_dict['[SEP]'])
        return ids

    def decode(self, ids):
        """
        将数字序列解码成字符串。
        Args:
            self:调用此成员函数的类的实例化对象。
            ids:待解码的数字序列。
        Return:
            string:解码后的字符串。
        """
        # head and tail char.
        ht_chars = ['[CLS]','[SEP]']
        # 解码后字符列表
        string = []
        for id in ids:
            word = self._id_word_dict[id]
            if word in ht_chars:
                continue
            string.append(word)
        return ''.join(string)