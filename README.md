## 🧠 Flujo de trabajo – Sistema SmartBin con ESP32 + Flask + MQTT

1️⃣ **ESP32 (C++ + Sensor + MQTT)**  
Cada SmartBin mide el peso actual de su contenido (ej. tornillos, piezas) y **envía los datos por MQTT** al tópico `smartbin/lectura`.

2️⃣ **Flask (Python + MySQL)**  
El backend Flask recibe el mensaje MQTT, identifica el `uid_hardware` del SmartBin y **consulta en la base de datos** a qué usuario pertenece.

3️⃣ **Flask (Control de stock)**  
Verifica si el peso está **por debajo del stock mínimo** configurado. Si es así, **registra el evento** y puede disparar una alerta (email, notificación, etc.).

4️⃣ **Frontend Web (Dashboard)**  
El usuario puede **ver el estado de todos sus SmartBins en tiempo real**, cambiar nombres, ubicaciones, configurar mínimos, o agregar nuevos bins desde un panel web.

5️⃣ **MQTT (Control remoto opcional)**  
La app también puede enviar comandos al ESP32 (por ejemplo: reset, calibración, testeo) usando tópicos como `smartbin/control/BIN01`.

---

## 💡 Resumen del flujo completo

📥 **ESP32 mide** → 📡 **MQTT envía peso** → 🖥 **Flask consulta y guarda**  
📊 **Dashboard muestra estado** → ⚠️ **Se genera alerta si el peso es bajo**

---

## 🆕 Flujo de alta de un nuevo SmartBin

1. El ESP32 ya viene flasheado con un `uid_hardware`, ej. `"BIN01"`.
2. El cliente recibe el SmartBin con un QR o código impreso.
3. Desde la app web, ingresa o escanea ese código.
4. Flask **verifica que el bin esté libre** y lo asocia a su cuenta.
5. El bin comienza a enviar datos, y queda visible en su dashboard.