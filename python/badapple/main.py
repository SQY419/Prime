import hpprime
hpprime.dimgrob(1, 256, 192, 16777215)
hpprime.dimgrob(2, 320, 240, 16777215)


char_to_bin = {"A":"000000","B":"000001","C":"000010","D":"000011","E":"000100","F":"000101","G":"000110","H":"000111","I":"001000","J":"001001","K":"001010","L":"001011","M":"001100","N":"001101","O":"001110","P":"001111","Q":"010000","R":"010001","S":"010010","T":"010011","U":"010100","V":"010101","W":"010110","X":"010111","Y":"011000","Z":"011001","a":"011010","b":"011011","c":"011100","d":"011101","e":"011110","f":"011111","g":"100000","h":"100001","i":"100010","j":"100011","k":"100100","l":"100101","m":"100110","n":"100111","o":"101000","p":"101001","q":"101010","r":"101011","s":"101100","t":"101101","u":"101110","v":"101111","w":"110000","x":"110001","y":"110010","z":"110011","0":"110100","1":"110101","2":"110110","3":"110111","4":"111000","5":"111001","6":"111010","7":"111011","8":"111100","9":"111101","+":"111110","/":"111111","":"0"}
ii = 0
z = ""


def draw_frame_data(data):
    global ii, z
    z = ""
    for i in range(len(data)-1):
        z += char_to_bin[data[i]]
    ii = 0
    recursively_draw(0, 0, 256)


def recursively_draw(x, y, s):
    global ii, z
    if x < 256 and y < 192:
        ii += 1
        if s == 1:
            draw(x, y, s, z[ii - 1])
            return
        if z[ii - 1] == "0":
            ii += 1
            draw(x, y, s, z[ii-1])
        else:
            recursively_draw(x, y, s / 2)
            recursively_draw(x + s / 2, y, s / 2)
            recursively_draw(x, y + s / 2, s / 2)
            recursively_draw(x + s / 2, y + s / 2, s / 2)
            

def draw(x, y, s, c):
    if c == "0":
        hpprime.fillrect(1, x, y, s, s, 0, 0)
    else:
        hpprime.fillrect(1, x, y, s, s, 16777215, 16777215)
   

def clear_screen(g): hpprime.fillrect(g, 0, 0, 320, 240, 16777215, 16777215)


print("start.")
clear_screen(0)
time = hpprime.eval('ticks()')
try:
    frame = 0
    start = -200
    a = 0
    k = 1
    while k <= 33:
        with open("split_" + str(k) + ".txt", mode = 'r') as data2:
            dat0 = data2.read()
            data2.close
        b = dat0.split("\n")
        k += 1
        start += 200
        while frame < len(b) - 1 + start:
            t = a
            a = hpprime.eval('ticks()')
            fps = 1000 / (a - t + 1e-10)
            frame = int((a - time) / 30)
            if frame > len(b) - 1 + start:
                break
            try:
                draw_frame_data(b[frame - start])
            except IndexError:
                ...
            clear_screen(2)
            hpprime.strblit(2, 0, 0, 320, 240, 1)
            hpprime.textout(2, 0, 220, "fps:{:<3}".format(fps), 0x969696)
            hpprime.blit(0, 0, 0, 2)
except KeyboardInterrupt:
    print()
