import RPi.GPIO as GPIO
import dht11
import time
import os


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# pines
DHT11_PIN = 4   # Pin para el sensor DHT11
PIR_PIN = 17    # Pin para el sensor PIR
SMOKE_PIN = 27  # Pin para el sensor de humo
VIBRATION_PIN = 22  # Pin para el sensor de vibración KY-031

# iniciar sensor temperatura humedad
dht11_sensor = dht11.DHT11(pin=DHT11_PIN)

# configurar demas sensores
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(SMOKE_PIN, GPIO.IN)
GPIO.setup(VIBRATION_PIN, GPIO.IN)

# variables para guardar el ultimo valor
last_temperature = None
last_humidity = None

# imprimir prueba
print("Directorio de trabajo actual:", os.getcwd())

# crear archivo y la a para asignar
with open("datos_sensores.txt", "a") as file:
    try:
        while True:
            # lect frl dht11
            dht11_result = dht11_sensor.read()
            if dht11_result.is_valid():
                # act los datos
                last_temperature = dht11_result.temperature
                last_humidity = dht11_result.humidity

            # mensajes
            data_line = ""
            if last_temperature is not None and last_humidity is not None:
                data_line += "Temperatura: %-3.1f C, Humedad: %-3.1f %%\n" % (last_temperature, last_humidity)
                print("Temperatura: %-3.1f C" % last_temperature)
                print("Humedad: %-3.1f %%" % last_humidity)
            else:
                data_line += "No hay datos válidos disponibles aún.\n"
                print("No hay datos válidos disponibles aún.")

            # lect pir
            pir_state = GPIO.input(PIR_PIN)
            if pir_state:
                data_line += "PIR: ¡Movimiento detectado!\n"
                print("PIR: ¡Movimiento detectado!")
            else:
                data_line += "PIR: No hay movimiento\n"
                print("PIR: No hay movimiento")

           
            smoke_state = GPIO.input(SMOKE_PIN)
            if smoke_state:
                data_line += "¡Humo detectado!\n"
                print("¡Humo detectado!")
            else:
                data_line += "No se detecta humo\n"
                print("No se detecta humo")
            
           
            vibration_state = GPIO.input(VIBRATION_PIN)
            if vibration_state:
                data_line += "¡Vibración detectada!\n"
                print("¡Vibración detectada!")
            else:
                data_line += "No se detecta vibración\n"
                print("No se detecta vibración")

       
            file.write(time.strftime("%Y-%m-%d %H:%M:%S") + " - " + data_line + "\n")
            file.flush()  
            time.sleep(1)

    except KeyboardInterrupt:
        print("Limpieza")
        GPIO.cleanup()