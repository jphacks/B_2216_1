#include "Hx711.h"
#include "Save.h"
#include "Wifi.h"
#include "Ble.h"

#include <HTTPClient.h>

#define HX711_DATA_1 23
#define HX711_CLK_1 22

#define HX711_DATA_2 21
#define HX711_CLK_2 19

#define HX711_DATA_3 18
#define HX711_CLK_3 17

#define HX711_DATA_4 16
#define HX711_CLK_4 15

const char* ssid = "TP-Link_0338";
const char* pass = "09968035";

int count = 0;

void setup() {
  Serial.begin(500000);
  delay(500);
  Serial.println("");
  save.setup();
  scale.setup(HX711_DATA_1, HX711_CLK_1, HX711_DATA_2, HX711_CLK_2, HX711_DATA_3, HX711_CLK_3, HX711_DATA_4, HX711_CLK_4);
  // scale.calibrate();
  ble.setup();
  wifi.setup(ssid, pass);
}

void loop() {
  scale.upd();

  /* jsonの作成*/
  char w_json[100];
  char w0[6];
  char w1[6];
  char w2[6];
  char w3[6];
  dtostrf(scale.getWeight(0), 5, 2, w0);
  dtostrf(scale.getWeight(1), 5, 2, w1);
  dtostrf(scale.getWeight(2), 5, 2, w2);
  dtostrf(scale.getWeight(3), 5, 2, w3);
  sprintf(w_json, "{\"id\":%d,\"w0\":%s,\"w1\":%s,\"w2\":%s,\"w3\":%s}", save.data.id, w0, w1, w2, w3);
  //Serial.println(w_json);

  wifi.checkStatus();

  /* http送信*/
  if (count > 200) {
    HTTPClient httpClient;
    httpClient.begin("http://api.jphacks2022.so298.net/data/");
    httpClient.addHeader("Content-Type", "application/json");
    //  POSTしてステータスコードを取得する
    int status_code = httpClient.POST((uint8_t *)w_json, strlen(w_json));
    if (status_code == 200)
    {
      //Serial.println("[POST]Send to server");
    } else {
      //Serial.println("[POST]failed to send to server");
    }
    httpClient.end();
    count = 0;
  }
  count++;

  /* BLE送信 */
  ble.write(w_json);
  delay(100);

  /* print*/
  //Serial.println(scale.getWeight(0) + scale.getWeight(1) + scale.getWeight(2) + scale.getWeight(3));
  Serial.print(scale.getWeight(0)); Serial.print(",");
  Serial.print(scale.getWeight(1)); Serial.print(",");
  Serial.print(scale.getWeight(2)); Serial.print(",");
  Serial.println(scale.getWeight(3));


  if (Serial.available() > 0) {
    // 受信したデータの1バイトを読み取る
    char incoming = Serial.read();
    if (incoming == 'r') {
      ESP.restart();
    }else if(incoming=='c'){
      scale.calibrate();
    }
  }
}
