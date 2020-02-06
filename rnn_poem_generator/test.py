import numpy as np
import tensorflow as tf

from util import load_graph,read_dict,Tokenizer,get_newest
from model import model

frozen_graph_path = "frozen_model"
frozen_graph = get_newest(frozen_graph_path)

word_id_dict = read_dict("config/word_id_dict.txt")
word_id_dict = {key:int(val) for key,val in word_id_dict.items()}

tokenizer = Tokenizer(word_id_dict)
evalmodel = model(1)

def generate_ramdom_poetry(tokenizer, graph, begin_word=None):
    """
    随机生成一首诗。
    Args:
        tokenizer:转义字符器。
        graph:rnn 计算图。
        s:起始字符。
    Return:
        poem:生成的诗。
    """
    # 初始字符编码
    word = begin_word or ''
    id_s = [tokenizer.word_to_id(word)]
    id_s = np.expand_dims(id_s, axis=0)
    input_data = tf.placeholder(tf.int32, [1, None])

    op_predict,op_last_state = evalmodel.network(input_data, 2, 128, 4147)
    saver = tf.train.Saver()
    init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
    with tf.Session() as sess:
        sess.run(init_op)

        poem = ''

        poem += word

        saver.restore(sess, 'ckpt/model')
        predict,last_state = sess.run([op_predict, op_last_state], {input_data: id_s})

        word = tokenizer.id_to_word(np.argmax(predict, axis=-1)[0][0])

        poem += word

        i = 0
        while word != '[SEP]':
            poem += word
            i += 1
            if i > 24:
                break
            x = np.array([[tokenizer.word_to_id(word)]])
            predict,last_state = sess.run([op_predict, op_last_state], {input_data: x, op_last_state:last_state})
            word = tokenizer.id_to_word(np.argmax(predict, axis=-1)[0][0])

        return poem
print(generate_ramdom_poetry(tokenizer, frozen_graph, "黑"))