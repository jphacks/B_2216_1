#pragma once

#include "HX711.h"
#include <stdint.h>
#include "Save.h"

#define SENSOR_NUM 4

class Hx711 {
  private:
    HX711 scale[SENSOR_NUM];
    float weight[SENSOR_NUM];
    float divider[SENSOR_NUM] = {47880, 49791, 50805, 61491};
  public:
    void setup(uint8_t data_pin1, uint8_t clk_pin1, uint8_t data_pin2, uint8_t clk_pin2, uint8_t data_pin3, uint8_t clk_pin3, uint8_t data_pin4, uint8_t clk_pin4) {
      Serial.println("### SENSOR INIT ###");
      scale[0].begin(data_pin1, clk_pin1);
      scale[1].begin(data_pin2, clk_pin2);
      scale[2].begin(data_pin3, clk_pin3);
      scale[3].begin(data_pin4, clk_pin4);
      for (int i = 0; i < SENSOR_NUM; i++) {
        weight[i] = 0;
      }
      Serial.println("init end");
    };

    void calibrate() {
      Serial.println("### SENSOR CALIBRATE ###");
      delay(1000);
      float t = 10;
      save.data.offset[0] = 0;
      save.data.offset[1] = 0;
      save.data.offset[2] = 0;
      save.data.offset[3] = 0;
      for (int j = 0; j < t; j++) {
        for (int i = 0; i < SENSOR_NUM; i++) {
          save.data.offset[i] += (float)scale[i].read() / (float)t;
        }
      }
      save.save();
      Serial.println("calibrate end");
    }

    void upd() {
      for (int i = 0; i < SENSOR_NUM; i++) {
        float alpha = 0.92;
        weight[i] = weight[i] * alpha + (scale[i].read() - save.data.offset[i]) / divider[i] * (1 - alpha);
      }
    }

    float getWeight(int num) {
      if (num < 0 || num >= SENSOR_NUM) {
        Serial.println("getWeight: index out of range.");
        return 0;
      }
      return weight[num] < 0 ? 0 : weight[num];
    }
};

Hx711 scale;
