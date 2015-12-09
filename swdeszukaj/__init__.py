# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SWDESzukaj
                                 A QGIS plugin
 wyszukiwarka działek geodezyjnych w bazie Postgis (dane zaimportowane z pliku SWDE)
                             -------------------
        begin                : 2015-12-08
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
    """Load SWDESzukaj class from file SWDESzukaj.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .swdeszukaj import SWDESzukaj
    return SWDESzukaj(iface)
