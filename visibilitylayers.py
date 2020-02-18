# -*- coding: utf-8 -*-
from time import sleep

from qgis.PyQt.QtCore import QObject, pyqtSlot, pyqtSignal

from qgis.core import (
    Qgis, QgsApplication,
    QgsLayerTreeLayer, QgsLayerTree,
    QgsTask
)


class VisibilityLayers(QObject):
    _visibility = pyqtSignal(float)
    def __init__(self, title):
        super().__init__()
        self.taskManager = QgsApplication.taskManager()
        self.title = title
        self.cancelTask = False
        self.nodeRoot, self.nameRoot = None, None# _setNodeRoot
        self._visibility.connect( self._setVisibility )

    @pyqtSlot(float)
    def _setVisibility(self, checked):
        self.nodeRoot.setItemVisibilityChecked( checked )

    def _setNodeRoot(self, nodeRoot):
        self.cancelTask = True # Cancel animation opacity

        # node, name
        self.nodeRoot = nodeRoot
        name = nodeRoot.name()
        self.nameRoot = name
        name = f"* {self.title} - {name}"
        nodeRoot.setName( name )

    def _restoreVisibility(self):
        self.nodeRoot.setName( self.nameRoot )
        self.nodeRoot.setItemVisibilityChecked( True )

    def animationOpacity(self, nodeRoot, second):
        def run(task):
            checked = False
            while True:
                if self.cancelTask or task.isCanceled():
                    break
                self._visibility.emit( checked )
                sleep( second )
                checked = not checked

        def finished(exception, result=None):
            self._restoreVisibility()

        self._setNodeRoot( nodeRoot ) # Cancel animation opacity
        self.cancelTask = False
        task = QgsTask.fromFunction( self.title, run, on_finished=finished )
        layers = [ nodeRoot.layer() ] if isinstance( nodeRoot , QgsLayerTreeLayer ) \
            else [ ltl.layer() for ltl in nodeRoot.findLayers() if ltl.itemVisibilityChecked() ]
        task.setDependentLayers( layers )
        self.taskManager.addTask( task )

    def cancel(self):
        self.cancelTask = True
