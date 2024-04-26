#include <Arduino.h>
#include <U8g2lib.h>
#include <Wire.h>
#include "video.h"

#define FPS 12
#define IMG_SIZE 1024 // image size in byte
// Define OLED display object
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0);

unsigned long long start;
unsigned long current_img;

void setup()
{
  // Initialize I2C communication
  Wire.begin();

  // Initialize the display
  u8g2.begin();
  start = millis();
  current_img = 0;
}

void loop()
{
  while ((current_img + 1) == (unsigned long)long((millis() - start) / 1000 * FPS))
    ; // Wait until it is time to print the next image

  if (current_img == nbr_img)
    current_img = 0;
  start = millis();

  u8g2.firstPage();
  do
  {
    u8g2.drawXBMP(0, 0, 128, 64, &images[current_img * IMG_SIZE]);
  } while (u8g2.nextPage());
  current_img++;
}
