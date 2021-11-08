from argparse import Namespace

class MyNamespace(Namespace):
    def __init__(self):
        super().__init__()
    
    def getInputDict(self):
        '''
        Returns a dict of all inputted options.
        '''
        output = {}
        for kwarg in self._get_kwargs():
            output[kwarg[0]] = kwarg[1]
        
        return output

    def getAuxilliaryInputDict(self):
        '''
        Returns a dict of all inputted options, minus command
        '''
        output = {}
        for kwarg in self._get_kwargs()[1:]:
            output[kwarg[0]] = kwarg[1]
        
        return output