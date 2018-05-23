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

from .geom_data.vertex import Vertex


class Geom:
    """ Handle GEOM data """


    embed_materialtype = {
        0x548394b9: "SimSkin",
        0xcf8a70b4: "SimEyes",
        0x00000000: "None"
    }


    def __init__(self, filedata):
        self.reader = DataReader(filedata)

        self.embedded_id = None
        self.mtnf_parms  = None
        self.vertices    = None
        self.triangles   = None
        self.skin_ctrl   = None
        self.bonehashes  = None
        self.tgisets     = None


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
        tgi_offset = self.reader.read_uint32() + self.reader.offset
        print("TGI Offset:", tgi_offset)
        print("TGI Size:", self.reader.read_uint32())
        embedded_id = self.reader.read_uint32()
        print("EmbeddedID:", Geom.embed_materialtype[embedded_id])

        # MTNF Chunk.
        # Probably important so should be saved as property in Blender
        if embedded_id != 0:
            mtnf_parms = []

            print("\nMTNF Chunk")
            chunksize = self.reader.read_int32()
            print("Chunksize:", chunksize)
            # self.reader.offset += chunksize
            print("MTNF:", self.reader.read_uint32() == 0x464e544d)
            print("UNKNOWN:", self.reader.read_int32())
            print("Datasize:", self.reader.read_int32())

            count = self.reader.read_int32()
            print("\nCount:", count)
            for _ in range(count):
                parm = {
                    'hash':None,
                    'typecode':None,
                    'size':None,
                    'offset':None,
                    'data':None
                }
                parm['hash'] = self.reader.read_uint32()
                parm['typecode'] = self.reader.read_int32()
                parm['size'] = self.reader.read_int32()
                parm['offset'] = self.reader.read_int32()
                mtnf_parms.append(parm)

            for p in mtnf_parms:
                # FLOATS
                if p['typecode'] == 1:
                    p['data'] = []
                    for _ in range(p['size']):
                        p['data'].append(self.reader.read_float())
                # INTEGERS
                elif p['typecode'] == 2:
                    p['data'] = []
                    for _ in range(p['size']):
                        p['data'].append(self.reader.read_int32())
                # TEXTURES
                elif p['typecode'] == 4:
                    p['data'] = []
                    for _ in range(p['size']):
                        p['data'].append(self.reader.read_int32())
                print(p)
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
            print(i, vertformats[i])

        # READ VERTEX DATA
        vertices = []
        for i in range(vertcount):
            vert = Vertex()

            for j in range(fcount):
                type = vertformats[j]['datatype']

                # POSITION
                if type == 1:
                    arr = []
                    for _ in range(3):
                        arr.append( self.reader.read_float() )
                    vert.position = arr
                # NORMAL
                elif type == 2:
                    arr = []
                    for _ in range(3):
                        arr.append( self.reader.read_float() )
                    vert.normal = arr
                # UV COORDINATES
                elif type == 3:
                    arr = []
                    for _ in range(2):
                        arr.append( self.reader.read_float() )
                    vert.uv = arr
                # BONE ASSIGNMENTS
                elif type == 4:
                    arr = []
                    for _ in range(4):
                        arr.append( self.reader.read_byte() )
                    vert.bone_asn = arr
                # BONE WEIGHTS
                elif type == 5:
                    arr = []
                    for _ in range(4):
                        arr.append( self.reader.read_float() )
                    vert.bone_wgt = arr
                # TANGENT
                elif type == 6:
                    arr = []
                    for _ in range(3):
                        arr.append( self.reader.read_float() )
                    vert.tangent = arr
                # TAGVAL
                elif type == 7:
                    arr = []
                    for _ in range(4):
                        arr.append( self.reader.read_byte() )
                    vert.tagval = arr
                # VERTEX ID
                elif type == 10:
                    vert.id = self.reader.read_int32()

            vertices.append(vert)
            # ENDLOOP
        # ENDLOOP


        # READ TRIANGLES
        if self.reader.read_int32() != 1:
            print("Unsupported Itemcount at", hex(self.reader.offset))
            return False

        if self.reader.read_byte() != 2:
            print("Unsupported Integer length for face indices at", hex(self.reader.offset))
            return False

        numfacepoints = self.reader.read_int32()
        triangles = []
        for _ in range(int(numfacepoints / 3)):
            tri = []
            for _ in range(3):
                tri.append(self.reader.read_int16())
            triangles.append(tri)


        skin_ctrl = self.reader.read_int32()


        bonehash_ct = self.reader.read_int32()
        bonehashes = []
        for _ in range(bonehash_ct):
            bonehashes.append(self.reader.read_uint32())
        print(bonehashes)


        # TGI SETS
        tgi_count = self.reader.read_int32()
        tgisets = []
        for _ in range(tgi_count):
            tgi = []
            tgi.append(self.reader.read_uint32())
            tgi.append(self.reader.read_uint32())
            tgi.append(self.reader.read_uint64())
            tgisets.append(tgi)
        for t in tgisets:
            print(t)


        self.embedded_id = embedded_id
        self.mtnf_parms  = mtnf_parms
        self.vertices    = vertices
        self.triangles   = triangles
        self.skin_ctrl   = skin_ctrl
        self.bonehashes  = bonehashes
        self.tgisets     = tgisets


        print()
        print("Finished at", self.reader.offset, "/", len(self.reader.data))
        del(self.reader)

        # Return True if nothing failed
        return True
