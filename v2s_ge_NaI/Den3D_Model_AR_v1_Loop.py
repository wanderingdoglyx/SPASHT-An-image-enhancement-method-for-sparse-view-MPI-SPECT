
from tensorflow.python.framework.ops import disable_eager_execution
import gc
from tensorflow.keras import layers
from tensorflow.keras.models import Model,load_model
from tensorflow.keras.layers import Input, Conv3D, Conv2D, Conv3DTranspose,UpSampling3D,UpSampling2D,MaxPooling3D, Dropout, BatchNormalization, concatenate, Add, Activation, LeakyReLU
from tensorflow.keras.activations import softmax
from tensorflow.keras.initializers import Constant
#from tensorflow.keras.utils import multi_gpu_model
import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras.callbacks import Callback,ReduceLROnPlateau
import numpy as np
from tensorflow.keras import backend as K
tf.compat.v1.enable_eager_execution()
#tf.config.run_functions_eagerly(True)
NORMALIZER = 1e1

def metric_mse():
  def fn(y_true, y_pred):
    #squared_difference = tf.square(y_true - y_pred)
    return tf.reduce_mean(tf.square(y_true - y_pred), axis=-1)
  fn.__name__ = 'mse'
  return fn

def metric_mae():
  def fn(y_true, y_pred):
    #squared_difference = tf.abs(y_true - y_pred)
    return tf.reduce_mean(tf.abs(y_true - y_pred), axis=-1)
  fn.__name__ = 'mae'
  return fn

def metric_tv(lambda_val):
  def fn(y_true, y_pred):
    return lambda_val * tf.reduce_mean(tf.image.total_variation(tf.squeeze(y_pred, axis=-1)))
  fn.__name__ = 'tv'
  return fn

def loss_fn_v1(lambda_val):
  def fn(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_true - y_pred)) \
            + lambda_val * tf.image.total_variation(tf.squeeze(y_pred, axis=-1))
  return fn

def loss_fn_v2(lambda_val):
  def fn(y_true, y_pred):
    return tf.reduce_mean(tf.abs(y_true - y_pred)) \
            + lambda_val * tf.image.total_variation(tf.squeeze(y_pred, axis=-1))
  return fn

def conv_tr_bnorm_relu_drp(nb_filters, krx, kry, krz, name, strd=(2,2,2), bias_ct=0.03, leaky_alpha=0.01, drop_prob=0.0):
  def f(input):
    conv = Conv3DTranspose(  nb_filters, 
                             kernel_size = (krx, kry, krz), # num. of filters and kernel size 
                             strides=strd,
                             padding='same',
                             use_bias=True,
                             kernel_initializer='glorot_normal', 
                             bias_initializer=Constant(value=bias_ct))(input)
    conv = BatchNormalization(name='BN-'+name)(conv)
    conv = LeakyReLU(alpha=leaky_alpha)(conv) # activation func. 

    return conv
  return f


def conv_relu_drp(nb_filters, krx, kry, krz, name, bias_ct=0.03, leaky_alpha=0.01, drop_prob=0.1):
  def f(input):
    conv = Conv3D( nb_filters, 
                   kernel_size = (krx, kry, krz), # num. of filters and kernel size 
                   strides=(1,1,1),
                   padding='same',
                   use_bias=True,
                   kernel_initializer='glorot_normal', 
                   bias_initializer=Constant(value=bias_ct))(input)
    conv = BatchNormalization(name='BN-'+name)(conv)
    conv = LeakyReLU(alpha=leaky_alpha)(conv) # activation func. 
    conv = Dropout(drop_prob)(conv) 

    return conv
  return f

def conv_bnorm_relu_drp(nb_filters, krx, kry, krz, name, bias_ct=0.03, leaky_alpha=0.01, drop_prob=0.1):
  def f(input):
    conv = Conv3D( nb_filters, 
                   kernel_size = (krx, kry, krz), # num. of filters and kernel size 
                   strides=(1,1,1),
                   padding='same',
                   use_bias=True,
                   kernel_initializer='glorot_normal', 
                   bias_initializer=Constant(value=bias_ct))(input)
    conv = BatchNormalization(name='BN-'+name)(conv)
    conv = LeakyReLU(alpha=leaky_alpha)(conv) # activation func. 
    conv = Dropout(drop_prob)(conv) 

    return conv
  return f

class SlicingLayer(layers.Layer):
  def __init__(self, start_slice = [0, 0, 0, 24, 0], slice_width = [-1, -1, -1, 3, -1], name='Slice_model'): #change: 2/4/23
    super(SlicingLayer, self).__init__(name=name)
    self.start_slice = tf.Variable(initial_value=start_slice, trainable=False, name='start_slice')
    self.slice_width = tf.Variable(initial_value=slice_width, trainable=False, name='slice_width')

  #@tf.function
  def call(self, inputs):
    #f = inputs
    #print("f shape:", K.shape(f))
    #batch_size = K.shape(f)[0]
    return tf.slice(inputs, self.start_slice, self.slice_width)

class ChannelShiftLayer(layers.Layer):
  def __init__(self, U, name = 'Channel_shift_model'):
    super(ChannelShiftLayer, self).__init__(name=name)
    #self.U = U
    self.U = tf.Variable(initial_value=U, trainable=False, name='Channels')
    #print('issue')
    #self.trainable = False
  #@tf.function
  def call(self, loc_img):
    # loc_image: size -> (B, 48, 48, 1)
    # U_shape:   size -> (32, 32, 1, 4) 
    # out_shape: size -> (B, 48, 48, 1, 4)
    #in_shape = K.shape(loc_img) #(B, 48, 48, 1)
    #k_shape = K.shape(self.U)
    #conv = Conv2D(
    #          k_shape[-1], 
    #          [k_shape[1], k_shape[2]],
    #          kernel_initializer = self.kernel_init,
    #          input_shape = in_shape[1:],
    #          padding = 'same',
    #          trainable = False
    #        )(loc_img) 
    loc_img = UpSampling2D(size=(2,2))(loc_img)
    conv = tf.nn.conv2d(
              loc_img,
              self.U,
              strides=[1, 1, 1, 1],
              padding='SAME'
            )
    #conv = loc_img
    conv = tf.expand_dims(conv, -2)
    #print("=======================>conv shape:", K.shape(conv))
    #conv = tf.expand_dims(loc_img, -2)
    return conv
  
  #@tf.function
  #def kernel_init(shape):
  #  #kernel = np.zeros(shape)
  #  kernel = self.U
  #  return kernel 

class ChannelizeLayer(layers.Layer):
  def __init__(self, name = 'Channelize_model'):
    super(ChannelizeLayer, self).__init__(name=name)
    #self.U_shifted = U_shifted
    #self.U_shifted = tf.Variable(initial_value=U_shifted, trainable=False, name='Channels')

  #@tf.function
  def call(self, f, U_shifted):
    # U_shifted:    size -> (B, 48, 48, 1, 4)
    # input_shape:  size -> (B, 48, 48, 3, 1)
    # output_shape: size -> (B, 3, 4)
    #u_shape = K.shape(self.U_shifted)
    #v = tf.reduce_sum(tf.multiply(f, U_shifted), [1, 2])
    f = UpSampling3D(size=(2,2,1))(f)
    v = tf.divide(tf.reduce_sum(tf.multiply(f, U_shifted), [1, 2]), NORMALIZER)
    #print("=======================>v shape:", K.shape(v))
    return v

def CNN_dennet3D_v3(input,num_reg,names):
  """ 
  F1. CBR1-CBR2-DS1-CBR3-CBR4-DS2-CBR5-CBR-DS-CBR-US
  F2. 
  """
  Feat1 = conv_relu_drp(16,3,3,3,names+'F2',drop_prob=0)(input)
  x = MaxPooling3D(pool_size=(2,2,2),name=names+'Pool1')(Feat1)

  Feat2 = conv_relu_drp(32,3,3,3,names+'F4',drop_prob=0)(x)
  x = MaxPooling3D(pool_size=(2,2,2),name=names+'Pool2')(Feat2)

  Feat3 = conv_relu_drp(64,3,3,3,names+'F7',drop_prob=0.0)(x)
  x = MaxPooling3D(pool_size=(2,2,2),name=names+'Pool3')(Feat3)
  

  x = conv_relu_drp(128,3,3,3,names+'Fmid',drop_prob=0.1)(x)
    

  x = conv_tr_bnorm_relu_drp(64,2,2,2,names+'Up1')(x)
  x = Add()([x, Feat3])
  x = conv_relu_drp(64,3,3,3,names+'F8',drop_prob=0.0)(x)

  x = conv_tr_bnorm_relu_drp(32,2,2,2,names+'Up2')(x)
  x = Add()([x, Feat2])
  x = conv_relu_drp(32,3,3,3,names+'F12',drop_prob=0)(x)

  x = conv_tr_bnorm_relu_drp(16,2,2,2,names+'Up3')(x)
  x = Add()([x, Feat1])
  x = conv_relu_drp(16,3,3,3,names+'F13',drop_prob=0)(x)


  x = Conv3D( num_reg, 
                 kernel_size = (1, 1, 1), # num. of filters and kernel size 
                 strides=(1,1,1),
                 padding='same',
                 use_bias=True,
                 kernel_initializer='glorot_normal', 
                 bias_initializer=Constant(value=0.03))(x)

  #x = BatchNormalization(name='BN-last')(x)
  x = LeakyReLU(alpha=0.00)(x)

  #x = Add()([x, input])

  return x


def build_dennet3D(input_shape, loc_shape, num_reg, lambda_val_chdiff, lambda_val_mdiff, U):
  F_hat_LD = Input(shape = (input_shape), name = 'f_hat_ld')
  F_hat_ND = Input(shape = (input_shape), name = 'f_hat_nd')
  Loc_Img = Input(shape = (loc_shape), name = 'loc_img')
  Mask_Img = Input(shape = (input_shape), name = 'mask_img')

  # build denoise net
  denoise_net_out = CNN_dennet3D_v3(F_hat_LD, num_reg, 'CNN3D')
  denoise_net = Model(
                    inputs = F_hat_LD, 
                    outputs = denoise_net_out
                  )

  # build the full network 
  print(f'Building  the full net ...')
  print(f'Denoiser ...')
  F_hat_ND_pred = denoise_net(F_hat_LD)
  print(f'Channel Shift ...')
  Channels_Shifted = ChannelShiftLayer(U=U, name='ChSh1')(Loc_Img)
  print(f'Slicing ...')
  F_hat_ND_sliced = SlicingLayer(name='Slice1')(F_hat_ND)
  F_hat_ND_pred_sliced = SlicingLayer(name='Slice2')(F_hat_ND_pred)
  print(f'Channelize ...')
  v_ND = ChannelizeLayer(name='chize1')(F_hat_ND_sliced, Channels_Shifted)
  v_ND_pred = ChannelizeLayer(name='chize2')(F_hat_ND_pred_sliced, Channels_Shifted)

  #opt = optimizers.Adam(learning_rate=1e-3)
  #model.compile(loss = loss_fn_v2(lambda_val=lambda_val), optimizer=opt, metrics=[metric_mae(), metric_tv(lambda_val=lambda_val)])
  denoise_obs_net = Model(
                      inputs = [F_hat_LD, F_hat_ND, Loc_Img, Mask_Img], 
                      outputs = [F_hat_ND_pred, Channels_Shifted, v_ND, v_ND_pred]
                    )
  #denoise_obs_net.summary()

  #========================================
  # Custom Losses
  #========================================
  #========================================
  # Loss1: L1 loss of denoising
  #========================================
  denoise_obs_net.add_loss(tf.reduce_mean(tf.math.squared_difference(F_hat_ND, F_hat_ND_pred)))
   
  #========================================
  # Loss2: (channelized difference)
  #========================================
  denoise_obs_net.add_loss(lambda_val_chdiff*tf.reduce_mean(tf.math.squared_difference(v_ND, v_ND_pred)))

  #========================================
  # Loss2: (masked difference)
  #========================================
  denoise_obs_net.add_loss(
      lambda_val_mdiff * 
      tf.reduce_mean(
        tf.math.abs(
          tf.multiply(Mask_Img, F_hat_ND_pred) -  
          tf.multiply(Mask_Img, F_hat_LD)
        )
      )
    )

  #========================================
  # Custom Metrics
  #========================================
  #========================================
  # Metric1: L1 loss for denoising
  #========================================
  denoise_obs_net.add_metric(tf.reduce_mean(tf.math.squared_difference(F_hat_ND, F_hat_ND_pred)), 
                              name = 'mse', aggregation = 'mean')
  denoise_obs_net.add_metric(tf.reduce_mean(tf.math.squared_difference(v_ND, v_ND_pred)), 
                              name = 'chv_mse', aggregation = 'mean')
  denoise_obs_net.add_metric(
      tf.reduce_mean(
        tf.math.abs(
          tf.multiply(Mask_Img, F_hat_ND_pred) -  
          tf.multiply(Mask_Img, F_hat_LD)
        )
      ),
      name = 'masked_diff', 
      aggregation = 'mean'
    )

  return denoise_obs_net

def build_dennet3D_pred(input_shape, num_reg):
  F_hat_LD = Input(shape = (input_shape), name = 'f_hat_ld')

  # build denoise net
  denoise_net_out = CNN_dennet3D_v3(F_hat_LD, num_reg, 'CNN3D')
  denoise_net = Model(
                    inputs = F_hat_LD, 
                    outputs = denoise_net_out
                  )

  # build the full network 
  print(f'Building  the full net ...')
  print(f'Denoiser ...')
  F_hat_ND_pred = denoise_net(F_hat_LD)

  #opt = optimizers.Adam(learning_rate=1e-3)
  #model.compile(loss = loss_fn_v2(lambda_val=lambda_val), optimizer=opt, metrics=[metric_mae(), metric_tv(lambda_val=lambda_val)])
  denoise_obs_net = Model(
                      inputs = [F_hat_LD], 
                      outputs = [F_hat_ND_pred]
                    )
  #denoise_obs_net.summary()
  return denoise_obs_net
class LossHistory(Callback):
  def on_train_begin(self, logs={}):
    self.losses = []
  def on_batch_end(self, batch, logs={}):
    self.losses.append(logs.get('loss'))

class ClearMemory(Callback):
  def on_epoch_end(self, epoch, logs=None):
    gc.collect()
    K.clear_session()

