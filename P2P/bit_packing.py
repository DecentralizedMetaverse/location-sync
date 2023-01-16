# ビットパッキング ----------------------
class BitPacking:
    def iptoi(self, x):
        x = x.split('.', )
        x = [int(i) for i in x]
        return ((x[0] << self.bit_size*3) | (x[1] << self.bit_size*2) | (x[2] << self.bit_size*1) | (x[3] << self.bit_size*0)) 


    def pack(self, ip, port, x, y):
        x = int(x * 100)
        y = int(y * 100)    
        data = (self.iptoi(ip) << self.bit_size*10) | (port << self.bit_size*8) | (x << self.bit_size*4) | (y << self.bit_size*0)
        return data.to_bytes(14, 'big')


    def unpack(self, data):
        data = int.from_bytes(data, 'big')
        ip0 = (data >> self.bit_size*13) & 0xFF
        ip1 = (data >> self.bit_size*12) & 0xFF
        ip2 = (data >> self.bit_size*11) & 0xFF
        ip3 = (data >> self.bit_size*10) & 0xFF
        ip = f"{ip0}.{ip1}.{ip2}.{ip3}"
        port = (data >> self.bit_size*8) & 0xFFFF
        x = float((data >> self.bit_size*4) & 0xFFFF_FFFF) * 0.01
        y = float((data >> self.bit_size*0) & 0xFFFF_FFFF) * 0.01

        return ip, port, x, y