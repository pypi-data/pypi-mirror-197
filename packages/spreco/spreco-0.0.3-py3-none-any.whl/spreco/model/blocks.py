from spreco.model import nn
from spreco.model import utils

import tensorflow.compat.v1 as tf
tf.disable_eager_execution()
from tf_slim import add_arg_scope

@add_arg_scope
def cond_resnet(x, h, out_filters, nonlinearity, normalizer, rescale=False, rescale_with_conv=True, **kwargs):
    """
    resnet block
    out_filters is output_dims/feature
    """

    in_filters = nn.int_shape(x)[-1]
    x_skip = x

    if normalizer is not None:
        x = normalizer(x) 
    x = nonlinearity(x)

    if rescale:
        x = nn.conv2d_plus(x, in_filters, nonlinearity=None, scope='cond_res', **kwargs)
    else:
        x = nn.conv2d_plus(x, out_filters, nonlinearity=None, scope='cond_res', **kwargs)

    if normalizer is not None:
        x = normalizer(x)
    x = nonlinearity(x)

    x = nn.conv2d_plus(x, out_filters, nonlinearity=None, scope='cond_res', **kwargs)
    if rescale:
        x = tf.nn.avg_pool2d(x, ksize=(1,2,2,1), strides=(1,2,2,1), padding='SAME')
    
    if out_filters == in_filters and not rescale: # the shape of current variable remains the same as 
        shortcut = x_skip
    else:
        if rescale:
            if rescale_with_conv:
                shortcut = nn.conv2d_plus(x_skip, out_filters, filter_size=[3, 3], stride=[2,2])
            else:
                shortcut = tf.nn.avg_pool2d(x_skip, ksize=(1,2,2,1), strides=(1,2,2,1), padding='SAME')
        else:
            shortcut = nn.conv2d_plus(x_skip, out_filters)   # increase filters inside block

    if h is not None:
        shortcut = shortcut + tf.expand_dims(tf.expand_dims(nn.nin(h, out_filters), 1), 1)

    return shortcut + x

@add_arg_scope
def encoder(x, h, z_filters,
            num_filters=64,
            num_resnet=2,
            ch_factor=[1,2,4,8],
            attention=[False, False, True, True],
            rescale_with_conv=True,
            normalizer=nn.instance_norm, nonlinearity=None, **kwargs):
    """
    encode input x into latent space z

    Args:
      x: input
      h: conditional info
      z_filters: the number of features in latent space
      num_filter: the number of features get to the 1st block
      num_resnet: the number of resnet contained within a single block
      ch_factor: the list contains the factor by which the num of features increase
      attention: the list indicate which block has self-attention module
      rescale_with_conv: the bool value tell rescale with convolution or pooling
      normalizer: the normalizer
    """

    blks=[]

    x = nn.conv2d_plus(x, num_filters, nonlinearity=None)
    blks.append(x)

    for level, (factor, attn) in enumerate(zip(ch_factor, attention)):

        current_filters = factor*num_filters
        
        for i in range(num_resnet):

            rescale = False
            if i == num_resnet-1 and level != len(ch_factor)-1:
                rescale=True
            x = cond_resnet(x, h, current_filters, rescale=rescale, rescale_with_conv=rescale_with_conv)
            if attn:
                x = nn.self_attention(x, qk_chns=current_filters, v_chns=current_filters)
            blks.append(x)
    
    x = normalizer(x)
    x = nonlinearity(x)
    z = nn.conv2d_plus(x, z_filters, nonlinearity=None, scope='latent_space')

    return z


@add_arg_scope
def decoder(x, h, out_filters, 
            num_filters=64,
            num_resnet=2,
            ch_factor=[1,2,4,8],
            attention=[True, True, False, False],
            normalizer=nn.instance_norm, nonlinearity=None, **kwargs):
    """
    decode latent space z into x

    Args:
      z, the latent space
      h, the conditional information
      out_filters, the number of channel of output
      num_resnet, the number of resnet that contained within a single block
      ch_factor, the list contains factor by which the number of features increases
      attention, the list indicate which block has self-attention module
      normalier, the default is instance normalizer
    """

    for level, (factor, attn) in enumerate(zip(ch_factor, attention)):

        current_filters = num_filters*factor

        for i in range(num_resnet):

            x = cond_resnet(x, h, current_filters)
            if attn:
                x = nn.self_attention(x, qk_chns=current_filters, v_chns=current_filters)
            if i == num_resnet-1 and level != len(ch_factor)-1:
                x = nn.upsample_2(x, x.shape[1:3], 2, current_filters)
                #x = nn.upsample(x, x.shape[1:3], 2, current_filters, with_conv=False)

    x = normalizer(x)
    x = nonlinearity(x)
    x = nn.conv2d_plus(x, out_filters, nonlinearity=None, scope='output')

    return x

@add_arg_scope
def transformer_block(x, past, num_heads, num_embedings, **kwargs):
    y = nn.nlp_norm(x, scope='transformer_layernorm')
    a, present = nn.causal_attention(y, past, num_heads, num_embedings)
    x = x + a 
    y = nn.nlp_norm(x, scope='transformer_layernorm')
    m = nn.mlp(y, num_embedings*4)
    return x+m, present

@add_arg_scope
def discriminator(x, num_filters, num_layers, norm_layer, **kwargs):

    x = nn.conv2d_plus(x, num_filters, filter_size=[4,4], stride=[2,2])
    x = tf.nn.leaky_relu(x)

    nf_mult = 1

    for n in range(1, num_layers):
        nf_mult = min(2**n, 8)
        x = nn.conv2d_plus(x, num_filters*nf_mult, filter_size=[4,4], stride=[2,2])
        x = norm_layer(x)
        x = tf.nn.leaky_relu(x)

    nf_mult = min(2**n, 8)
    x = nn.conv2d_plus(x, num_filters*nf_mult, filter_size=[4,4])
    x = norm_layer(x)
    x = tf.nn.leaky_relu(x)

    nf_mult = min(2**n, 8)
    x = nn.conv2d_plus(x, 1, filter_size=[4,4])

    return x