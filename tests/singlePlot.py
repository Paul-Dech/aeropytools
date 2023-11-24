def main():
    from aerotools import aerotools
    import os
    import numpy as np
    from scipy.interpolate import interp1d
    thisdir = os.path.split(os.path.abspath(__file__))[0] + '/'

    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)

    xp = np.linspace(0, 2*np.pi, 10)
    yp = interp1d(x, y)(xp)

    args = {'graph': {'type': 'presentation',
                      'xlabel': 'Frequency [Hz]',
                      'ylabel': 'Amplitude [-]',
                      'save': True,
                      'format': 'pdf',
                      'legendOn': True,
                      'removeTRaxis': True,
                      'savefilename': 'sinwave'},
            'curves': [{'name': 'Base',
                        'data': [np.column_stack((x, y))],
                        'color': 'darkblue',
                        'ls': ':'},
                       {'name': 'Interpolation',
                        'ls': '',
                        'data': [np.column_stack((xp, yp))],
                        'color': 'red',
                        'mt': 'x',
                        'ms': 10,
                        'lw': 6}
                        ],
            }
    driver = aerotools(args)
    driver.runFigs()

if __name__ == '__main__':
    main()