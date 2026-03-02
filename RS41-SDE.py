#!/usr/bin/env python3
import serial
import time
import re
from datetime import datetime


Save_File = 0  # 0 = The .txt file will not be created, 1 = The .txt file will be created
File_Path = "File_Path"  # If you enter 1 in the Save_File variable, specify the file path indicating the location where you want to save it. 


# Serial Configuration 
PORT = '' # Insert the serial communication port
BAUD = 9600
TIMEOUT = 1
DELAY_AFTER_CMD = 1.5
P0_HPA = 1013.25  # Standard pressure at sea level

RE_TEMP = re.compile(r'\bT:\s*([-+]?[0-9]+\.[0-9]+)')
RE_UMID = re.compile(r'\bRH:\s*([0-9]+\.[0-9]+)')
RE_PRES = re.compile(r'\bPressure:\s*([0-9]+\.[0-9]+)')

def send_command(ser, cmd, newline=True, delay=DELAY_AFTER_CMD):
    if newline:
        ser.write((cmd + '\r\n').encode())
    else:
        ser.write(cmd.encode())
    time.sleep(delay)
    return ser.read_all().decode(errors='ignore')

def estrai_dati(text):
    dati = {}
    m1 = RE_TEMP.search(text)
    m2 = RE_UMID.search(text)
    m3 = RE_PRES.search(text)

    if m1:
        try:
            dati['Temperature'] = float(m1.group(1))
        except ValueError:
            pass

    if m2:
        try:
            dati['Humidity'] = float(m2.group(1))
        except ValueError:
            pass

    if m3:
        try:
            dati['Atm_Pressure'] = float(m3.group(1))
        except ValueError:
            pass

    return dati

def pressione_to_altitudine(p_hpa, p0_hpa=P0_HPA):
    if p_hpa is None or p_hpa <= 0 or p0_hpa <= 0:
        return None

    altitudine = 44330.0 * (1.0 - (p_hpa / p0_hpa) ** (1.0 / 5.255))
    return round(altitudine + 60.0, 2)

# Start
out = ""
ser = None

try:
    ser = serial.Serial(PORT, baudrate=BAUD, timeout=TIMEOUT)
    ser.reset_input_buffer()

    # Send Command
    ser.write(b'S')
    time.sleep(DELAY_AFTER_CMD)
    out = ser.read_all().decode(errors='ignore')

    if "RH:" not in out:
        ser.write(b'Twsv\r\n')
        time.sleep(3)
        out = send_command(ser, "S")

except serial.SerialException as e:
    print(f"Errore seriale: {e}")
    out = ""

finally:
    if ser is not None:
        try:
            ser.close()
        except Exception:
            pass

# data extraction
dati = estrai_dati(out)
ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if 'Atm_Pressure' in dati:
    alt = pressione_to_altitudine(dati['Atm_Pressure'])
else:
    alt = None


temperatura = dati.get('Temperature')
umidita = dati.get('Humidity')
pressione = dati.get('Atm_Pressure')
altitudine = alt


# .txt
if Save_File == 1:
    try:
        with open(File_Path, "w") as f:
            f.write(f"Temperature (°C): {temperatura}\n")
            f.write(f"Humidity (%): {umidita}\n")
            f.write(f"Atm Pressure (hPa): {pressione}\n")
            f.write(f"Altitude (m): {altitudine}\n")
    except Exception as e:
        print(f"File Error {e}")


print("Telemetry Data:")

if temperatura is not None:
    print(f"Temperature (°C): {temperatura}")
if umidita is not None:
    print(f"Humidity (%): {umidita}")
if pressione is not None:
    print(f"Atm Pressure (hPa): {pressione}")
if altitudine is not None:
    print(f"Altitude (m): {altitudine}")

if all(v is None for v in [temperatura, umidita, pressione]):
    print("No data found.")

print(f"[{ts}]")

