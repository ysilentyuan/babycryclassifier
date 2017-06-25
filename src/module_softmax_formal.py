# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""A very simple MNIST classifier.
See extensive documentation at
https://www.tensorflow.org/get_started/mnist/beginners
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from PreFlight import const
from PreFlight import data_generation_for_softmax as gd
import numpy as np

import argparse
import sys
import tensorflow as tf

FLAGS = None


def main(_):
  # Import data
  [train_x,train_y] = gd.loadTrain()
  [test_x,test_y] = gd.loadTest()

  # Create the model
  x = tf.placeholder(tf.float32, [None, const.param_feature_num],name="input")
  W = tf.Variable(tf.zeros([const.param_feature_num, const.param_final_category]),name='weight')
  b = tf.Variable(tf.zeros([const.param_final_category]),name="bias")
  y = tf.add(tf.matmul(x, W) , b, name="softop")

  # Define loss and optimizer
  y_ = tf.placeholder(tf.float32, [None, const.param_final_category])

  cross_entropy = tf.reduce_mean(
      tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
  train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

  sess = tf.InteractiveSession()
  tf.global_variables_initializer().run()
  saver = tf.train.Saver()

  # Train
  for _ in range(1000):
    #batch_xs, batch_ys = gd.iterate_minibatches(train_x,train_y, 2, shuffle=True)
    sess.run(train_step, feed_dict={x: train_x, y_: train_y})
    if _ % 50 == 0:
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        print("Setp: ", _, "Accuracy: ", sess.run(accuracy, feed_dict={x: train_x,y_: train_y}))

  # Test trained model
  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  print(sess.run(accuracy, feed_dict={x: test_x,y_: test_y}))

  #[predict, empty] = gd.loadPredict("C:\\Project\\2017Hackthon\\data\\predict.csv")
  #preY = tf.add(tf.matmul(tf.cast(predict,tf.float32), W), b)

  saver.save(sess, "C:\\Project\\2017Hackthon\\data\\voice_model", global_step=1000)
  weights = W.eval()
  bias = b.eval()
  np.savetxt("C:\\Project\\2017Hackthon\\data\\Weights.csv", weights, delimiter=",")
  np.savetxt("C:\\Project\\2017Hackthon\\data\\bias.csv", bias, delimiter=",")

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',
                      help='Directory for storing input data')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)