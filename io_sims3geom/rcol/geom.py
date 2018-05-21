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

from .geom_data.matdef import MaterialDefinition


class Geom:
    """ Handle GEOM data """


    embed_materialtype = {
        0x548394b9: "SimSkin",
        0xcf8a70b4: "SimEyes",
        0x00000000: "None"
    }


    def __init__(self, filedata):
        self.reader = DataReader(filedata)

        self.embedded_id = None     # FNV32 Hash of "SimSkin" or "SimEyes"
        self.matdef      = None     # only if embedded_id != 0
        self.vertformats = None


    @staticmethod
    def from_file(filepath):
        print("Reading .simgeom file...\n")

        file = open(filepath, "rb")
        filedata = file.read()
        file.close()
        return(Geom(filedata))


    def read_data(self):
        # RCOL Header section
        self.reader.read_int32()     # Version
        self.reader.read_int32()     # Count of Internal Public Chunks
        self.reader.read_int32()     # Index3 (unused)
        self.reader.read_int32()     # ExternalCount

        internalct = self.reader.read_int32()
        # GEOM files have TGI values of 0
        # TGI: Type, Group, Instance
        for _ in range(internalct):
            if self.reader.read_uint64() != 0:
                print("Unexpected TGI values at", hex(self.reader.offset))
                return False
            if self.reader.read_uint32() != 0:
                print("Unexpected TGI values at", hex(self.reader.offset))
                return False
            if self.reader.read_uint32() != 0:
                print("Unexpected TGI values at", hex(self.reader.offset))
                return False

        for _ in range(internalct):
            self.reader.read_uint32()    # Position of the Chunk (absolute)
            self.reader.read_uint32()    # Size of the Chunk


        # GEOM Data section
        # 0x4d4f4547 'GEOM' in ascii, identifies a GEOM block
        if self.reader.read_uint32() != 0x4d4f4547:
            print("Error, invalid geom file")
            return False

        print("GEOM version:", self.reader.read_uint32())
        print("TGI Offset:", self.reader.read_uint32())
        print("TGI Size:", self.reader.read_uint32())
        embedded_id = self.reader.read_uint32()
        print("EmbeddedID:", Geom.embed_materialtype[embedded_id])

        ## MTNF Chunk is skipped for now, as I do not yet know it's purpose
        if embedded_id != 0:
            print("\nMATD Chunk")
            chunksize = self.reader.read_int32()
            print("Chunksize:", chunksize)
            self.reader.offset += chunksize
            # print("MTNF:", self.reader.read_uint32() == 0x464e544d)
            # print("UNKNOWN:", self.reader.read_int32())
            # print("Datasize:", self.reader.read_int32())
            #
            # count = self.reader.read_int32()
            # print("\nCount:", count)
            # for _ in range(count):
            #     print("Param name hash:", hex( self.reader.read_uint32() ))
            #     print("Data type code:", self.reader.read_int32())
            #     print("Data size:", self.reader.read_int32())
            #     print("Data offset:", self.reader.read_int32())
            print()

        print("Merge Group", self.reader.read_int32())
        print("Sort Order", self.reader.read_int32())
        vertcount = self.reader.read_int32()
        fcount    = self.reader.read_int32()
        print("VertexCount", vertcount)
        print("VertexElement Count", fcount)

        vertformats = []
        for i in range(fcount):
            _datatype = self.reader.read_int32()
            _subtype  = self.reader.read_int32()
            _byteamount = self.reader.read_byte()
            vertformats.append({
                'datatype':_datatype,
                'subtype':_subtype,
                'byteamount': _byteamount
            })
            print(vertformats[i])



        # Return True if nothing failed
        return True
