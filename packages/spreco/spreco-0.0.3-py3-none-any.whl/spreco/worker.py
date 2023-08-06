from spreco.common.options import MODELS
from spreco.common import utils
from spreco.common.logger import logger
from spreco.common.utils import LambdaWarmUpCosineScheduler

import tensorflow.compat.v1 as tf
tf.disable_eager_execution()

import os
import numpy as np
import time

class worker():
    """
    mode, 0: train
    mode, 1: inference
    mode, 2: export
    """

    def __init__(self, train_pipe, test_pipe, config, default_feed=True):

        self.train_pipe = train_pipe
        self.test_pipe  = test_pipe
        self.config     = config

        if train_pipe is not None:
            self.log_path   = utils.create_folder(config['log_folder'])
            utils.save_config(config, self.log_path)
            self.logger = logger(self.log_path)

        self.model      = None
        self.sess       = None

        self.global_step  = 0
        self.default_feed = default_feed


    def init_model(self, mode, feed_func=None, gpu_id=None):
        
        if self.config['model'] == MODELS.NCSN:
            tf.random.set_random_seed(self.config['seed'])
            from spreco.model.ncsn import ncsn as selected_class

        elif self.config['model'] == MODELS.SDE:
            from spreco.model.sde import sde as selected_class

        elif self.config['model'] == MODELS.PIXELCNN:
            from spreco.model.pixelcnn import pixelcnn as selected_class

        else:
            raise Exception("Currently, this model is not implemented!")

        if mode == 0:
            self.lr_scheduler = LambdaWarmUpCosineScheduler(self.config['lr_warm_up_steps'],
                                self.config['lr_min'], self.config['lr_max'], self.config['lr_start'], self.config['lr_max_decay_steps'])

        self.model = selected_class(self.config)

        self.model.init(mode)
        if not self.default_feed:
            self.feed_func=feed_func

        # set gpu
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        if gpu_id is None:
            os.environ["CUDA_VISIBLE_DEVICES"] = '-1'
        else: 
            os.environ["CUDA_VISIBLE_DEVICES"] = gpu_id

    def mk_feed_dict(self, pipe, reps=None):
        """"utility to make feed dict"""
        if reps is None:
            reps = self.config['nr_gpu']

        keys = self.model.ins_outs.keys()
        elm = pipe.get_next()
        feed_dict ={}

        for key in keys:
            tmp = np.split(elm[key], self.config['nr_gpu'])
            feed_dict.update({self.model.ins_outs[key][i]: tmp[i] for i in range(reps)})

        return feed_dict

    def run_op(self, sess, ops, loss, feed_dict, is_training):
        
        if is_training:
            if type(ops) == list:
                l = []
                for op, l_op in zip(ops, loss):
                    l_tmp, _ = sess.run([l_op, op], feed_dict=feed_dict)
                    l.append(l_tmp)

            else:
                l, _ = sess.run([loss, ops], feed_dict=feed_dict)

            return l

        else:
            if type(loss) == list:
                l = []
                for l_op in loss:
                    l_tmp = sess.run(l_op, feed_dict=feed_dict)
                    l.append(l_tmp)

            else:
                l = sess.run(loss, feed_dict=feed_dict)

            return l

    def mk_kvs(self, keys, values):
        kvs = {}
        for key, value in zip(keys, values):
            if type(value) == list:
                for i, a in enumerate(value):
                    key_ = "%s_%d"%(key,i)
                    kvs[key_] = a
            else:
                kvs[key] = value
        return kvs

    def mk_info(self, epoch, t, loss_avg, printing, is_training=True):

        if is_training:
            info = "Epochs %d, time %ds, train loss: %s" % (epoch, t, ''.join(str(loss_avg)))
        else:
            info = "Epochs %d, time %ds, test loss: %s" % (epoch, t, ''.join(str(loss_avg)))

        if printing:
            print(info)

        return info

    def train_loop(self):

        # ready to go
        init_op    = tf.global_variables_initializer()
        saver      = tf.train.Saver(max_to_keep=self.config['max_keep'])
        gpu_config = tf.ConfigProto(allow_soft_placement=True)
        sess       = tf.Session(config=gpu_config)
        sess.run(init_op)

        utils.print_parameters(self.log_path+'/layer_info')
        train_loss = []
        test_loss  = []
        begin      = time.time()

        while self.train_pipe.get_epoch() < self.config['max_epochs']:

            if self.default_feed:
                feed_dict = self.mk_feed_dict(self.train_pipe)
            else:
                feed_dict = self.feed_func(self, self.train_pipe)

            learning_rate = self.lr_scheduler(self.global_step)

            feed_dict.update({self.model.learning_rate: learning_rate})

            l = self.run_op(sess, self.model.train_op, self.model.loss_train, feed_dict, is_training=True)
            self.global_step = self.global_step + 1

            kvs = self.mk_kvs(['train_loss', 'learning_rate'], [l, learning_rate])
            self.logger.writekvs(kvs)

            train_loss.append(l)

            if self.train_pipe.check_epoch():

                # one epoch is finised
                self.train_pipe.update_epoch()
                if self.train_pipe.get_epoch() % self.config["save_interval"] == 0:
                    saver.save(sess, os.path.join(self.log_path, self.config['saved_name']+'_'+str(self.train_pipe.get_epoch())))

                epoch = self.train_pipe.get_epoch()
                train_loss_avg = np.mean(train_loss, axis=0).tolist()

                info = self.mk_info(epoch, time.time()-begin, train_loss_avg, self.config['print_loss'])
                utils.log_to(os.path.join(self.log_path, 'loss'), [info], prefix="->")
                kvs = self.mk_kvs(['train_loss_avg'], [train_loss_avg])
                self.logger.writekvs(kvs, epoch)
                begin      = time.time()
                train_loss = []

                # run test
                while not self.test_pipe.check_epoch():
                    if self.default_feed:
                        feed_dict = self.mk_feed_dict(self.test_pipe)
                    else:
                        feed_dict = self.feed_func(self, self.test_pipe)

                    l = self.run_op(sess, None, self.model.loss_test, feed_dict=feed_dict, is_training=False)
                    test_loss.append(l)

                self.test_pipe.update_epoch()
                test_loss_avg = np.mean(test_loss, axis=0).tolist()
                info = self.mk_info(epoch, time.time()-begin, test_loss_avg, self.config['print_loss'], False)
                utils.log_to(os.path.join(self.log_path, 'loss'), [info], prefix="->")
                kvs = self.mk_kvs(['test_loss_avg'], [test_loss_avg])
                self.logger.writekvs(kvs, epoch)

                test_loss  = []
                begin      = time.time()

    def train(self, feed_func=None):
        self.train_pipe.start()
        self.test_pipe.start()
        self.init_model(mode=0, feed_func=feed_func, gpu_id=self.config['gpu_id'])
        self.train_loop()
        self.train_pipe.stop()
        self.test_pipe.stop()

    def inference(self, model_path, func, batch_size=None, gpu_id=None, **kwargs):
        """
        Restore the model located at model_path 
        Create the tf sess and model
        Func must take sess and model as two args
        Kwargs will be passed to func and which could be None
        """

        if self.model is None and self.sess is None:
            self.init_model(mode=1, batch_size=batch_size, gpu_id=gpu_id)
            _, sess, _ = self.restore(model_path)
            self.sess = sess

        return func(self.sess, self.model, **kwargs)

    def export(self, model_path, export_path, name, gpu_id='0'):

        self.init_model(mode=2, gpu_id=gpu_id)
        saver, sess, gpu_id = self.restore(model_path)
        utils.export_model(saver, sess, export_path, name, gpu_id=gpu_id)

    def restore(self, model_path):
        """restore the given model"""

        saver        = tf.train.Saver()
        gpu_options  = tf.GPUOptions(allow_growth=True, visible_device_list='0')
        config_proto = tf.ConfigProto(gpu_options=gpu_options)
        serialized   = config_proto.SerializeToString()
        gpu_id       = list(map(hex, serialized))
        sess         = tf.Session(config=config_proto)
        saver.restore(sess, model_path)
        return saver, sess, gpu_id