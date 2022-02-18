from keras.models import load_model


class Model:
    """
    The abstract model for machine learning
    """
    def __init__(self, name=None, filepath=None):
        self.name = name
        self.filepath = filepath

    def _create(self):
        try:
            model = load_model(self.filepath)
            print('-----------load Ai models from backuped files!------------')
        except Exception:
            model = self._new_model()

        self.model = model

    def _new_model(self):
        raise NotImplementedError


    def save(self):
        self.model.save(self.filepath, save_format='h5')
