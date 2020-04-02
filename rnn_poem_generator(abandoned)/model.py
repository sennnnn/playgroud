import os
import yaml as ya
from functools import wraps,partial
import tensorflow as tf

class model(object):
    def __init__(self, batch_size):
        self.batch_size = batch_size

    def network(self, input, rnn_layer_number, rnn_units_size, vocabulary_vector_size):
        vocabulary_embedding_matrix_size = [vocabulary_vector_size, rnn_units_size]
        embedding_convert_matrix = tf.Variable(tf.random_uniform(vocabulary_embedding_matrix_size), name='embedding')
        # embedding 权重，其实就是表示字符的 one-hot 编码变为二维 0~1 的浮点数表示的编码格式。
        lstm_input = tf.nn.embedding_lookup(embedding_convert_matrix, input)

        meta_cell = tf.nn.rnn_cell.BasicLSTMCell(rnn_units_size)
        cell = tf.nn.rnn_cell.MultiRNNCell([meta_cell] * rnn_layer_number)
        initial_state = cell.zero_state(self.batch_size, tf.float32)

        output, last_state = tf.nn.dynamic_rnn(cell, lstm_input, initial_state=initial_state)

        weights = tf.Variable(tf.random_uniform(vocabulary_embedding_matrix_size[::-1]))
        bias = tf.Variable(tf.random_uniform([vocabulary_vector_size]))
        output = tf.add(tf.matmul(output, weights), bias)

        return output, last_state

    def loss(self, predict, label):
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=label, logits=predict, axis=-1))
        return loss

    def optimizer(self, loss, learning_rate):
        optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)
        return optimizer
