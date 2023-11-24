import numpy as np
import os
from matplotlib import pyplot as plt

class Plot:
    def __init__(self, **kwargs):
        """Init the plot object
        """
        self.args = self.__checkargs(**kwargs)
        self.fig = plt.figure()
        self.curveList = []

    def addCurves(self, curveList):
        """Add curves to the plot object
        """
        self.curveList.append(curveList)

    def display(self, path=None):
        if self.args['save']:
            self.__save(path)
        else:
            self.__show()

    def __save(self, path):
        """Save the plot object in different formats
        """
        print('Saving figure '+os.path.basename(path), end='... ')
        if self.args['xlim'] is not None or self.args['ylim'] is not None:
            self.__cleanCurves()
        if self.args['format'] != 'tex':
            self.__plotFig()
            plt.savefig(path)
        elif self.args['format'] == 'tex':
            self.__plotFig()
            self.__writeTexfile(path)
            self.__removeAxis(path)
        print('done.')

    def __show(self):
        """Show the plot object
        """
        plt.clf()
        if self.args['xlim'] is not None or self.args['ylim'] is not None:
            self.__cleanCurves()
        self.__plotFig()
        plt.show()

    def __checkargs(self, **args):
        """Check input arguments and set them to default
        """
        if 'xlim' not in args:
            args['xlim'] = None
        if 'ylim' not in args:
            args['ylim'] = None
        if 'gridOn' not in args:
            args['gridOn'] = False
        if 'xlabel' not in args:
            args['xlabel'] = ''
        if 'ylabel' not in args:
            args['ylabel'] = ''
        if 'legendOn' not in args:
            args['legendOn'] = False
        if 'inverse_y' not in args:
            args['inverse_y'] = False
        if 'inverse_x' not in args:
            args['inverse_x'] = False
        if 'removeTRaxis' not in args:
            args['removeTRaxis'] = False
        if 'legendLoc' not in args:
            args['legendLoc'] = 'best'
        return args

    def __plotFig(self):
        """Plot the figure using the curves in pyplot
        """
        if self.curveList is None:
            raise RuntimeError('Init curves before plotting.')

        for curve in self.curveList:
            plt.plot(curve.x, curve.y, ls=curve.args['ls'], marker=curve.args['mt'], lw=curve.args['lw'],
                     ms=curve.args['ms'], color=curve.args['color'], label=curve.args['name'])
        if self.args['legendOn'] is True:
            plt.legend(loc=self.args['legendLoc'], frameon=False)
        if self.args['xlim'] is not None:
            plt.xlim(self.args['xlim'])
        if self.args['ylim'] is not None:
            plt.ylim(self.args['ylim'])
        if self.args['inverse_y']:
            plt.gca().invert_yaxis()
        if self.args['inverse_x']:
            plt.gca().invert_xaxis()
        if self.args['removeTRaxis']:
            for s in ['top', 'right']:
                plt.gca().spines[s].set_visible(False)

        plt.grid(self.args['gridOn'])
        plt.xlabel(self.args['xlabel'])
        plt.ylabel(self.args['ylabel'])
        self.plotted = True

    def __writeTexfile(self, path):
        """Write a tex file from the pyplot figure
        using tikzplotlib
        """
        import tikzplotlib
        tikzplotlib.clean_figure()
        tikzplotlib.save(path)
        self.__removeAxis(path)

    def __removeAxis(self, path):
        """Remove axis from the tex file by modifying the file
        """
        print('Removing axis of '+os.path.basename(path), end='... ')
        iLine = 0
        with open(path, "r+") as f:
            for line in f.readlines():
                if 'begin{axis}' in line:
                    currentLine = line
                    line_to_write = iLine
                    break
                iLine += 1

        with open(path, 'r') as file:
            lines = file.readlines()

        if len(lines) > int(line_to_write):
            lines[line_to_write] = currentLine + \
                'axis x line*=bottom,\naxis y line*=left,\n'

        with open(path, 'w') as file:
            file.writelines(lines)
        print('done.')

    def __cleanCurves(self):
        """Clean curves data according to xlim and ylim
        """
        for curv in self.curveList:
            data = np.column_stack((curv.x, curv.y))
            if self.args['xlim'] is not None:
                data = data[data[:, 0] >= self.args['xlim'][0], :]
                data = data[data[:, 0] <= self.args['xlim'][1], :]
            if self.args['ylim'] is not None:
                data = data[data[:, 1] >= self.args['ylim'][0], :]
                data = data[data[:, 1] <= self.args['ylim'][1], :]
            curv.x = data[:, 0]
            curv.y = data[:, 1]
