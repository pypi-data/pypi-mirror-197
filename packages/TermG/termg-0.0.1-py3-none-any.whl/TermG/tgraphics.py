import os, sys, time, keyboard, math

class Screen:
    def __init__(self, w, h, doColor=True, maxFPS=None):
        self.w = w
        self.h = h
        self.doColor = doColor
        self.maxFPS = maxFPS
        self.prev_time = time.time()
        self.dt = 0
        self.keys = []
        os.system( "" )
        os.system("cls")
        self.clearMatrix()

    def clearMatrix(self):
        self.matrix = []
        for x in range(self.h):
            self.matrix.append([])
            for y in range(self.w):
                self.matrix[-1].append(Pixel(Color(127), Color(255), " "))

    def fill(self, bg=None, fg=None, char=" "):
        if bg == None: bg = Color(0)
        if fg == None: fg = Color(255)
        temp_pixel = Pixel(bg, fg, char)
        self.matrix = []
        for x in range(self.h):
            self.matrix.append([])
            for y in range(self.w):
                self.matrix[-1].append(temp_pixel)

    def drawPixel(self, x, y, bg=None, fg=None, char=" "):
        try:
            if not (x < 0 or y < 0):
                if bg == None: bg = Color(0)
                if fg == None: fg = Color(255)
                self.matrix[y][x] = Pixel(bg, fg, char)
        except:
            pass

    def drawRect(self, x, y, w, h, bg=None, fg=None, char=" "):
        for i in range(w):
            for j in range(h):
                self.drawPixel(x+i, y+j, bg=bg, fg=fg, char=char)

    def drawCircle(self, x, y, r, bg=None, fg=None, char=" "):
        for i in range(r*2):
            for j in range(r*2):
                n_x = -r+i
                n_y = -r+j
                if math.sqrt(abs(n_x)**2 + abs(n_y)**2) <= r:
                    self.drawPixel(x+n_x, y+n_y, bg=bg, fg=fg, char=char)

    def drawStripe(self, x, y, l, hov, bg=None, fg=None, char=" "): #hov = horizontal ("h") or vertical ("v")
        for i in range(l):
            if hov == "h":
                self.drawPixel(x+i, y, bg=bg, fg=fg, char=char)
            else:
                self.drawPixel(x, y+i, bg=bg, fg=fg, char=char)

    def drawLine(self, start_x, start_y, end_x, end_y, bg=None, fg=None, char=" "):
        curr_x = start_x
        curr_y = start_y
        if abs(end_x-start_x) <= abs(end_y-start_y):
            if end_y == start_y:
                avg_x = 1 if (end_x-start_x) > 0 else -1
                avg_y = 0
            else:
                avg_x = abs(abs(end_x-start_x) / abs(end_y-start_y)) * 1 if (end_x-start_x) > 0 else -1
                avg_y = 1 if (end_y-start_y) > 0 else -1
        else:
            if end_x == start_x:
                avg_x = 0
                avg_y = 1 if (end_y-start_y) > 0 else -1
            else:
                avg_x = 1 if (end_x-start_x) > 0 else -1
                avg_y = abs(abs(end_y-start_y) / abs(end_x-start_x)) * 1 if (end_y-start_y) > 0 else -1
        print(avg_x, avg_y)
        tally_x = 0
        tally_y = 0
        while not (abs(curr_x-end_x)+abs(curr_y-end_y)) <= 1:
            curr_x += math.floor(avg_x)
            curr_y += math.floor(avg_y)
            if (abs(curr_x-end_x)+abs(curr_y-end_y)) <= 1: break

            tally_x += abs(abs(avg_x) - abs(math.floor(avg_x)))
            tally_y += abs(abs(avg_y) - abs(math.floor(avg_y)))

            self.drawPixel(curr_x, curr_y, bg=bg, fg=fg, char=char)

            if tally_x >= 1:
                tally_x -= 1
                curr_x += 1 if (end_x-start_x) > 0 else -1
                self.drawPixel(curr_x, curr_y, bg=bg, fg=fg, char=char)
                if (abs(curr_x-end_x)+abs(curr_y-end_y)) <= 1: break
            if tally_y >= 1:
                tally_y -= 1
                curr_y += 1 if (end_y-start_y) > 0 else -1
                self.drawPixel(curr_x, curr_y, bg=bg, fg=fg, char=char)
                if (abs(curr_x-end_x)+abs(curr_y-end_y)) <= 1: break

    def blit(self):
        result = ""
        previous_pixel = Pixel(Color(0), Color(255), " ")
        for i in self.matrix:
            for j in i:
                if self.doColor:
                    result += j.getPixelOptimised(previous_pixel)
                    previous_pixel = j
                else:
                    result += j.char
            result += "\n"
        print("\033[0H")
        if not self.doColor: os.system("color 7")
        print(result)

    def update(self):
        self.blit()
        self.dt = time.time()-self.prev_time
        time.sleep(max(1/self.maxFPS-self.dt,0))
        self.prev_time = time.time()

    def getDelta(self):
        return self.dt

    def addKeys(self, *args):
        for key in args:
            if not key in self.keys: self.keys.append(key)

    def getKeyPresses(self):
        returnable = {}
        for key in self.keys:
            returnable.update({key:keyboard.is_pressed(key)})
        return returnable

    def quit(self):
        os.system("color 7")
        os.system("cls")
        sys.exit()

class Pixel:
    def __init__(self, bg, fg, char):
        self.bg = f"\033[48;2;{bg.r};{bg.g};{bg.b}m"
        self.fg = f"\033[38;2;{fg.r};{fg.g};{fg.b}m"
        self.char = char

    def getPixel(self):
        return self.bg + self.fg + self.char

    def getPixelOptimised(self, prev_pixel):
        r_bg = self.bg
        if self.bg == prev_pixel.bg: r_bg = ""
        r_fg = self.fg
        if self.fg == prev_pixel.fg: r_fg = ""
        return r_bg + r_fg + self.char

class Color:
    def __init__(self, *args):
        if len(args) == 0:
            self.r = self.g = self.b = "0"
        if len(args) == 1 or len(args) == 2:
            self.r = self.g = self.b = str(args[0])
        else:
            self.r = str(args[0])
            self.g = str(args[1])
            self.b = str(args[2])

class Sprite:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.matrix = []
        self.clearMatrix()

    def clearMatrix(self):
        self.matrix = []
        for x in range(self.h):
            self.matrix.append([])
            for y in range(self.w):
                self.matrix[-1].append(Pixel(Color(127), Color(255), " "))
