
with open('input-16.txt', 'r') as f:
    line = f.read().strip()

class Bits:
    @staticmethod
    def get_bits(i: int):
        return [i & 8, i & 4, i & 2, i & 1]
    
    def __init__(self, data: str):
        self.bits = []
        for c in data:
            self.bits.extend(Bits.get_bits(int(c, 16)))
        self.current_count = []
    
    def peek(self, count):
        return self.bits[:count]
    
    def get(self, count):
        data = self.peek(count)
        for i in range(len(self.current_count)):
            self.current_count[i] += count
        self.bits = self.bits[count:]
        return data
    
    def get_bool(self):
        return bool(self.get_int(1))
    
    def get_int(self, count):
        bs = self.get(count)
        v = 0
        for b in bs:
            v = v << 1
            if b:
                v |= 1
        return v
    
    def begin_packet(self):
        self.current_count.append(0)
    
    def end_packet(self, remove_padding):
        if remove_padding:
            while self.current_count[-1] % 4 != 0:
                self.get(1)
        self.current_count.pop()

def read_header(bits: Bits):
    version = bits.get_int(3)
    typ = bits.get_int(3)
    return version, typ

def read_subpacket_len(bits: Bits):
    uses_num_subpackets = bits.get_bool()
    if uses_num_subpackets:
        return None, bits.get_int(11)
    else:
        return bits.get_int(15), None

def read_literal(bits: Bits):
    val = 0
    last = False
    while not last:
        last = not bits.get_bool()
        seg = bits.get_int(4)
        val = val << 4
        val |= seg
    return val

class LiteralPacket:
    def __init__(self, version: int, bits: Bits):
        self.version = version
        self.value = read_literal(bits)
    
    def __str__(self):
        return f'Literal{{version={self.version}, value={self.value}}}'

class OperatorPacket:
    def __init__(self, version: int, typ: int, bits: Bits):
        self.version = version
        self.type = typ
        self.bit_len, self.num_subpackets = read_subpacket_len(bits)
        self.subpackets = []
    
    @property
    def has_bit_len(self): return self.bit_len is not None

    @property
    def header_len(self):
        return 22 if self.has_bit_len else 18
    
    @property
    def value(self):
        if self.type == 0:
            return sum(s.value for s in self.subpackets)
        elif self.type == 1:
            v = 1
            for s in self.subpackets:
                v *= s.value
            return v
        elif self.type == 2:
            return min(s.value for s in self.subpackets)
        elif self.type == 3:
            return max(s.value for s in self.subpackets)
        elif self.type == 5:
            return int(self.subpackets[0].value > self.subpackets[1].value)
        elif self.type == 6:
            return int(self.subpackets[0].value < self.subpackets[1].value)
        else:
            return int(self.subpackets[0].value == self.subpackets[1].value)
    
    def __str__(self):
        return f'Operator{{version={self.version}, type={self.type}, contains=[{", ".join(str(s) for s in self.subpackets)}]}}'

def read_packet(bits: Bits, top: bool):
    bits.begin_packet()
    version, typ = read_header(bits)
    if typ == 4:
        packet = LiteralPacket(version, bits)
        bits.end_packet(top)
        return packet
    
    packet = OperatorPacket(version, typ, bits)
    while True:
        subpacket = read_packet(bits, False)
        packet.subpackets.append(subpacket)
        if packet.has_bit_len:
            if (bits.current_count[-1] - packet.header_len) == packet.bit_len:
                break
        else:
            if len(packet.subpackets) == packet.num_subpackets:
                break
    bits.end_packet(top)
    return packet

def get_version_sum(packet):
    sum = packet.version
    if type(packet) is OperatorPacket:
        for sub in packet.subpackets:
            sum += get_version_sum(sub)
    return sum

#breakpoint()
bits = Bits(line)
packet = read_packet(bits, True)
print(packet)
#print(get_version_sum(packet))
print(packet.value)