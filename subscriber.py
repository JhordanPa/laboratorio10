import json
import paho.mqtt.client as mqtt
from pydantic import BaseModel, Field, ValidationError
# Definimos el esquema de datos esperado usando Pydantic
class LecturaSensor(BaseModel):
    sensor_id: int
    timestamp: float
    valor: float = Field(..., ge=-50.0, le=100.0) # Validación de límites físicos de temperatura
    unidad: str
    
BROKER = "broker.hivemq.com"
PUERTO = 1883
TOPICO = "unmsm/callao/camara/+/telemetria"

#Funcion para registrar errores
def registrar_error(mensaje_error):
    with open("log_errores.txt", "a", encoding="utf-8") as file:
        file.write(f"{mensaje_error}\n")

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Conectado exitosamente al Broker MQTT")
        # Suscribirse al tópico de interés
        client.subscribe(TOPICO)
        print(f"Suscrito a: {TOPICO}")
    else:
        print(f"Error de conexión. Código de retorno: {rc}")
        # Callback cuando llega un mensaje publicado al tópico suscrito
        
def on_message(client, userdata, msg):
    raw_payload = msg.payload.decode()
    print(f"\n[SUBSCRIBER] Mensaje recibido en {msg.topic}")
    
    try:
        datos_json = json.loads(raw_payload)
        lectura = LecturaSensor(**datos_json)
        
        # Validación de temperatura de la cámara
        if lectura.valor > 5.0:
            print(f"[PELIGRO] ¡Pérdida de cadena de frío en Cámara {lectura.sensor_id}!")
        else:
            print(f"-> Cámara {lectura.sensor_id} estable a {lectura.valor} {lectura.unidad}")
            
    except json.JSONDecodeError:
        error_msg = f"[ALERTA] JSON inválido en {msg.topic}: {raw_payload}"
        print(error_msg)
        registrar_error(error_msg)
        
    except ValidationError as e:
        error_msg = f"[ALERTA DE SEGURIDAD] Datos corruptos en {msg.topic}. Detalles:\n{e}"
        print(error_msg)
        registrar_error(error_msg) # Se guarda en log_errores.txt
        
def main():
    cliente = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    # Asignar los callbacks de eventos de red
    cliente.on_connect = on_connect
    cliente.on_message = on_message
    cliente.connect(BROKER, PUERTO, 60)
    # Iniciar bucle síncrono infinito para escuchar mensajes de red
    cliente.loop_forever()
    
if __name__ == "__main__":
    main()
