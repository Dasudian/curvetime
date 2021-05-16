from .model import Model
from tensorflow.keras import layers
from tensorflow import keras
from curvetime.env.stock_env import WINDOW_SIZE, TOTAL_STOCKS, FEATURES_PER_STOCK


MODEL_PATH = 'data/models/model.h5'

class StockModel(Model):
    """
    The model for stock price analysis
    """
    def __init__(self, env, name='StockModel', filepath=MODEL_PATH):
        super().__init__(name, filepath)
        self.input_shape = env.shape
        self.num_actions = env.num_actions
        self.name = name
        self.filepath = filepath
        self._create()


    def _create(self):
        try:
            model = load_model(self.filepath)
        except Exception:
            model = self._new_model()

        self.model = model

    def _new_model(self):
        """
        input_shape = (rows, cols, channels)
        """
        inputs = layers.Input(shape=self.input_shape)
        layer1 = layers.Conv2D(64, 5, strides=1, activation="relu")(inputs)
        layer2 = layers.Conv2D(128, 4, strides=1, activation="relu")(layer1)
        layer3 = layers.Conv2D(256, 3, strides=1, activation="relu")(layer2)
        layer4 = layers.Conv2D(512, 3, strides=1, activation="relu")(layer3)
        layer5 = layers.Flatten()(layer4)
        layer6 = layers.Dense(512, activation="relu")(layer5)
        layer7 = layers.Dense(1024, activation="relu")(layer6)
        layer8 = layers.Dense(512, activation="relu")(layer7)
        action = layers.Dense(self.num_actions, activation="linear")(layer8)
        model = keras.Model(inputs=inputs, outputs=action)
        optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)
        model.compile(optimizer=optimizer, loss='huber_loss')
        return model
