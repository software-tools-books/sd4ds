from struct import pack, unpack

def pack_string(msg):
    as_bytes = bytes(msg, "utf-8")
    header = pack("i", len(as_bytes))
    body_format = "%ds" % len(as_bytes)
    body = pack(body_format, as_bytes)
    return header + body

packed = pack_string("hello")
print(repr(packed))


def unpack_string(buffer):
    header, body = buffer[:4], buffer[4:]
    unpacked_header = unpack("i", header)
    length = unpacked_header[0]
    body_format = "%ds" % length
    result = unpack(body_format, body)
    return str(result[0], "utf-8")

unpacked = unpack_string(packed)
print(unpacked)
