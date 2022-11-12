#include "Hx711.h"
#include "Save.h"
#include "Wifi.h"
#include "Ble.h"

#include <HTTPClient.h>
#include <ArduinoJson.h>

#define HX711_DATA_1 23
#define HX711_CLK_1 22

#define HX711_DATA_2 21
#define HX711_CLK_2 19

#define HX711_DATA_3 18
#define HX711_CLK_3 17

#define HX711_DATA_4 16
#define HX711_CLK_4 15

//#define USE_WIFI

const char* ssid = "TP-Link_0338";
const char* pass = "09968035";

int count = 0;

void setup() {
  Serial.begin(500000);
  delay(500);
  Serial.println("");
  save.setup();
  scale.setup(HX711_DATA_1, HX711_CLK_1, HX711_DATA_2, HX711_CLK_2, HX711_DATA_3, HX711_CLK_3, HX711_DATA_4, HX711_CLK_4);
  ble.setup();

#ifdef USE_WIFI
  wifi.setup(ssid, pass);
#endif
}

void loop() {
  /* scaleの更新 */
  scale.update();

  /* jsonの作成*/
  char w_json[100];
  StaticJsonDocument<96> doc;
  doc["id"] = save.data.id;
  doc["w0"] = scale.getWeight(0);
  doc["w1"] = scale.getWeight(1);
  doc["w2"] = scale.getWeight(2);
  doc["w3"] = scale.getWeight(3);
  serializeJson(doc, w_json);
  Serial.println(w_json);

#ifdef USE_WIFI
  /* wifiの状況確認 */
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
#endif

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
    } else if (incoming == 'c') {
      scale.calibrate();
    }
  }
}
