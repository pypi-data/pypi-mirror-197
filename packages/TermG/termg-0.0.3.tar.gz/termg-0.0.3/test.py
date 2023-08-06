from src.TermG import termg as tg
import time

pos_x = 30
pos_y = 15
sc = tg.Screen(51, 25, doColor=True)
sc.addKeys("up", "down", "left", "right", "escape")
sc.maxFPS = 30
while True:
    sc.fill(bg=tg.Color(127))
    sc.drawRect(1, 1, 49, 23, bg=tg.Color(255))
    sc.drawCircle(26, 13, 3, bg=tg.Color(0))
    sc.drawLine(26, 13, pos_x, pos_y, bg=tg.Color(0, 0, 255)) # doesn't work yet
    sc.drawPixel(pos_x, pos_y, bg=tg.Color(None), fg=tg.Color(255, 0, 0), char="X")
    sc.update()
    keys = sc.getKeyPresses()
    if keys["up"]:
        pos_y -= 1
    if keys["down"]:
        pos_y += 1
    if keys["left"]:
        pos_x -= 1
    if keys["right"]:
        pos_x += 1
    if keys["escape"]:
        sc.quit()
