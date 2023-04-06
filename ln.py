from ctypes import Structure, Union, c_float , c_uint32


class struct (Structure):
     _fields_ = [("f", c_uint32,23),
                ("e", c_uint32, 8),
                ("s",c_uint32,1)
                ]

class IEE754(Union):
     _fields_ = [("x",c_float),
                 ("bits",struct)]
def get_IEE754(y):
    z = IEE754()
    z.x = y
    fz = z.bits.f
    e = z.bits.e
    s = z.bits.s
    f23 = 0.00000011920928955078125#2^-23
    fr = fz*f23#ver como float
    return fz,e,s,fr

fz,e,s,fr = get_IEE754(3.125)
print(fz,e,s,fr)
