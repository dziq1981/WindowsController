import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
import TemperatureSensor


class Display():
    RST = None 
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)    
    sensor =TemperatureSensor.Si7021()
    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    # Load default font.
    #font = ImageFont.load_default()
    counter=0
    
    def __init__(self, minLine, maxLine) -> None:
        self.minLine = minLine
        self.currentLine = self.minLine
        self.maxLine = maxLine

    def displayTextLine(self, text, clearScreen, lineNumber, fontsize=8):
        font = ImageFont.truetype('Super Mario Bros. 2.ttf', fontsize)
        if clearScreen:
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.draw.text((self.x, self.top+lineNumber), text,  font=font, fill=255)
        
        self.disp.image(self.image)
        self.disp.display()

    def displayTimeString(self,time2Display):    
        text= "{:02d}".format(time2Display.hour) +":" + "{:02d}".format(time2Display.minute)
        print(text)
        self.displayTextLine(text,True,self.currentLine,20)
        self.currentLine+=2
        if self.currentLine>=self.maxLine:
            self.currentLine=self.minLine
            #self.displayStats()

    def clearStr(self, str2clear : str):
        newString = str(str2clear)     
        newString = newString.replace("b'","")
        newString = newString.replace("\\n'","")
        newString = newString.replace("'","")
        print(newString)
        return newString

    def displayTemperature(self):
        temp = self.sensor.readTemp()        
        txt = f"{temp:.1f}°C"
        print(txt)
        self.displayTextLine(txt,True,10,20)

    def displayhumidity(self):
        hum = self.sensor.readHumidity()
        txt = f"{hum:.1f}%"
        print(txt)
        self.displayTextLine(txt,True,10,20)


    def displayInLoop(self,time2display):
        if self.counter == 0:
            self.displayTimeString(time2display)
        elif self.counter == 1:
            self.displayStats()
        elif self.counter == 2:
            self.displayTemperature()
        elif self.counter == 3:
            self.displayhumidity()
        else:
            self.displayTimeString(time2display)
            self.counter=0
        self.counter+=1


    def displayStats(self):
            # Draw a black filled box to clear the image.
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        font = ImageFont.load_default()
        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = self.clearStr(subprocess.check_output(cmd, shell = True ))
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = self.clearStr(subprocess.check_output(cmd, shell = True ))
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = self.clearStr(subprocess.check_output(cmd, shell = True ))
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = self.clearStr(subprocess.check_output(cmd, shell = True ))

        self.draw.text((self.x, self.top),       "IP: " + str(IP),  font=font, fill=255)
        self.draw.text((self.x, self.top+8),     str(CPU), font=font, fill=255)
        self.draw.text((self.x, self.top+16),    str(MemUsage),  font=font, fill=255)
        self.draw.text((self.x, self.top+24),    str(Disk),  font=font, fill=255)

        # Display image.
        self.disp.image(self.image)
        self.disp.display()
        