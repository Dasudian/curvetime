from tensorflow.keras import layers
from tensorflow import keras
import tensorflow as tf
import pandas as pd
import numpy as np


from .model import Model
from curvetime.env.stock_env import WINDOW_SIZE, TOTAL_STOCKS, FEATURES_PER_STOCK


MODEL_PATH = 'data/models/ac_transformer.h5'

class Transformer(Model):
    """
    The model for stock price analysis
    """
    def __init__(self, env, name='StockModel', filepath=MODEL_PATH,
            head_size=256,
            num_heads=8,
            ff_dim=4,
            num_transformer_blocks=6,
            mlp_units=[128],
            mlp_dropout=0.25,
            dropout=0.25):
        super().__init__(name, filepath)
        self.input_shape = (env.shape[0], env.shape[1]*env.shape[2])
        self.num_actions = env.num_actions
        self.name = name
        self.filepath = filepath
        self.head_size = head_size
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.num_transformer_blocks = num_transformer_blocks
        self.mlp_units = mlp_units
        self.mlp_dropout = mlp_dropout
        self.dropout = dropout
        self._create()


    def _new_model(self):
        model = build_model(
                input_shape=self.input_shape,
                head_size=self.head_size,
                num_heads=self.num_heads,
                ff_dim=self.ff_dim,
                num_transformer_blocks=self.num_transformer_blocks,
                mlp_units=self.mlp_units,
                classes=self.num_actions,
                mlp_dropout=self.mlp_dropout,
                dropout=self.dropout)

        model.compile(
                loss="huber_loss",
                optimizer=keras.optimizers.Adam(learning_rate=1e-4),
                metrics=['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error', 'cosine_proximity'])
        return model




def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0):
    # Normalization and Attention
    x = layers.LayerNormalization(epsilon=1e-6)(inputs)
    x = layers.MultiHeadAttention(
        key_dim=head_size, num_heads=num_heads, dropout=dropout
    )(x, x)
    x = layers.Dropout(dropout)(x)
    res = x + inputs

    # Feed Forward Part
    x = layers.LayerNormalization(epsilon=1e-6)(res)
    x = layers.Conv1D(filters=ff_dim, kernel_size=1, activation="relu")(x)
    x = layers.Dropout(dropout)(x)
    x = layers.Conv1D(filters=inputs.shape[-1], kernel_size=1)(x)
    return x + res


def build_model(
    input_shape,
    head_size,
    num_heads,
    ff_dim,
    num_transformer_blocks,
    mlp_units,
    classes,
    dropout=0,
    mlp_dropout=0,
):
    inputs = keras.Input(shape=input_shape)
    x = inputs
    for _ in range(num_transformer_blocks):
        x = transformer_encoder(x, head_size, num_heads, ff_dim, dropout)

    x = layers.GlobalAveragePooling1D(data_format="channels_first")(x)
    for dim in mlp_units:
        x = layers.Dense(dim, activation="relu")(x)
        x = layers.Dropout(mlp_dropout)(x)
    action = layers.Dense(classes, activation="softmax")(x)
    critic = layers.Dense(1)(x)
    return keras.Model(inputs, [action, critic])
