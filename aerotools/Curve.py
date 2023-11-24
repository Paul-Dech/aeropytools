class Curve:
    def __init__(self, data, args):
        self.type = type
        self.args = self.__initArgs(args)
        self.x = data[:,args['dataColumn'][0]] * args['scaleData'][0]
        self.y = data[:,args['dataColumn'][1]] * args['scaleData'][1]

    def setArgs(self, newArgs:dict):
        for key in newArgs:
            self.args[key] = newArgs[key]

    def __initArgs(self, args):
        if 'type' not in args:
            args['type'] = 'default'
        defaults = self.__defaultsParameters()
        if 'dataColumn' not in args:
            args['dataColumn'] = [0, 1]
        if 'scaleData' not in args:
            args['scaleData'] = [1, 1]
        if 'name' not in args:
            args['name'] = 'Data'
        
        # Look for missing parameters and set them to default values
        # All parameters can be overriden by the user
        for key in defaults:
            if key not in args:
                args[key] = defaults[key]
        return args

    def __defaultsParameters(self):
        if type == 'experimental':
            return {'ls': '',
                    'mt': 'x',
                    'lw': 3,
                    'color': 'black',
                    'ms': 6}
        if type == 'dartvii':
            return {'ls': '-',
                    'lw': 3,
                    'mt': None,
                    'color': 'darkblue',
                    'ms': 4}
        if type == 'dartinviscid':
            return {'ls': '--',
                    'lw': 3,
                    'mt': None,
                    'color': 'darkblue',
                    'ms': 4}
        if type == 'rans':
            return {'ls': '-',
                    'lw': 3,
                    'mt': None,
                    'color': 'firebrick',
                    'ms': 4}
        else:
            # Defaults parameters
            return {'ls': '-',
                    'lw': 3,
                    'color': 'black',
                    'ms': 4,
                    'mt': 3}
