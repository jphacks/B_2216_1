#pragma once
#include <Arduino.h>

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#include "Save.h"
#include "Hx711.h"

#define SERVICE_UUID "2309e44f-cb8d-43fc-95b2-4c7134c23467"
#define CHARACTERISTIC_UUID "37216a09-9f31-40f7-ab16-54ae5b32fd19"

#define BT_NAME "smart-chair"

class BleCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic* pCharacteristic) {
      std::string value = pCharacteristic->getValue();

      if (value.length() > 0) {
        String received = value.c_str();
        Serial.println(received);
        if (received == "calibrate") {
          scale.calibrate();
        } else {
          save.data.id = received.toInt();
          save.save();
        }
      }
    }
};

class Ble {
  private:
    BLECharacteristic* pCharacteristic;
  public:
    void setup() {
      Serial.println("### BLE INIT ###");
      BLEDevice::init(BT_NAME); // この名前がスマホなどに表示される
      BLEServer* pServer = BLEDevice::createServer();
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
      pCharacteristic->setValue(i);
      pCharacteristic->notify();
    }

};

Ble ble;
