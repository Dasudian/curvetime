from tensorflow.keras import layers
from tensorflow import keras

from .model import Model
from curvetime.env.stock_env import WINDOW_SIZE, TOTAL_STOCKS, FEATURES_PER_STOCK


MODEL_PATH = 'data/models/ac_nasnet.h5'

class NasNet(Model):
    """
    The model for stock price analysis
    """
    def __init__(self, env, name='NasLarge', filepath=MODEL_PATH,
            dense_dim=256,
            dropout=0.25):
        super().__init__(name, filepath)
        self.input_shape = env.shape
        self.num_actions = env.num_actions
        self.name = name
        self.filepath = filepath
        self.dense_dim = dense_dim
        self.dropout = dropout
        self._create()

    def _new_model(self):
        baseModel = keras.applications.NASNetLarge(weights=None, include_top=False,
	input_tensor=layers.Input(shape=self.input_shape))

        # construct the head of the model that will be placed on top of the
        # the base model
        headModel = baseModel.output
        headModel = layers.AveragePooling2D(pool_size=(4, 4))(headModel)
        headModel = layers.Flatten(name="flatten")(headModel)
        headModel = layers.Dense(self.dense_dim, activation="relu")(headModel)
        headModel = layers.Dropout(self.dropout)(headModel)
        action = layers.Dense(self.num_actions, activation="softmax")(headModel)
        critic = layers.Dense(1)(headModel)
        # place the head FC model on top of the base model (this will become
        # the actual model we will train)
        model = keras.models.Model(inputs=baseModel.input, outputs=[action, critic])
        model.compile(loss="categorical_crossentropy",
                optimizer=keras.optimizers.Adam(learning_rate=1e-4),
                metrics=["accuracy"])

        return model
