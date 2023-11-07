import machine
my_SDA_pin = 8  # I2C SDA pin number here!
my_SCL_pin = 9  # I2C SCL pin number here!
my_i2c_freq = 400000 


# Scanner i2c en MicroPython | MicroPython i2c scanner
# Renvoi l'adresse en decimal et hexa de chaque device connecte sur le bus i2c
# Return decimal and hexa adress of each i2c device
# https://projetsdiy.fr - https://diyprojects.io (dec. 2017)
i2c = machine.I2C(0, scl=machine.Pin(my_SCL_pin), sda=machine.Pin(my_SDA_pin))

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))