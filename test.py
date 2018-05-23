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
from io_sims3geom.rcol.geom import Geom


# Testing file
def main():
    # geomtest = Geom.from_file("testfiles/amTopShirtMuscle_lod1_0x0000000055575982.simgeom")
    geomtest = Geom.from_file("testfiles/tf_rockstar.simgeom")
    if not geomtest.read_data(strict=False):
        print("\nCancelled at", geomtest.reader.offset, "/", len(geomtest.reader.data))
        del(geomtest)

        return

main()
