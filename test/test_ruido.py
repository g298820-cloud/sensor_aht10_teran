# -------------------------------------------------------------
# test_ruido.py — Evaluación de estabilidad (ruido) del sensor AHT10
# Autor: Gustavo Santos Terán Rupay
# Curso: EA801 — 2025S2
# -------------------------------------------------------------

from machine import Pin, I2C
import time
import math

# Dirección I2C del sensor AHT10
AHT10_ADDR = 0x38

# Configuración del bus I2C del sensor
i2c_sensor = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)

def leer_aht10():
    """Lee la temperatura y humedad del sensor AHT10."""
    try:
        # Reset e inicialización
        i2c_sensor.writeto(AHT10_ADDR, b'\xBA')
        time.sleep_ms(20)
        i2c_sensor.writeto(AHT10_ADDR, b'\xE1\x08\x00')
        time.sleep_ms(20)

        # Comando de medición
        i2c_sensor.writeto(AHT10_ADDR, b'\xAC\x33\x00')
        time.sleep_ms(100)

        # Leer 6 bytes de datos
        data = i2c_sensor.readfrom(AHT10_ADDR, 6)

        # Procesar datos crudos
        humidity_raw = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4))
        humidity = humidity_raw * 100 / 1048576

        temp_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        temperature = temp_raw * 200 / 1048576 - 50

        return temperature, humidity

    except OSError as e:
        print("Error de comunicación I2C:", e)
        return None, None


def calcular_estadisticas(datos):
    """Devuelve promedio y desviación estándar de una lista de valores."""
    if not datos:
        return None, None
    media = sum(datos) / len(datos)
    varianza = sum((x - media) ** 2 for x in datos) / len(datos)
    return media, math.sqrt(varianza)



# Medición de ruido en 30 muestras consecutivas

temperaturas = []
humedades = []

print("\n Iniciando prueba de estabilidad del sensor AHT10...\n")

for i in range(30):
    temp, hum = leer_aht10()
    if temp is not None:
        temperaturas.append(temp)
        humedades.append(hum)
        print(f"{i+1:02d}. Temp: {temp:.2f} °C | Hum: {hum:.2f} %")
    else:
        print(f"{i+1:02d}. Error de lectura.")
    time.sleep(2)  # espera entre mediciones

# Calcular estadísticas
temp_media, temp_std = calcular_estadisticas(temperaturas)
hum_media, hum_std = calcular_estadisticas(humedades)

print("\n Resultados finales:")
print(f"Temperatura media: {temp_media:.2f} °C  |  Desv. estándar: {temp_std:.3f}")
print(f"Humedad media:     {hum_media:.2f} %    |  Desv. estándar: {hum_std:.3f}")
print("\n Test de ruido completado.")














































