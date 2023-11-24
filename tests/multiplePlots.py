def main():
    from aerotools import aerotools
    import os
    import numpy as np
    thisdir = os.path.split(os.path.abspath(__file__))[0] + '/'
    args = {'graph': {'type': 'article',
                      'xlim': [0, 1],
                      'xlabel': 'x/c',
                      'ylabel': 'Cp',
                      'removeTRaxis': True,
                      'inverse_y': True,
                      'save': True,
                      'format': 'png',
                      'savefilename': 'test'},
            'curves': [{'name': 'Experimental',
                        'type': 'experimental',
                        'path': thisdir+'ressources/experimental',
                        'dataColumn': [0, 1],
                        'scaleData': [1/100, 1],
                        'skiprows': 1,
                        'delimiter': ','},
                       {'name': 'RANS',
                        'type': 'rans',
                        'path': thisdir+'ressources/rans',
                        'dataColumn': [3, 4],
                        'skiprows': 1,
                        'delimiter': ','}
                        ],
            }
    driver = aerotools(args)
    driver.runFigs()

if __name__ == '__main__':
    main()