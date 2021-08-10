import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Display():
    RST = None 
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

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
    font = ImageFont.load_default()
    

    def displayTextLine(self, text, clearScreen, lineNumber):
 #       now = datetime.now()
 #       text= str(now.hour) +":" + str(now.minute)
         
        if clearScreen:
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.draw.text((self.x, self.top+lineNumber), text,  font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()
        