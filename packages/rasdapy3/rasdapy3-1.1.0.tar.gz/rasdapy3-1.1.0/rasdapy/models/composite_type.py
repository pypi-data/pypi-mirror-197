"""
 *
 * This file is part of rasdaman community.
 *
 * Rasdaman community is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Rasdaman community is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU  General Public License for more details.
 *
 * You should have received a copy of the GNU  General Public License
 * along with rasdaman community.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Copyright 2003 - 2016 Peter Baumann / rasdaman GmbH.
 *
 * For more information please see <http://www.rasdaman.org>
 * or contact Peter Baumann via <baumann@rasdaman.com>.
 *
"""
from rasdapy.cores.format_utils import format_scalar


class CompositeType(object):
    """
    Represent a composite object of bands's values (e.g: select {1, 2, 3})
    """
    def __init__(self, bands_values, bands_types):
        # bands_values is an array of values
        self.bands_values = bands_values
        self.bands_types = bands_types

    def __str__(self):
        """
        String representing the composite object (e.g: array bands_values: [1, 2, 3] -> { 1, 2, 3 } in String)
        :return: String (e.g: { 1, 2, 3 })
        """
        output = ""
        for i in range(len(self.bands_values)):
            val = self.bands_values[i]
            dt = self.bands_types[i]
            if len(output) > 0:
                output += ", "
            output += format_scalar(val, dt)
        return "{ " + output + " }"
