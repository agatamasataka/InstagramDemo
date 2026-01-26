import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

def drop(event):
    print(event.data)

root = TkinterDnD.Tk()
root.geometry('200x200')
lb = tk.Label(root, text='Drag and drop files here')
lb.pack(fill='both', expand=True)

# register the label as a drop target
lb.drop_target_register(DND_FILES)
lb.dnd_bind('<<Drop>>', drop)

root.mainloop()
