from classes.Command import Command
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd


class LCD16x2Command(Command):
    name = "lcd16x2"
    state = None
    lcd: characterlcd.Character_LCD_Mono

    def __init__(self,
                 rs="D19",
                 en="D21",
                 d4="D31",
                 d5="D33",
                 d6="D35",
                 d7="D37"):
        self.lcd = characterlcd.Character_LCD_Mono(
            rs=digitalio.DigitalInOut(getattr(board, rs)),
            en=digitalio.DigitalInOut(getattr(board, en)),
            db4=digitalio.DigitalInOut(getattr(board, d4)),
            db5=digitalio.DigitalInOut(getattr(board, d5)),
            db6=digitalio.DigitalInOut(getattr(board, d6)),
            db7=digitalio.DigitalInOut(getattr(board, d7)),
            columns=16,
            lines=2)
        self.lcd.clear()
        self.state = ""

    def execute(self, payload) -> dict:
        if (isinstance(payload, str)):
            self.lcd.clear()
            self.lcd.message = payload
            self.state = payload
            result = {
                "feedback": {
                    "message":
                    "successfully written {message} on lcd".format(
                        message=payload)
                },
                self.name: payload
            }
            return result
        else:
            result = {
                "feedback": {
                    "error": "payload supported types are [str]"
                }
            }
            return result
