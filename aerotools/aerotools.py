from .Curve import Curve
from .Plot import Plot
from .Compute import Compute
from .Figure import Figure


class aerotools:
    def __init__(self, args):
        self.args = self.__checkargs(args)
        self.compute = Compute()
        self.figList = self.__genFigs()

    def runFigs(self):
        # Length check
        for i, fig in enumerate(self.figList):
            graph = Plot(**self.args['graph'])
            for l in fig.curveList:
                graph.addCurves(l)
            pathName = self.args['graph']['savedirectory'] + self.args['graph']['savefilename'] + '_' + str(i)+'.'+ self.args['graph']['format']
            graph.display(pathName)
    
    def loadSections(self, curvesArgs):
        """
        Loads the sections from the sections file. File format : slice_i.ext

        Returns:
            A list of all sections.

        """
        import numpy as np
        import os

        sections = []
        i = 0
        while True:
            try:
                section = np.loadtxt(f"{curvesArgs['path']}/slice_{i}.{curvesArgs['extention']}", skiprows=curvesArgs['skiprows'], delimiter=curvesArgs['delimiter'])
                sections.append(section)
                i+=1
            except FileNotFoundError:
                if len(sections) > 0:
                    break
                else:
                    raise RuntimeError(f"No sections found in {os.path.basename(os.path.normpath(curvesArgs['path']))}/")
            except Exception as e:
                raise RuntimeError(e)
        
        # Create a mask on NaNs and remove them
        if curvesArgs['checkCurve']:
            for i in range(len(sections)):
                mask = np.isnan(sections[i])
                mask = np.any(mask, axis=1)
                sections[i] = sections[i][~mask]

        print(f"Loaded {len(sections)} '{curvesArgs['type']}' sections in {os.path.basename(os.path.normpath(curvesArgs['path']))}/")
        return sections
    
    def __genFigs(self):
        # Create a list of list of curves
        listofListofCurves = []
        for curveArgs in self.args['curves']:
            listofListofCurves.append(self.__genCurves(curveArgs))
        
        # Put them in Figure objects
        figList = []
        for iFig in range(len(listofListofCurves[0])):
            fig = Figure(self.args['graph'])
            for iCurve in range(len(listofListofCurves)):
                fig.addCurve(listofListofCurves[iCurve][iFig])
            figList.append(fig)
        
        self.nFigs = len(figList)
        self.nCurves = len(figList[0].curveList)
        print(f"Generated {self.nFigs} figures with {self.nCurves} curves each.")
        return figList
    
    def __genCurves(self, curvesArgs):
        """
        Load curves from a folder.
        """
        import numpy as np
        if 'path' in curvesArgs: # Load curves from a folder
            sections = self.loadSections(curvesArgs) # Generate list of curves
        else: # Load curves from data
            sections = []
            if 'data' not in curvesArgs:
                raise ValueError("No data specified")
            for d in curvesArgs['data']:
                sections.append(d)

        curveList = []
        from .Curve import Curve
        for sec in sections:
            curveList.append(Curve(sec, curvesArgs))
        return curveList
    
    def __checkargs(self, args):

        # Graph
        if 'savedirectory' not in args['graph']:
            args['graph']['savedirectory'] = ''
        
        # Curves
        if 'curves' not in args:
            raise ValueError("No curves specified")
        
        for curveArgs in args['curves']:
            if 'extention' not in curveArgs:
                curveArgs['extention'] = 'dat'
            if 'checkCurve' not in curveArgs:
                curveArgs['checkCurve'] = False
        return args
