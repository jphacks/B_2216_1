import processing.serial.*;
Serial myPort;

float []data = new float [4];

int prev_x = 255;
int prev_y = 255;

void setup() {
  size( 500, 500 );
  background( 255 );
  circle(250, 250, 490);
  noStroke();
  myPort = new Serial(this, Serial.list()[0], 500000);
}

void draw() {
  float sum = data[0]+data[1]+data[2]+data[3];
  float x = (data[0]+data[1]-data[2]-data[3])/sum*300;
  float y = (data[0]-data[1]-data[2]+data[3])/sum*300;

  fill(255);
  noStroke();
  circle(prev_x, prev_y, sum*2);
  fill(255);
  stroke(0);
  circle(250, 250, 490);
  fill(0, 0, 255);
  noStroke();
  circle(int(x)+250, int(y)+250, sum*1.8);

  prev_x = int(x)+250;
  prev_y = int(y)+250;
}

//送られてきたデータを処理する関数
void serialEvent(Serial p) {
  String inString = myPort.readStringUntil('\n');

  if (inString != null) {
    inString = trim(inString);
    if (Float.isNaN(float(split(inString, ','))[0])) {
      return;
    }
    data = float(split(inString, ','));
    data[0] = data[0] + 5;
    data[1] = data[1] + 5;
    data[2] = data[2] + 5;
    data[3] = data[3] + 5;
  }
}
