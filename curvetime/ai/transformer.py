from tensorflow_docs.vis import embed
from tensorflow.keras import layers
from tensorflow import keras
from tensorflow.keras.models import load_model

import tensorflow as tf
import pandas as pd
import numpy as np


from .model import Model
from curvetime.env.stock_env import WINDOW_SIZE, TOTAL_STOCKS, FEATURES_PER_STOCK


MODEL_PATH = 'data/models/model.h5'
MAX_SEQ_LENGTH = 100   #same as the SEQ_LENGTH in stock_env
NUM_FEATURES = 2048

class Transformer(Model):
    """
    The model for stock price analysis
    """
    def __init__(self, env, name='StockModel', filepath=MODEL_PATH, dense_dim=4, num_heads=8):
        super().__init__(name, filepath)
        self.input_shape = env.shape
        self.num_actions = env.num_actions
        self.name = name
        self.filepath = filepath
        self.dense_dim = dense_dim
        self.num_heads = num_heads
        self._create()


    def _create(self):
        try:
            model = load_model(self.filepath)
        except Exception:
            model = self._new_model()

        self.model = model

    def _new_model(self):
        seq_length = MAX_SEQ_LENGTH
        embed_dim = NUM_FEATURES
        classes = self.num_actions

        inputs = keras.Input(shape=(None, None))
        x = PositionalEmbedding(
        seq_length, embed_dim, name="frame_position_embedding")(inputs)
        x = TransformerEncoder(embed_dim, self.dense_dim, self.num_heads, name="transformer_layer")(x)
        x = layers.GlobalMaxPooling1D()(x)
        x = layers.Dropout(0.5)(x)
        outputs = layers.Dense(classes, activation="softmax")(x)
        model = keras.Model(inputs, outputs)

        model.compile(
            optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
        )
        return model


    def build_feature_extractor(self, shape):
        feature_extractor = keras.applications.NASNetLarge(
            weights=None,
            include_top=False,
            pooling="avg",
            input_shape=shape,
        )
        preprocess_input = keras.applications.nasnet.preprocess_input

        inputs = keras.Input(shape)
        preprocessed = preprocess_input(inputs)

        outputs = feature_extractor(preprocessed)
        return keras.Model(inputs, outputs, name="feature_extractor")


    def frames_to_features(self, frames):
        feature_extractor = self.build_feature_extractor(frames[0].shape)
        # Initialize placeholder to store the features of the current video.
        temp_frame_features = np.zeros(
            shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32"
        )

        # Extract features from the frames of the current video.
        for i, batch in enumerate(frames):
            video_length = batch.shape[0]
            length = MAX_SEQ_LENGTH
            for j in range(length):
                if np.mean(batch[j, :]) > 0.0:
                    temp_frame_features[i, j, :] = feature_extractor.predict(
                        batch[None, j, :]
                    )

                else:
                    temp_frame_features[i, j, :] = 0.0
        return temp_frame_features.squeeze()


class PositionalEmbedding(layers.Layer):
    def __init__(self, sequence_length, output_dim, **kwargs):
        super().__init__(**kwargs)
        self.position_embeddings = layers.Embedding(
            input_dim=sequence_length, output_dim=output_dim
        )
        self.sequence_length = sequence_length
        self.output_dim = output_dim

    def call(self, inputs):
        # The inputs are of shape: `(batch_size, frames, num_features)`
        length = tf.shape(inputs)[1]
        positions = tf.range(start=0, limit=length, delta=1)
        embedded_positions = self.position_embeddings(positions)
        return inputs + embedded_positions

    def compute_mask(self, inputs, mask=None):
        mask = tf.reduce_any(tf.cast(inputs, "bool"), axis=-1)
        return mask


class TransformerEncoder(layers.Layer):
    def __init__(self, embed_dim, dense_dim, num_heads, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.dense_dim = dense_dim
        self.num_heads = num_heads
        self.attention = layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=embed_dim, dropout=0.3
        )
        self.dense_proj = keras.Sequential(
            [layers.Dense(dense_dim, activation=tf.nn.gelu), layers.Dense(embed_dim),]
        )
        self.layernorm_1 = layers.LayerNormalization()
        self.layernorm_2 = layers.LayerNormalization()

    def call(self, inputs, mask=None):
        if mask is not None:
            mask = mask[:, tf.newaxis, :]

        attention_output = self.attention(inputs, inputs, attention_mask=mask)
        proj_input = self.layernorm_1(inputs + attention_output)
        proj_output = self.dense_proj(proj_input)
        return self.layernorm_2(proj_input + proj_output)



