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

from qgis.PyQt.QtCore import Qt, QCoreApplication
from qgis.PyQt.QtGui import QCursor

from qgis.gui import QgsMessageBar, QgsMapTool
from qgis.core import QgsLayerTreeLayer, QgsLayerTreeGroup, QgsLayerTree

from .translate import Translate

class ToggleActiveLayerTool(QgsMapTool):
  def __init__(self, iface):
    super().__init__( iface.mapCanvas() )
    self.view = iface.layerTreeView()
    self.node  = None
    self.msgBar = iface.messageBar()
    self.pluginName = 'ToggleActiveLayer'
    self.setCursor( QCursor( Qt.PointingHandCursor ) )
    self.translate = Translate( self.pluginName.lower() )

  def setVisibilityCheckedParents(self, node, checked):
    parent = node.parent()
    if isinstance( parent , QgsLayerTree ):
      return
    if ( checked == Qt.Checked and parent.itemVisibilityChecked() ) or ( checked == Qt.Unchecked  and not parent.itemVisibilityChecked() ):
      return
    parent.setItemVisibilityChecked( checked )
    self.setVisibilityCheckedParents( parent, checked )

  def hasVisibleChildren(self, node):
    for children in node.children():
      if children.itemVisibilityChecked():
        return True
    return False

  def canvasPressEvent(self, e):
    self.msgBar.popWidget()
    node = self.view.currentNode()
    if isinstance( node , QgsLayerTreeLayer) and not node.layer().isSpatial():
      self.node = None
      f = QCoreApplication.translate('ToggleActiveLayer', "'{}' is not spatial layer(Vector or Raster)")
      msg = f.format( node.name() )
      self.msgBar.pushWarning( self.pluginName, msg )
      return
    if isinstance( node , QgsLayerTreeGroup ) and not self.hasVisibleChildren( node ):
      self.node = None
      f = QCoreApplication.translate('ToggleActiveLayer', "'{}' don't have visible layers" )
      msg = f.format( node.name() )
      self.msgBar.pushWarning( self.pluginName, msg )
      return

    self.checkState = Qt.Checked if node.itemVisibilityChecked() == Qt.Unchecked else Qt.Unchecked
    node.setItemVisibilityChecked( self.checkState )
    if self.checkState == Qt.Checked:
      self.setVisibilityCheckedParents( node,  self.checkState )

    if not node == self.node:
      if isinstance( node , QgsLayerTreeLayer):
        f = QCoreApplication.translate('ToggleActiveLayer', "Active layer is '{}'." )
      else:
        f = QCoreApplication.translate('ToggleActiveLayer', "Active group is '{}'." )
      msg = f.format( node.name() )
      self.msgBar.pushInfo( self.pluginName, msg )
      self.node = node

  def canvasReleaseEvent(self, e):
    if self.node is None:
      return

    self.checkState = Qt.Checked if self.checkState == Qt.Unchecked else Qt.Unchecked
    self.node.setItemVisibilityChecked( self.checkState )
    if self.checkState == Qt.Unchecked:
      self.setVisibilityCheckedParents( self.node, self.checkState )

  def deactivate(self):
      super().deactivate()
      self.deactivated.emit()
