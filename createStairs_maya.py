try:
  from PySide2.QtCore import * 
  from PySide2.QtGui import * 
  from PySide2.QtWidgets import *
  from PySide2 import __version__
  from shiboken2 import wrapInstance 
except ImportError:
  from PySide.QtCore import * 
  from PySide.QtGui import * 
  from PySide import __version__
  from shiboken import wrapInstance 

from maya import cmds
from maya import OpenMayaUI as omui 

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget) 

class CreateStairsUI(QWidget):  
    def __init__(self, *args, **kwargs):        
        super(CreateStairsUI, self).__init__(*args, **kwargs)   
        self.setParent(mayaMainWindow)
        self.setWindowFlags(Qt.Window)

        self.__stepWidth=1
        self.__stepHeight=1
        self.__stepDepth=1
        self.__curvature=0
      
        self.setObjectName('StairUI_uniqueId')        
        self.setWindowTitle('Procedural Stairs')
        self.setMinimumWidth(300)
        
        self.initUI() 

        layout=QVBoxLayout()
        self.setLayout(layout)
        # Steps widget
        stepsWidget=QWidget()
        # Set horizontal layout
        stepsLayout=QHBoxLayout()
        stepsWidget.setLayout(stepsLayout)
        stepsLabel=QLabel('Number of steps')
        self.stepsSpinBox=QSpinBox()
        self.stepsSpinBox.setMinimum(2)
        self.stepsSpinBox.valueChanged.connect(self.createStair)
        stepsLayout.addWidget(stepsLabel)
        stepsLayout.addWidget(self.stepsSpinBox)
        # Width widget
        widthWidget=QWidget()
        widthLayout=QHBoxLayout()
        widthWidget.setLayout(widthLayout)
        widthLabel=QLabel('Step width')
        self.widthSpinBox=QDoubleSpinBox()
        self.widthSpinBox.setMinimum(1)
        self.widthSpinBox.setValue(1)
        self.widthSpinBox.valueChanged.connect(self.updateWidth)
        widthLayout.addWidget(widthLabel)
        widthLayout.addWidget(self.widthSpinBox)
        # Depth widget
        depthWidget=QWidget()
        depthLayout=QHBoxLayout()
        depthWidget.setLayout(depthLayout)
        depthLabel=QLabel('Step depth')
        self.depthSpinBox=QDoubleSpinBox()
        self.depthSpinBox.setMinimum(0.1)
        self.depthSpinBox.setSingleStep(0.1)
        self.depthSpinBox.setValue(1)
        self.depthSpinBox.valueChanged.connect(self.updateDepth)
        depthLayout.addWidget(depthLabel)
        depthLayout.addWidget(self.depthSpinBox)        
        # Height widget
        heightWidget=QWidget()
        heightLayout=QHBoxLayout()
        heightWidget.setLayout(heightLayout)
        heightLabel=QLabel('Step height')
        self.heightSpinBox=QDoubleSpinBox()
        self.heightSpinBox.setMinimum(0.1)
        self.heightSpinBox.setSingleStep(0.1)
        self.heightSpinBox.setValue(1)
        self.heightSpinBox.valueChanged.connect(self.updateHeight)
        heightLayout.addWidget(heightLabel)
        heightLayout.addWidget(self.heightSpinBox)
        # Add all of our widget to the main widget, which has a vertical layout defined way up in line 105
        layout.addWidget(stepsWidget)
        layout.addWidget(depthWidget)
        layout.addWidget(widthWidget)
        layout.addWidget(heightWidget)

    def getChildrenInputs(self):
        '''
        Returns the inputs for every cube, so we can modify width, height, depth and subdivision level
        '''
        inputs=[]
        if cmds.objExists('StairGroup'):
            getStepGroups=self.getChildren()
            for stepGroup in getStepGroups:
                inputs.append(cmds.listConnections(cmds.listRelatives(cmds.listRelatives(stepGroup)))[1])
        return inputs   

    def getChildren(self):
        '''
        Returns the bunch of groups inside the StairGroup
        '''
        if cmds.objExists('StairGroup'):
            return cmds.listRelatives('StairGroup')

    def updateWidth(self, value):
        '''
        Iterates through the StairGroup children and modifies the width accordingly to the new value of the ui.
        We only get the inputs, since we will not modify the children groups of StairGroup directly.
        '''
        self.stepWidth=value
        getInputs=self.getChildrenInputs()
        for polyInput in getInputs:
            cmds.setAttr('%s.width' % polyInput, self.stepWidth)
            if self.stepWidth>1:
                cmds.setAttr('%s.subdivisionsWidth' % polyInput, self.stepWidth)

    def updateDepth(self, value):
        '''
        Iterates through the StairGroup children and modifies the depth accordingly to the new value of the ui.
        Gets both inputs and children, since we need the children groups of StairGroup to modify its translation Z.
        '''
        self.stepDepth=value
        count=1
        getInputs=self.getChildrenInputs()
        getChildren=self.getChildren()
        for polyInput in getInputs:
            cmds.setAttr('%s.depth' % polyInput, self.stepDepth)
            if self.stepDepth>1:
                cmds.setAttr('%s.subdivisionsDepth' % polyInput, self.stepDepth)
            cmds.setAttr('%s.tz' % getChildren[count-1], self.stepDepth*count)
            count+=1

    def updateHeight(self, value):
        '''
        Iterates through the StairGroup children and modifies the height accordingly to the new value of the ui.
        Gets both inputs and children, since we need the children groups of StairGroup to modify its translation Y.
        '''
        self.stepHeight=value
        count=1
        getInputs=self.getChildrenInputs()
        getChildren=self.getChildren()
        for polyInput in getInputs:
            cmds.setAttr('%s.height' % polyInput, self.stepHeight)
            if self.stepHeight>1:
                cmds.setAttr('%s.subdivisionsHeight' % polyInput, self.stepHeight)
            cmds.setAttr('%s.ty' % getChildren[count-1], self.stepHeight*count)
            count+=1

    # Getters and setters
    @property
    def curvature(self):
        return self.__curvature

    @curvature.setter
    def curvature(self, curvature):
        self.__curvature=curvature

    @property
    def stepWidth(self):
        return self.__stepWidth

    @stepWidth.setter
    def stepWidth(self, stepWidth):
        self.__stepWidth=stepWidth

    @property
    def stepDepth(self):
        return self.__stepDepth

    @stepDepth.setter
    def stepDepth(self, stepDepth):
        self.__stepDepth=stepDepth

    @property
    def stepHeight(self):
        return self.__stepHeight

    @stepHeight.setter
    def stepHeight(self, stepHeight):
        self.__stepHeight=stepHeight

    def createStair(self, value):
        '''
        Main function that procedurally creates a bunch of cubes and sets them according to the values of the ui.
        '''
        if not cmds.objExists('StairGroup'):
            stairGroup=cmds.group(n='StairGroup', em=True)
        else:
            cmds.delete(cmds.listRelatives('StairGroup'))
            stairGroup='StairGroup'
        
        for step in range(1,value+1):
            stepGroup=cmds.group(n='StepGroup_%s' % (str(step)), em=True)
            stepCube=cmds.polyCube(n='Step_%s' % (str(step)), w=1, h=1, d=1, sx=1, sy=1, sz=1, ax=(0,1,0), cuv=4, ch=1)
            cmds.parent(stepCube, stepGroup)
            cmds.setAttr('%s.ty' % stepGroup, self.__stepHeight*step)
            cmds.setAttr('%s.tz' % stepGroup, self.__stepDepth*step)
            cmds.parent(stepGroup, stairGroup)
        self.updateHeight(self.__stepHeight)
        self.updateWidth(self.__stepWidth)
        self.updateDepth(self.__stepDepth)

# Create a new instance of our main class and show it though the QtGui.QWidget.show() definition. 
CreateStairsUI().show()