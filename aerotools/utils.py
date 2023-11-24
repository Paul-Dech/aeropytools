from .Plot import Plot

def initGraph(**argsGraph):
    """
    Initializes a graph with the given arguments.

    Args:
        **argsGraph: Keyword arguments for initializing the graph.

    Returns:
        An instance of the Plot class.

    """
    return Plot(**argsGraph)

def plotSections(list, save=False, filename=None, format='png', **argsGraph):
    """
    Plot sections from a list of curves. Figure i will have curves [el0[i], el1[i], ...] in it.

    Args:
        list (list): List of curves to plot.
        filename (str): Name of the file to save the plot.
        save (bool, optional): Flag indicating whether to save the plot or not. Defaults to False.
        format (str, optional): Format of the saved plot file. Defaults to '.png'.
        **argsGraph: Additional arguments to be passed to the initGraph function.

    Raises:
        ValueError: If the lengths of all lists in the input list are not the same.

    Returns:
        None
    """

    # Length check
    if not all(len(lst) == len(list[0]) for lst in list):
        raise ValueError("All lists must have the same length")
    if save and filename is None:
        raise ValueError("Filename must be specified when saving the plot")

    for i in range(len(list[0])):
        graph = initGraph(**argsGraph)
        for l in list:
            graph.addCurves(l[i])
        if save:
            graph.save(filename+'_'+str(i), type=format)
        else:
            graph.show()

def loadSections(pathToFolder, skiprows=1, delimiter=',', ext='.dat', checkData=True):
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
            section = np.loadtxt(f"{pathToFolder}/slice_{i}{ext}", skiprows=skiprows, delimiter=delimiter)
            sections.append(section)
            i += 1
        except FileNotFoundError:
            if len(sections) > 0:
                break
            else:
                raise RuntimeError(f"No sections found in {os.path.basename(os.path.normpath(pathToFolder))}/")
        except Exception as e:
            raise RuntimeError(e)
    
    # Create a mask on NaNs and remove them
    for i in range(len(sections)):
        mask = np.isnan(sections[i])
        mask = np.any(mask, axis=1)
        sections[i] = sections[i][~mask]

    print(f"Loaded {len(sections)} sections in {os.path.basename(os.path.normpath(pathToFolder))}/")
    return sections

def loadCurves(pathToFolder, name, type, dataColumn=[0, 1], skiprows=1, delimiter=',', ext='.dat'):
    """
    Load curves from a folder.

    Args:
        pathToFolder (str): Path to the folder containing the curves.
        name (str): Name of the curves.
        type (str): Type of the curves.
        dataColumn (list, optional): Indices of the columns containing the data. Defaults to [0, 1].
        skiprows (int, optional): Number of rows to skip in the data file. Defaults to 1.
        delimiter (str, optional): Delimiter used in the data file. Defaults to ','.
        ext (str, optional): File extension of the data files. Defaults to '.dat'.

    Returns:
        list: List of Curve objects.
    """
    sections = loadSections(pathToFolder, skiprows=skiprows, delimiter=delimiter, ext=ext) # Generate list of curves
    curveList = []
    from .Curve import Curve
    for sec in sections:
        curveList.append(Curve(sec[:,dataColumn], name=name, type=type))
    return curveList

def compute3DAeroCoeffFromFiles(sections, alpha, pathToCpFolder, pathToCfFolder=None, skiprows=1, delimiter=',', ext='.dat'):
    """Load sections and compute aeroCoefficients
    """
    import numpy as np
    Cl3D = 0
    Cd3D = 0
    Cm3D = 0
    cpSections = loadSections(pathToCpFolder, skiprows=skiprows, delimiter=delimiter, ext=ext)
    for isec, c in enumerate(cpSections):
        ynext = sections[isec] if isec < len(sections) else 1
        yprev = sections[isec-1] if isec > 0 else 0
        dy = ynext - yprev
        (cl, cd, cm) = compute2DAeroCoeffFromCp(alpha*np.pi/180, c[:,0], c[:,1])
        Cl3D += cl*dy
        Cd3D += cd*dy
        Cm3D += cm*dy

    if pathToCfFolder is not None:
        cfSections = loadSections(pathToCfFolder, skiprows=skiprows, delimiter=delimiter, ext=ext)
        for isec, c in enumerate(cfSections):
            ynext = sections[isec] if isec < len(sections) else 1
            yprev = sections[isec-1] if isec > 0 else 0
            dy = ynext - yprev
            (cl, cd, cm) = compute2DAeroCoeffFromCp(alpha*np.pi/180, c[:,0], c[:,1])
            Cl3D += cl*dy
            Cd3D += cd*dy
            Cm3D += cm*dy
    else:
        cfSections = None
    return (Cl3D, Cd3D, Cm3D)
    
def compute2DAeroCoeffFromCp(alpha, Cp, x, y=None):
    import math
    if y is None:
        i = 0
        Cy = 0
        Cm = 0
        while i < (len(x)-1):
            dx = -(x[i+1] - x[i])
            Cy += 0.5 * dx * (Cp[i+1] + Cp[i])
            Cm -= 0.5*(Cp[i+1]*(x[i+1]-0.25) + Cp[i]*(x[i]-0.25)) * dx
            i = i+1
        Cl = Cy*math.cos(alpha)
        Cd = Cy*math.sin(alpha)
        
    else:
        import math
        i = 0
        Cy = 0
        Cx = 0
        Cm = 0 # positive nose-up (clockwise)
        while i < (len(x)-1):
            dx = -(x[i+1] - x[i])
            dy = -(y[i+1] - y[i])
            Cy += 0.5 * dx * (Cp[i+1] + Cp[i])
            Cx -= 0.5 * dy * (Cp[i+1] + Cp[i])
            Cm -= 0.5*(Cp[i+1]*(x[i+1]-0.25) + Cp[i]*(x[i]-0.25)) * dx + 0.5*(Cp[i+1]*y[i+1] + Cp[i]*y[i]) * dy
            i = i+1
        Cl = Cy*math.cos(alpha) - Cx*math.sin(alpha)
        Cd = Cy*math.sin(alpha) + Cx*math.cos(alpha)
    return (Cl, Cd, Cm)