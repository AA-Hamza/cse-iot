from classes.Command import Command
import Adafruit_CharLCD as LCD


class LCD16x2Command(Command):
    name = "lcd16x2"
    state = None
    lcd: LCD.Adafruit_CharLCD

    def __init__(self,
                 lcd_rs=25,
                 lcd_en=24,
                 lcd_d4=23,
                 lcd_d5=17,
                 lcd_d6=18,
                 lcd_d7=22,
                 lcd_backlight=4):
        self.lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                        lcd_d7, 16, 2, lcd_backlight)

    def execute(self, payload) -> dict:
        if (isinstance(payload, str)):
            self.lcd.clear()
            self.lcd.message(payload)
            self.state = payload
            result = {
                "feedback": {
                    "message":
                    "successfully written {message} on lcd".format(
                        message=payload)
                }
            }
            return result
        else:
            result = {
                "feedback": {
                    "error": "payload supported types are [str]"
                }
            }
            return result
