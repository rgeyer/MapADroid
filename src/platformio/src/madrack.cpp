// #include <FS.h>
// #include <Arduino.h>
// #include <ArduinoJson.h>
// #include <ESP8266WiFi.h>
// #include <ESP8266mDNS.h>
// #include <ESPAsyncWebServer.h>

// class MadRack {
//     private:
//     AsyncWebServer *_server;
//     bool _configured = false;
//     uint8_t _reset_pin;
//     String _config_file_path = "config.json";
//     const char* _name;
//     const char* _wifi_ssid;
//     const char* _wifi_pass;
//     const char* _iot_host;
//     const char* _iot_cacert;
//     const char* _iot_client_cert;
//     const char* _iot_key;

//     bool _readConfig() {
//         File configFile = SPIFFS.open(_config_file_path, "r");
//         if(!configFile) {
//             Serial.println("Unable to open config file.");
//             return false;
//         }

//         size_t size = configFile.size();
//         std::unique_ptr<char []> buf(new char[size]);
//         configFile.readBytes(buf.get(), size);

//         DynamicJsonDocument doc(size);
//         auto error = deserializeJson(doc, buf.get());
//         if (error) {
//             Serial.println("Unable to deserialize config file.");
//             return false;
//         }

//         _name = doc["name"];
//         _wifi_ssid = doc["wifi_ssid"];
//         _wifi_pass = doc["wifi_pass"];
//         _iot_host = doc["iot_host"];
//         _iot_cacert = doc["iot_cacert"];
//         _iot_client_cert = doc["iot_client_cert"];
//         _iot_key = doc["iot_key"];

//         return true;
//     }

//     void _configMode() {
//         WiFi.mode(WIFI_AP);
//         const char apname[] = "MADRack-" + ESP.getChipId();
//         Serial.println("Creating softAP with name " + apname);
//         WiFi.softAP(apname);
//         _server->on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
//             request->send(200, "text/plain", "Setup Mode");
//         });

//         Serial.println("AP IP Address: " + WiFi.softAPIP().toString());
//     }

//     void _connectToWiFi() {

//     }

//     public:
//     MadRack() {
//         _server = new AsyncWebServer(80);
//     }

//     bool begin(uint8_t reset_pin) {
//         Serial.println("Heller?");
//         if (!SPIFFS.begin()) {
//             Serial.println("Unable to start SPIFFS");
//         }
//         _reset_pin = reset_pin;
//         // Setup the reset pin.
//         pinMode(_reset_pin, INPUT_PULLUP);
//         Serial.println("Pins all setup");

//         if(_readConfig()) {
//             WiFi.hostname(_name);
//             WiFi.mode(WIFI_STA);
//             WiFi.begin(_wifi_ssid, _wifi_pass);
//             Serial.println(String("Attempting to connect to SSID: ") + String(_wifi_ssid));
//             while (WiFi.status() != WL_CONNECTED)
//             {
//                 Serial.print(".");
//                 delay(1000);
//             }
//             Serial.println("");
//             Serial.print("IP address: ");
//             Serial.println(WiFi.localIP());

//             MDNS.addService("http", "tcp", 80);
//         } else {
//             _configMode();
//         }

//         Serial.println("Starting webserver");
//         _server->serveStatic("/fs", SPIFFS, "/");
//         _server->begin();
//         Serial.println("Server Started");
//         return true;
//     }

//     void loop() {
//         if(!_configured || digitalRead(_reset_pin) == LOW) {
//             // Reset
//         }
//     }
// };