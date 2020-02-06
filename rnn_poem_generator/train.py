import time
import yaml as ya
import tensorflow as tf

from util import Generator,Tokenizer,get_dataset,read_dict,frozen_graph
from model import model
from sklearn.model_selection import train_test_split

config_path = "config/config.yaml"
dataset_path = "dataset/dataset.txt"
word_id_dict_path = "config/word_id_dict.txt"
config_dict = None

with open(config_path,"r",encoding='utf-8') as f:
    config_dict = ya.load(f.read())

batch_size = config_dict['batch_size']
learning_rate = config_dict['learning_rate']
max_epoch_num = config_dict['max_epoch_num']
rnn_units_size = config_dict['rnn_units_size'] # LSTM 隐藏结点个数
rnn_layer_number = config_dict['rnn_layer_number'] # RNN 深度
vocabulary_vector_size = config_dict['vocabulary_vector_size'] # 词向量长度，即总共有多少个词
share_embedding_with_output = config_dict['share_embedding_with_output'] # 即输入转换矩阵与 embedding 层是否共用一套矩阵

input = tf.placeholder(tf.int32, [None, None], name='x')
label = tf.placeholder(tf.int32, [None, None, None], name='y')

data = get_dataset(dataset_path)
train_data,valid_data = train_test_split(data, test_size=0.2)
word_id_dict = read_dict(word_id_dict_path)
word_id_dict = {key:int(val) for key,val in word_id_dict.items()}
tokenizer = Tokenizer(word_id_dict)
train_generator = Generator(train_data, batch_size, tokenizer, True)
valid_generator = Generator(valid_data, batch_size, tokenizer, True)
train_epochwise_generator = train_generator.for_fit()
valid_epochwise_generator = valid_generator.for_fit()
one_epoch_steps = train_generator.one_epoch_steps

m = model(batch_size)
output,last_state = m.network(input, rnn_layer_number, rnn_units_size, vocabulary_vector_size)
output = tf.identity(output, name='predict')
loss = m.loss(output, label)
correct = tf.equal(tf.argmax(output, axis=-1), tf.argmax(label, axis=-1))
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32), name='accuracy')
optimizer = m.optimizer(loss, learning_rate)
init = tf.global_variables_initializer()
saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(init)
    for i in range(max_epoch_num):
        epochwise_accuracy = 0
        for j in range(one_epoch_steps):
            train_batch_x,train_batch_y = next(train_epochwise_generator)
            _ = sess.run(optimizer, feed_dict={"x:0":train_batch_x, "y:0":train_batch_y})
            if(j%20 == 0):
                valid_batch_x,valid_batch_y = next(valid_epochwise_generator)
                acc,los = sess.run([accuracy, loss],feed_dict={"x:0":valid_batch_x, "y:0":valid_batch_y})
                epochwise_accuracy += acc*20//one_epoch_steps
                print("epoch:{} accuracy:{} loss:{}".format(i+1, acc, los))
        frozen_graph(sess ,"frozen_model/{}_{}.pb".format(i+1, epochwise_accuracy))
        saver.save(sess, "ckpt/model")
