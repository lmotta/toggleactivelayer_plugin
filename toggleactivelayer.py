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

from PyQt4.QtCore import ( Qt )
from PyQt4.QtGui import ( QCursor )

from qgis.gui import ( QgsMessageBar, QgsMapTool )
from qgis.core import ( QgsLayerTreeLayer )

class ToggleActiveLayerMapTool(QgsMapTool):
  def __init__(self, iface):
    super(ToggleActiveLayerMapTool, self).__init__( iface.mapCanvas() )
    self.view = iface.layerTreeView()
    self.msgBar = iface.messageBar()
    self.checkState = self.layerNode = None
    self.setCursor( QCursor( Qt.CrossCursor ) )

  def canvasPressEvent(self, e):
    self.layerNode  = None
    node = self.view.currentNode()
    if not isinstance( node , QgsLayerTreeLayer):
      msg = "Select active layer in legend."
      self.msgBar.pushMessage( "ToggleActiveLayerMapTool", msg, QgsMessageBar.WARNING, 4 )
      return

    self.checkState = Qt.Checked if node.isVisible() == Qt.Unchecked else Qt.Unchecked
    node.setVisible( self.checkState )
    self.layerNode = node

  def canvasReleaseEvent(self, e):
    if self.layerNode is None:
      return

    self.checkState = Qt.Checked if self.checkState == Qt.Unchecked else Qt.Unchecked
    self.layerNode.setVisible( self.checkState )

  def deactivate(self):
      super( ToggleActiveLayerMapTool, self ).deactivate()
      self.deactivated.emit()

