# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SWDEWypis
                                 A QGIS plugin
 przezentuje dane o działce geodezyjnej z bazy danych SWDE (Postgres) w formie zbliżonej do wypisu z rejestru grundów 
                             -------------------
        begin                : 2015-11-13
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
    """Load SWDEWypis class from file SWDEWypis.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .swde_wypis import SWDEWypis
    return SWDEWypis(iface)
