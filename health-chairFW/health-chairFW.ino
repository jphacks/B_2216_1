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

#define USE_WIFI

int count = 0;

void setup() {
  Serial.begin(500000);
  delay(500);
  Serial.println("");
  save.setup();
  scale.setup(HX711_DATA_1, HX711_CLK_1, HX711_DATA_2, HX711_CLK_2, HX711_DATA_3, HX711_CLK_3, HX711_DATA_4, HX711_CLK_4);

#ifdef USE_WIFI
  wifi.setup(save.data.ssid, save.data.pass);
#endif
  ble.setup();
}

void loop() {
  /* scaleの更新 */
  scale.update();

  /* jsonの作成*/
  char ios_json[130];
  StaticJsonDocument<100> doc;
  doc["id"] = save.data.id;
  doc["w0"] = scale.getWeight(0);
  doc["w1"] = scale.getWeight(1);
  doc["w2"] = scale.getWeight(2);
  doc["w3"] = scale.getWeight(3);
  doc["wifi"] = wifi.getStatus();
  serializeJson(doc, ios_json);
  //  Serial.println(ios_json);

#ifdef USE_WIFI
  /* http送信*/
  if (count > 200) {
    /* wifiの状況確認 */
    if (!ble.getConnectStatus()) {
      wifi.setup(save.data.ssid, save.data.pass);
    }
    char server_json[130];
    StaticJsonDocument<100> doc;
    doc["id"] = save.data.id;
    doc["w0"] = scale.getWeight(0);
    doc["w1"] = scale.getWeight(1);
    doc["w2"] = scale.getWeight(2);
    doc["w3"] = scale.getWeight(3);
    serializeJson(doc, server_json);

    HTTPClient httpClient;
    httpClient.begin("http://api.jphacks2022.so298.net/data/");
    httpClient.addHeader("Content-Type", "application/json");
    //  POSTしてステータスコードを取得する
    int status_code = httpClient.POST((uint8_t *)server_json, strlen(server_json));
    if (status_code == 200)
    {
      Serial.println("[*] POST Success");
    } else {
      Serial.println("[*] POST Failed");
    }
    httpClient.end();
    count = 0;
  }
  count++;
#endif

  /* BLE送信 */
  ble.write(ios_json);
  ble.checkStatus();
  delay(100);

  /* キャリブ */
  if (ble.getCalibStatus()) {
    scale.calibrate();
  }
  if(ble.getWifiSetupStatus()){
    wifi.setup(save.data.ssid, save.data.pass);
  }

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
