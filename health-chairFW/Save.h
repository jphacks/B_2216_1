#pragma once

#include <Arduino.h>
#include <EEPROM.h>
#include <string.h>

#define VER 1

struct DATA_SET {
  int check;
  int id;
  float offset[4];
  char ssid[30];
  char pass[30];
};


class Save {
  private:
    void load() {
      EEPROM.get<DATA_SET>(0, data);
      if (data.check != VER) { //バージョンをチェック
        data.check = VER;
        data.id = 0;
        data.offset[0] = 0;
        data.offset[1] = 0;
        data.offset[2] = 0;
        data.offset[3] = 0;
        strcpy(data.ssid, "");
        strcpy(data.pass, "");
        save();
      }
    }
  public:
    DATA_SET data;
    void setup() {
      Serial.println("### EEPROM INIT ###");
      EEPROM.begin(512);
      load();
      Serial.println("init end.");
    }

    void save() {
      //EEPROMに設定を保存する
      EEPROM.put<DATA_SET>(0, data);
      EEPROM.commit(); //大事
    }
};

Save save;
