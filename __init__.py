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

from qgis.PyQt.QtCore import QObject, pyqtSlot
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .toggleactivelayer import ToggleActiveLayerTool

import os

def classFactory(iface):
  return ToggleActiveLayerPlugin( iface )

class ToggleActiveLayerPlugin(QObject):

  def __init__(self, iface):
    super().__init__()
    self.iface = iface
    self.canvas = iface.mapCanvas() 

    self.action = None
    self.tool = ToggleActiveLayerTool( self.iface )

  def initGui(self):
    title = "Toggle visibility of active layer"
    icon = QIcon( os.path.join( os.path.dirname(__file__), 'toggleactivelayer.png' ) )
    self.action = QAction( icon, title, self.iface.mainWindow() )
    self.action.setObjectName( "ToggleActiveLayerPlugin" )
    self.action.setWhatsThis( title )
    self.action.setStatusTip( title )
    self.action.triggered.connect( self.run )
    self.menu = "&Toggle active layer tool"

    # Maptool
    self.action.setCheckable( True )
    self.tool.setAction( self.action )

    self.iface.addToolBarIcon( self.action )
    self.iface.addPluginToMenu( self.menu, self.action )

  def unload(self):
    self.canvas.unsetMapTool( self.tool )
    self.iface.removeToolBarIcon( self.action )
    self.iface.removePluginMenu( self.menu, self.action )
    del self.action

  @pyqtSlot(bool)
  def run(self, checked):
    if self.canvas.mapTool() != self.tool:
      self.canvas.setMapTool( self.tool)
