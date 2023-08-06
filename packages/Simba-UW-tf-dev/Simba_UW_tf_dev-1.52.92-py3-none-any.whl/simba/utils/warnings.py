import warnings

class SimBAWarning(Warning):
    pass

class BENTOWarning(SimBAWarning):
    def __init__(self, msg):
        super().__init__()
        print(f'BENTO WARNING: {msg}')
        #warnings.warn('message', warning1)