
import spidev
import time

class AHN72:
    def __init__(self, spi_device=0, spi_port=0):
        time.sleep(20)
        self.spi = spidev.SpiDev()
        self.spi.open(spi_device, spi_port)
        self.spi.max_speed_hz = 244000
        self.spi.mode = 0b01
        time.sleep(20)

    def get_humidity(self):    
        time.sleep(30)
        msg = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]
        self.spi.xfer(msg)

        time.sleep(5)

        answer = self.spi.readbytes(4)

        print([hex(item) for item in answer])
        int_val = int.from_bytes(answer, "little")
        time.sleep(10)
        return int_val