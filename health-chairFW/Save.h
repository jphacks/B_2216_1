#pragma once

#include <Arduino.h>
#include <EEPROM.h>

#define VER 7

struct DATA_SET {
  int check;
  int id;
  float offset[4];
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
        save();
      }
    }
  public:
    DATA_SET data;
    void setup() {
      Serial.println("### EEPROM INIT ###");
      EEPROM.begin(1024);
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
