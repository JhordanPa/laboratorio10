**1. Pregunta Crítica: ¿Por qué no es viable utilizar una arquitectura síncrona HTTP REST**
**para interconectar 10, 000 sensores industriales que reportan datos cada 100 milisegundos?** 
**Justifique su respuesta basándose en hilos de ejecución de servidor y sobrecarga de paquetes.**

Hilos de ejecución (Sincronía): HTTP se basa en un modelo síncrono de Cliente-Servidor. Si miles de sensores reportan datos cada 100 milisegundos, 
el servidor web tendría que mantener miles de hilos (threads) abiertos y bloqueados simultáneamente esperando procesar cada petición,
lo que provocaría un colapso rápido del servidor (Thread Starvation). En cambio, MQTT ejecuta estas operaciones de manera asíncrona, liberando los hilos.

Sobrecarga de red (Overhead): HTTP requiere cabeceras de texto pesadas que superan los 500 bytes por cada envío, 
mientras que MQTT tiene una cabecera fija ultra ligera de apenas 2 bytes. Multiplicar 500 bytes por miles de sensores enviando datos diez veces por segundo saturaría 
por completo el ancho de banda físico de la planta industrial.

**2. Pregunta Práctica: Explique en qué escenarios de desarrollo de software es imperativo**
**utilizar el nivel QoS 2 en lugar de QoS 0.**

El nivel QoS 0 opera bajo el principio del "mejor esfuerzo", donde un mensaje puede perderse en el camino sin intentar retransmitirse. 
En contraparte, QoS 2 garantiza que el mensaje llegue exactamente una vez. Es absolutamente imperativo usar QoS 2 en escenarios donde perder 
el mensaje o procesarlo dos veces causa un daño crítico:

Ejmplo de control de maquinaria crítica: Si se envía el comando de "Abrir Válvula de Liberación de Presión", 
debe ejecutarse con total certeza una única vez.

**3. Reflexión Ética/RSU: El uso ineficiente de protocolos de red aumenta el procesamiento**
**en centros de datos, incrementando la huella de carbono. ¿Cómo contribuye el diseño de**
**protocolos eficientes como MQTT a la sostenibilidad tecnológica de las regiones rurales**
**del Perú?**

El protocolo MQTT está diseñado para funcionar en redes propensas a interrupciones o conexiones satelitales, características muy comunes en la geografía rural peruana. 
Al minimizar drásticamente el tamaño de los paquetes de datos transmitidos, este protocolo logra un ahorro crítico tanto en el ancho de banda como en la batería de los 
microcontroladores.
