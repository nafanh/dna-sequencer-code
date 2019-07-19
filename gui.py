import tkinter as tk

# --- functions ---

def in_folder():
    global is_folder
    is_folder = var.get()

def folder_name():
    global f_name
    f_name = var2.get()
    
def time_pts():
    global time
    time = var3.get()
    
def get_x_min():
    global x_min
    x_min = var4.get()

def get_x_max():
    global x_max
    x_max = var5.get()

def get_y_min():
    global y_min
    y_min = var6.get()

def get_y_max():
    global y_max
    y_max = var7.get()

  
# --- main ---

root = tk.Tk()

var = tk.StringVar()
var2 = tk.StringVar()
var3 = tk.IntVar()
var4 = tk.IntVar()
var5 = tk.IntVar()
var6 = tk.IntVar()
var7 = tk.IntVar()

tk.Label(root,text='In Folder?').grid(row=0)
tk.Label(root,text='Folder Name').grid(row=1)
tk.Label(root,text='Num Time Points').grid(row=2)
tk.Label(root,text='x Minimum').grid(row=3)
tk.Label(root,text='x Maximum').grid(row=4)
tk.Label(root,text='y Minimum').grid(row=5)
tk.Label(root,text='y Maximum').grid(row=6)


ent = tk.Entry(root, textvariable=var)
ent.grid(row=0,column=1)

ent2 = tk.Entry(root, textvariable=var2)
ent2.grid(row=1,column=1)

ent3 = tk.Entry(root, textvariable=var3)
ent3.grid(row=2,column=1)

ent4 = tk.Entry(root, textvariable=var4)
ent4.grid(row=3,column=1)

ent5 = tk.Entry(root, textvariable=var5)
ent5.grid(row=4,column=1)

ent6 = tk.Entry(root, textvariable=var6)
ent6.grid(row=5,column=1)

ent7 = tk.Entry(root, textvariable=var7)
ent7.grid(row=6,column=1)


but = tk.Button(root, text="Enter", command=in_folder).grid(row=0,column=3)
but2 = tk.Button(root, text="Enter", command=folder_name).grid(row=1,column=3)
but3 = tk.Button(root, text="Enter", command=time_pts).grid(row=2,column=3)
but4 = tk.Button(root, text="Enter", command=get_x_min).grid(row=3,column=3)
but5 = tk.Button(root, text="Enter", command=get_x_max).grid(row=4,column=3)
but6 = tk.Button(root, text="Enter", command=get_y_min).grid(row=5,column=3)
but7 = tk.Button(root, text="Enter", command=get_y_max).grid(row=6,column=3)

tk.Button(root, 
          text='Quit', 
          command=root.quit).grid(row=7, 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)
root.mainloop()

