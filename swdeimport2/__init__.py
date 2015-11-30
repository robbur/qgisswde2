# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SWDEImport2
                                 A QGIS plugin
 importuje dane z plików SWDE do bazy Postgis
                             -------------------
        begin                : 2015-10-20
        copyright            : (C) 2015 by Robert Dorna
        email                : robert.dorna@wp.eu
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SWDEImport2 class from file SWDEImport2.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .swde_import_2 import SWDEImport2
    return SWDEImport2(iface)
