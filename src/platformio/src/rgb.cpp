#include <Adafruit_NeoPixel.h>
#define NEO_PIXEL_PIN D8

class RackRGB {
    private:
    Adafruit_NeoPixel strip;    
    const uint32_t COLORS[4] = {
        strip.Color(255, 255, 255),
        strip.Color(255, 0, 0),
        strip.Color(0, 255, 0),
        strip.Color(0, 0, 255)};

    int color_idx = 0;

    public:
    RackRGB() {
        strip = Adafruit_NeoPixel(56, NEO_PIXEL_PIN, NEO_GRB + NEO_KHZ800);
    }

    void begin() {
        strip.begin();
        strip.clear();
        strip.show();
    }

    void update() {
        color_idx++;
        if (color_idx > 3)
        {
            color_idx = 0;
        }
        strip.clear();
        strip.fill(COLORS[color_idx], 0, strip.numPixels());
        delay(50);
        strip.show();
    }

    void theaterChase(uint32_t color, int wait)
    {
        for (int a = 0; a < 10; a++)
        { // Repeat 10 times...
            for (int b = 0; b < 3; b++)
            {                  //  'b' counts from 0 to 2...
                strip.clear(); //   Set all pixels in RAM to 0 (off)
                // 'c' counts up from 'b' to end of strip in steps of 3...
                for (int c = b; c < strip.numPixels(); c += 3)
                {
                    strip.setPixelColor(c, color); // Set pixel 'c' to value 'color'
                }
                strip.show(); // Update strip with new contents
                delay(wait);  // Pause for a moment
            }
        }
    }

    void theaterChaseRainbow(int wait)
    {
        int firstPixelHue = 0; // First pixel starts at red (hue 0)
        for (int a = 0; a < 30; a++)
        { // Repeat 30 times...
            for (int b = 0; b < 3; b++)
            {                  //  'b' counts from 0 to 2...
                strip.clear(); //   Set all pixels in RAM to 0 (off)
                // 'c' counts up from 'b' to end of strip in increments of 3...
                for (int c = b; c < strip.numPixels(); c += 3)
                {
                    // hue of pixel 'c' is offset by an amount to make one full
                    // revolution of the color wheel (range 65536) along the length
                    // of the strip (strip.numPixels() steps):
                    int hue = firstPixelHue + c * 65536L / strip.numPixels();
                    uint32_t color = strip.gamma32(strip.ColorHSV(hue)); // hue -> RGB
                    strip.setPixelColor(c, color);                       // Set pixel 'c' to value 'color'
                }
                strip.show();                // Update strip with new contents
                delay(wait);                 // Pause for a moment
                firstPixelHue += 65536 / 90; // One cycle of color wheel over 90 frames
            }
        }
    }
};