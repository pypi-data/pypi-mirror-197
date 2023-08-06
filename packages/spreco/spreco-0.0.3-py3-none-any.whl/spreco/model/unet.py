from spreco.model import nn, blocks
import tensorflow.compat.v1 as tf
import numpy as np
from tf_slim import arg_scope

class unet():

    def __init__(self, name, config, chns):

        super().__init__(name,
                        config,
                        tf.make_template('forward', self.body),
                        chns, nn.get_nonlinearity(config['nonlinearity']))
        self.counters    = {}

        self.nr_filters = self.config['nr_filters']
        self.attention  = self.config['attention']
        self.ch_factor  = self.config['ch_factor']
        self.nr_resnet  = self.config['nr_resnet']

    def body(self, x, t):

        with arg_scope([nn.conv2d_plus, blocks.cond_resnet, nn.self_attention, nn.downsample, nn.upsample, nn.nin], nonlinearity=self.nonlinearity, counters=self.counters, normalizer=None):

            # downstream
            temb = nn.get_timestep_embedding(t, embedding_size=self.nr_filters)
            temb = nn.nin(temb, self.nr_filters * 4, self.nonlinearity)
            temb = nn.nin(temb, self.nr_filters * 4)

            blks = []

            x = nn.conv2d_plus(x, self.nr_filters, nonlinearity=None)
            blks.append(x)

            for level, (factor, attn) in enumerate(zip(self.ch_factor, self.attention)):

                current_filters = factor*self.nr_filters
                for i in range(self.nr_resnet):
                    x = blocks.cond_resnet(x, temb, current_filters, rescale=False, rescale_with_conv=True)
                    if attn:
                        x = nn.self_attention(x, qk_chns=current_filters, v_chns=current_filters)
                    blks.append(x)
                if level != len(self.ch_factor)-1:
                    x = nn.downsample(x, with_conv=True)
                    blks.append(x)

            # bottom
            x = blocks.cond_resnet(x, temb, current_filters, rescale=False)
            x = nn.self_attention(x, current_filters, current_filters)
            x = blocks.cond_resnet(x, temb, current_filters, rescale=False)
            
            # upstream
            for level, (factor, attn) in enumerate(zip(reversed(self.ch_factor), reversed(self.attention))):

                current_filters = factor*self.nr_filters
                for i in range(self.nr_resnet+1):

                    x = blocks.cond_resnet(tf.concat([x, blks.pop()], axis=-1), temb, current_filters, rescale=False, rescale_with_conv=True)
                    if attn:
                        x = nn.self_attention(x, qk_chns=current_filters, v_chns=current_filters)

                if level!= len(self.ch_factor)-1:
                    x = nn.upsample(x, x.shape[1:3], 2, current_filters, True)
            x = self.nonlinearity(x)
            x = nn.conv2d_plus(x, num_filters=self.out_chns, nonlinearity=None)
            self.counters = {}
            return x