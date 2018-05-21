'''
Copyright (C) 2018 SmugTomato

Created by SmugTomato

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from .datareader import DataReader
from .datawriter import DataWriter

from .geom_data.header import GeomHeader


class Geom:
    """ Handle GEOM data """


    def __init__(self, filedata):
        self.reader = DataReader(filedata)


    @staticmethod
    def from_file(filepath):
        print("Reading .simgeom file...\n")

        file = open(filepath, "rb")
        filedata = file.read()
        file.close()
        return(Geom(filedata))


    def read_data(self):
        # HEADER
        header = GeomHeader()
        if not header.from_file(self.reader):
            print("Could not read GEOM file, aborting")
            return False

        return True
