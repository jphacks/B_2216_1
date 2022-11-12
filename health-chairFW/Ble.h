#pragma once
#include <Arduino.h>

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <ArduinoJson.h>
#include <string.h>

#include "Save.h"
#include "Hx711.h"

#define SERVICE_UUID "2309e44f-cb8d-43fc-95b2-4c7134c23467"
#define CHARACTERISTIC_UUID "37216a09-9f31-40f7-ab16-54ae5b32fd19"

#define BT_NAME "smart-chair"

static bool deviceConnected = false;
static bool calibStatus = false;
static bool wifiStatus = false;

class BleServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      Serial.println("[*] BLE connected");
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
      Serial.println("[*] BLE disconnected");
    }
};

class BleCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic* pCharacteristic) {
      std::string value = pCharacteristic->getValue();

      if (value.length() > 0) {
        String received = value.c_str();
        Serial.println(received);

        StaticJsonDocument<150> doc;

        // Deserialize the JSON document
        DeserializationError error = deserializeJson(doc, received);

        if (doc["ssid"] != nullptr) {
          /* ssid pass設定 */
          strcpy(save.data.ssid, doc["ssid"].as<const char*>());
          strcpy(save.data.pass, doc["pass"].as<const char*>());
          
          Serial.print("Wifi setting to ");
          Serial.print(save.data.ssid);
          Serial.print(" ");
          Serial.println(save.data.pass);
          
          save.save();
          wifiStatus = true;
          
          return;
        } else {
          if (received == "calibrate") {
            calibStatus = true;
          } else {
            save.data.id = received.toInt();
            save.save();
            Serial.print("ID: ");
            Serial.println(save.data.id);
          }
        }
      }
    }
};

class Ble {
  private:
    BLECharacteristic* pCharacteristic;
    BLEServer* pServer = NULL;
    bool oldDeviceConnected = false;

  public:
    void setup() {
      Serial.println("### BLE INIT ###");
      BLEDevice::init(BT_NAME); // この名前がスマホなどに表示される
      pServer = BLEDevice::createServer();
      pServer->setCallbacks(new BleServerCallbacks());
      BLEService* pService = pServer->createService(SERVICE_UUID);
      pCharacteristic = pService->createCharacteristic(
                          CHARACTERISTIC_UUID,
                          BLECharacteristic::PROPERTY_READ |
                          BLECharacteristic::PROPERTY_WRITE |
                          BLECharacteristic::PROPERTY_NOTIFY |
                          BLECharacteristic::PROPERTY_INDICATE
                        );
      pCharacteristic->setCallbacks(new BleCallbacks());
      pService->start();
      BLEAdvertising* pAdvertising = BLEDevice::getAdvertising();
      pAdvertising->addServiceUUID(SERVICE_UUID);
      pAdvertising->setScanResponse(true);
      pAdvertising->setMinPreferred(0x06);  // iPhone接続の問題に役立つ
      pAdvertising->setMinPreferred(0x12);
      BLEDevice::startAdvertising();
      Serial.println("init end.");
    }

    void write(char* i) {
      if (deviceConnected) {
        pCharacteristic->setValue(i);
        pCharacteristic->notify();
      }
    }

    void checkStatus() {
      // disconnecting
      if (!deviceConnected && oldDeviceConnected) {
        delay(500); // give the bluetooth stack the chance to get things ready
        pServer->startAdvertising(); // restart advertising
        Serial.println("### BLE start advertising ###");
        oldDeviceConnected = deviceConnected;
      }
      // connecting
      if (deviceConnected && !oldDeviceConnected) {
        // do stuff here on connecting
        oldDeviceConnected = deviceConnected;
      }
    }

    bool getCalibStatus() {
      if (calibStatus) {
        calibStatus = false;
        return true;
      }
      return false;
    }

    bool getWifiSetupStatus(){
      if(wifiStatus){
        wifiStatus = false;
        return true;
      }
      return false;
    }

    bool getConnectStatus(){
      return deviceConnected;
    }

};

Ble ble;
