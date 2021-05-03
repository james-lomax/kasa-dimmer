import tkinter
from bulb import BulbService

bulb = BulbService("bedroom")

def on_power_press():
    print("Power!")
    bulb.toggle_power()

def on_saturation_scale(val):
    v = int(val)
    print("Set s v=%d" % v)
    bulb.set_saturation(v)

def on_brightness_scale(val):
    v = int(val)
    print("Set b v=%d" % v)
    bulb.set_brightness(v)

root = tkinter.Tk()
root.title('Scale example')

root.columnconfigure(0, pad=5)
root.columnconfigure(1, pad=15)
root.rowconfigure(0, pad=5)

swt = tkinter.Button(root, text="Power", width=8, command=on_power_press)
swt.grid(column=0, row=0)

s1 = tkinter.Scale(root, from_=0, to=100, orient=tkinter.HORIZONTAL, command=on_saturation_scale)
s1.grid(column=0, row=1)

s2 = tkinter.Scale(root, from_=0, to=100, orient=tkinter.HORIZONTAL, command=on_brightness_scale)
s2.grid(column=0, row=2)

root.geometry("600x440+300+300")
root.mainloop()