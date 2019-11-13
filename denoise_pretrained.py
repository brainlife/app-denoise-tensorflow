#!/usr/bin/env python3

import os
from pathlib import Path
import sys
import json
import nibabel as nib
import numpy as np
import tensorflow as tf
#from tensorflow.python.client import device_lib
#print(device_lib.list_local_devices())

def getModel(x, nDim):
    ## THIS GENERATES THE TF GRAPH TREE USED FOR TRAINING. SEE HU'S ABSTRACT
    ## FOR MORE INFORMATION ABOUT THIS
    # Input Layer
    input_layer = tf.reshape(x, [-1, nDim, 1])

    # Convolutional Layer #1
    conv1 = tf.layers.conv1d(
        inputs=input_layer,
        filters=16,
        kernel_size=16,
        padding="same",
        activation=tf.nn.relu)

    # Pooling Layer #1
    pool1 = tf.layers.max_pooling1d(inputs=conv1, pool_size=2, strides=2)

    # Convolutional Layer #2 and Pooling Layer #2
    conv2 = tf.layers.conv1d(
        inputs=pool1,
        filters=32,
        kernel_size=8,
        padding="same",
        activation=tf.nn.relu)

    pool2 = tf.layers.max_pooling1d(inputs=conv2, pool_size=2, strides=2)

    # Dense Layer
    pool2_flat = tf.layers.flatten(pool2)

    logits = tf.layers.dense(inputs=pool2_flat, units=nDim, activation=tf.nn.relu)

    return logits


def main():
    # opens configuration file for inputs
    with open('config.json') as config_json:
        config = json.load(config_json)
    
    # load brainmask
    masktmp = nib.load(str(config['mask']))
    msk_img = masktmp.get_fdata()
    sz = msk_img.shape
    msk = msk_img
    
    # load noisy SoS data
    tmp = nib.load(str(config['dwi_noise']))
    normal_img = tmp.get_fdata()
    sz = normal_img.shape
    nDim = sz[3]
    imgNoised = np.transpose(np.reshape(tmp.get_fdata(), (sz[0]*sz[1]*sz[2], sz[3])))
    sigNoised = np.delete(imgNoised, np.where(msk != 1), axis=1)  # signals with high-level noise
    
    # define tensorflow graph
    input = tf.placeholder(tf.float32, [None, nDim])

    output = getModel(input, nDim=nDim)

    sess = tf.InteractiveSession()
    sess.run(tf.global_variables_initializer())
    
    # loads pretrained models
    saver = tf.train.Saver()
    trainedPath = './pretrained-models/' + config['trainingSubj'] + '/' + str(config['iters']) + '/ckpt/model.ckpt'
    saver.restore(sess, trainedPath)
    
    # set batch size and dumby image
    batch_size = int(config['batch_size']) #2000
    x = np.zeros((sz[3], sz[0] * sz[1] * sz[2]))
    size = 0
    
    # fit pretrained model graph to noisy SoS data
    for i in range(0, np.int(sz[0] * sz[1] * sz[2]), batch_size):
        size += batch_size
        if size <= (sz[0] * sz[1] * sz[2]):
            batch_tmp = imgNoised[:, i: size]
            x[:, i: size] = output.eval(feed_dict={input: batch_tmp.T}).T
        else:
            batch_tmp = imgNoised[:, i: np.int(sz[0] * sz[1] * sz[2])]
            x[:, i: np.int(sz[0] * sz[1] * sz[2])] = output.eval(feed_dict={input: batch_tmp.T}).T
    sess.close()

    # masking and saving results
    x_img = np.float32(np.reshape(np.transpose(x), (sz[0], sz[1], sz[2], sz[3])))
    img_denoised = tmp.get_fdata()
    img_denoised[:, :, :,:] = x_img[:, :, :, :]
    for ii in range(0, nDim):
        img_denoised[:, :, :, ii] = img_denoised[:, :, :, ii] * msk_img

    x1 = nib.Nifti1Image(img_denoised, tmp.affine, tmp.header)
    nib.save(x1, 'dwi.nii.gz')


if __name__ == '__main__':
    main()

