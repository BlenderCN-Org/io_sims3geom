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


class GeomHeader:


    embed_materialtype = {
        0x548394b9: "SimSkin",
        0xcf8a70b4: "SimEyes",
        0x00000000: "None"
    }


    def __init__(self):
        self.embedded_id = None
        self.mtnf_chunk  = None


    @staticmethod
    def from_file(reader):
        # RCOL Header section
        reader.read_int32()     # Version
        reader.read_int32()     # Count of Internal Public Chunks
        reader.read_int32()     # Index3 (unused)
        reader.read_int32()     # ExternalCount

        internalct = reader.read_int32()
        # GEOM files have TGI values of 0
        # TGI: Type, Group, Instance
        for _ in range(internalct):
            if reader.read_uint64() != 0:
                print("Unexpected TGI values at", hex(reader.offset))
                return False
            if reader.read_uint32() != 0:
                print("Unexpected TGI values at", hex(reader.offset))
                return False
            if reader.read_uint32() != 0:
                print("Unexpected TGI values at", hex(reader.offset))
                return False

        for _ in range(internalct):
            reader.read_uint32()    # Position of the Chunk (absolute)
            reader.read_uint32()    # Size of the Chunk


        # GEOM Header section
        # 0x4d4f4547 'GEOM' in ascii, identifies a GEOM block
        if reader.read_uint32() != 0x4d4f4547:
            print("Error, invalid geom file")
            return False

        print("GEOM version:", reader.read_uint32())
        print("TGI Offset:", reader.read_uint32())
        print("TGI Size:", reader.read_uint32())
        embedded_id = reader.read_uint32()
        print("EmbeddedID:", GeomHeader.embed_materialtype[embedded_id])

        if embedded_id != 0:
            print("Chunksize:", reader.read_int32())



        return True
