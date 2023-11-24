class Figure:
    def __init__(self, argsGraph):
        self.args = argsGraph
        self.curveList = []
    
    def addCurve(self, curve):
        self.curveList.append(curve)
