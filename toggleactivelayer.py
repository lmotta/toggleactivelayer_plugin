# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Toggle Active Layer
Description          : Plugin for toggle visibility of active layer
Date                 : June, 2015
copyright            : (C) 2015 by Luiz Motta
email                : motta.luiz@gmail.com

 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Luiz Motta'
__date__ = '2015-06-01'
__copyright__ = '(C) 2018, Luiz Motta'
__revision__ = '$Format:%H$'


from qgis.PyQt.QtCore import Qt, QCoreApplication
from qgis.PyQt.QtGui import QCursor

from qgis.gui import QgsMessageBar, QgsMapTool
from qgis.core import QgsLayerTreeLayer, QgsLayerTreeGroup, QgsLayerTree

from .visibilitylayers import VisibilityLayers

from .translate import Translate

class ToggleActiveLayerTool(QgsMapTool):
    def __init__(self, iface):
        super().__init__( iface.mapCanvas() )
        self.view = iface.layerTreeView()
        self.msgBar = iface.messageBar()
        self.pluginName = 'ToggleActiveLayer'
        self.vl = VisibilityLayers( self.pluginName )
        self.setCursor( QCursor( Qt.PointingHandCursor ) )
        self.translate = Translate( self.pluginName.lower() )

    def hasVisibleChildren(self, node):
        for child in node.children():
            if child.itemVisibilityChecked():
                return self.hasVisibleChildren( child )
            else:
                return False
        return True

    def hasVisibleParent(self, node):
        parent = node.parent()
        if isinstance( parent , QgsLayerTree ): # Root legend
            return True
        if not parent.itemVisibilityChecked():
            return False
        return self.hasVisibleParent( parent )

    def canvasPressEvent(self, e):
        self.msgBar.popWidget()
        node = self.view.currentNode()
        if not node.itemVisibilityChecked():
            f = QCoreApplication.translate('ToggleActiveLayer', "'{}' isn't visible")
            msg = f.format( node.name() )
            self.msgBar.pushWarning( self.pluginName, msg )
            return
        if not self.hasVisibleParent( node ):
            f = QCoreApplication.translate('ToggleActiveLayer', "'{}' don't have visible parents" )
            msg = f.format( node.name() )
            self.msgBar.pushWarning( self.pluginName, msg )
            return
        if isinstance( node , QgsLayerTreeLayer):
            if not node.layer().isSpatial():
                f = QCoreApplication.translate('ToggleActiveLayer', "'{}' is not spatial layer(Vector or Raster)")
                msg = f.format( node.name() )
                self.msgBar.pushWarning( self.pluginName, msg )
                return
            f = QCoreApplication.translate('ToggleActiveLayer', "Active layer is '{}'." )
        else:
            if not self.hasVisibleChildren( node ):
                f = QCoreApplication.translate('ToggleActiveLayer', "'{}' don't have visible children" )
                msg = f.format( node.name() )
                self.msgBar.pushWarning( self.pluginName, msg )
                return
            f = QCoreApplication.translate('ToggleActiveLayer', "Active group is '{}'." )
        
        if not self.vl.nodeRoot == node:
            msg = f.format( node.name() )
            self.msgBar.pushInfo( self.pluginName, msg )

        self.vl.animationOpacity( node, 1 )

    def canvasReleaseEvent(self, e):
        self.vl.cancel()

    def deactivate(self):
        super().deactivate()
        self.deactivated.emit()
