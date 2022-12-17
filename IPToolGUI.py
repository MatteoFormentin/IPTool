import tkinter as tk

class IPToolGUI:
    def __init__(self):
        self.app = tk.Tk()
        self.app.resizable(width=False, height=False)
        self.app.wm_title("IPTool")
        self.app.wm_iconname("IPTool")
        self.app.geometry("400x300")
        self.app.configure(background="#282828")
        #self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

    def run(self):
        self.app.mainloop()

ip = IPToolGUI()
ip.run()