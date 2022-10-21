#pragma once
#include <Arduino.h>
#include <WiFi.h>

class Wifi {
  public:
    void setup(const char* ssid, const char* pass) {
      // WiFiのアクセスポイントに接続
      Serial.println("### WIFI INIT ###");
      WiFi.begin(ssid, pass);
      while (WiFi.status() != WL_CONNECTED) {
        delay(500);
      }
      // ESP32のIPアドレスを出力
      Serial.println("WiFi Connected.");
      Serial.print("IP = ");
      Serial.println(WiFi.localIP());
    }

    void checkStatus() {
      if ((WiFi.status() != WL_CONNECTED)) {
        Serial.println("Reconnecting to WiFi...");
        WiFi.disconnect();
        WiFi.reconnect();
      }
    }
};

Wifi wifi;
