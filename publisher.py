import time
import random
import json
import paho.mqtt.client as mqtt
# Configuración del Broker Público de Pruebas
BROKER = "broker.hivemq.com"
PUERTO = 1883
TOPICO = "unmsm/fisi/cc/sensor/temperatura"
def conectar_mqtt():
# Inicializar cliente MQTT utilizando la API moderna v2
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    print(f"Conectando al broker {BROKER}...")
    client.connect(BROKER, PUERTO, 60)
    return client
def main():
    cliente = conectar_mqtt()
    cliente.loop_start() # Iniciar el bucle de red de fondo
    
    camaras = [1, 2]
    
    try:
        while True:
            for camara_id in camaras:
                # 1. Tópico dinámico
                topico = f"unmsm/callao/camara/{camara_id}/telemetria"
                
                # 2. Inyección de fallas (aprox. 20% de probabilidad de error)
                probabilidad_fallo = random.random()
                
                if probabilidad_fallo < 0.10:
                    temperatura = 150.0 # Falla: fuera del límite físico
                elif probabilidad_fallo < 0.20:
                    temperatura = "ERROR_DE_LECTURA" # Falla: tipo de dato incorrecto (string)
                else:
                    # Rango normal de operación (ej. -5 a 10 grados)
                    temperatura = round(random.uniform(-5.0, 10.0), 2)
                
                datos_sensor = {
                    "sensor_id": camara_id,
                    "timestamp": time.time(),
                    "valor": temperatura,
                    "unidad": "Celsius"
                }
                
                mensaje = json.dumps(datos_sensor)
                info = cliente.publish(topico, mensaje, qos=1)
                info.wait_for_publish()
                
                print(f"[PUBLISHER] Enviado a {topico}: {mensaje}")
                time.sleep(2) # Pausa breve entre el envío de cada cámara
                
    except KeyboardInterrupt:
        print("\nDeteniendo publicador...")
        
    finally:
        cliente.loop_stop()
        cliente.disconnect()
        
if __name__ == "__main__":
    main()
