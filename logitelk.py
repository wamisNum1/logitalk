from customtkinter import *
import threading
from socket import socket,AF_INET,SOCK_STREAM


class RegisterWindow(CTk):
    def __init__(self):
        super().__init__()
        self.username = None
        self.title("Приєднатися до сервера")
        self.geometry("300x300")
        self.label = CTkLabel(self,text="Вхід в LogiTalk",font=('Arial',20,'bold'))
        self.label.pack(pady=40)
        
        self.entry = CTkEntry(self,placeholder_text="Введіть ім'я")
        self.entry.pack()
        
        self.host_entry = CTkEntry(self,placeholder_text="Введіть хост")
        self.host_entry.pack()
        
        self.port_entry = CTkEntry(self,placeholder_text="Введіть порт")
        self.port_entry.pack()
        
        self.join_btn = CTkButton(self,text="Приєднатися",command=self.start_chat)
        self.join_btn.pack(pady=5)   
        
    def start_chat(self):
        self.username = self.username = self.entry.get()

        try:
            self.sock = socket(AF_INET,SOCK_STREAM)
            self.sock.connect((self.host_entry.get(),int(self.port_entry.get())))
            hello = f"{self.username} приєднався до чату!\n"
            self.sock.send(hello.encode())
            win = MainWindow(self.sock,self.username)
            self.destroy()
            win.mainloop()
        except:
            print("Не вдалося підкючитися до сервера")


class MainWindow(CTk):
    def __init__(self,sock,username):
        super().__init__()
        self.sock = sock
        self.username = username
        self.title("Chat Client")
        self.geometry("400x300")

        self.frame_width = 0
        self.is_show_menu = False

        self.frame = CTkFrame(self, fg_color='light blue', width=self.frame_width, height=self.winfo_height())
        self.frame.pack_propagate(False)
        self.frame.columnconfigure(0, weight=1)
        self.frame.place(x=0, y=0)

        self.btn = CTkButton(self, text='menu', command=self.toggle_show_menu, width=30)
        self.btn.place(x=0, y=0)
        
        self.chat_text = CTkTextbox(self,state="disabled")
        self.chat_text.place(x=0,y=30)
        
        self.message_input = CTkEntry(self,placeholder_text="Введіть повідомлення")
        self.message_input.place(x=0,y=250)
        
        self.send_btn = CTkButton(self, text="▶️", width=30,command=self.send_message)
        self.send_btn.place(x=200,y=250)
        
        self.label_name = CTkLabel(self.frame,text="Ім'я")
        self.label_name.pack(pady=30)
        
        self.entry = CTkEntry(self.frame,placeholder_text="Ваш нік...")
        self.entry.pack()
        
        self.save_btn = CTkButton(self.frame,text="Зберегти",command=self.change_name)
        self.save_btn.pack()
        
        self.adaptive_ui()
        
        
        
        
    def change_name(self):
        new_name = self.entry.get()
        if new_name:
            self.username = new_name
            self.add_message(f"Ваш новий нік: {self.username}")

    def adaptive_ui(self):
        self.chat_text.configure(width=self.winfo_width()-self.frame.winfo_width(),height=self.winfo_height()-self.message_input.winfo_height()-30)
        self.chat_text.place(x=self.frame.winfo_width())
        self.message_input.configure(width=self.winfo_width()-self.frame.winfo_width()-self.send_btn.winfo_width())
        self.message_input.place(x=self.frame.winfo_width(),y=self.winfo_height()-self.send_btn.winfo_height())
        self.send_btn.place(x=self.winfo_width()-self.send_btn.winfo_width(),y=self.winfo_height()-self.send_btn.winfo_height())
        self.after(20,self.adaptive_ui)
        
    def add_message(self, text):
        self.chat_text.configure(state="normal")
        self.chat_text.insert(END,text+"\n")
        self.chat_text.configure(state="disable")
        
    def send_message(self):
        message = self.message_input.get()
        if message:
            self.add_message(f"{self.username}: {message}")
            data = f"TEXT@{message}\n"
            try:
                pass
            except:
                pass
        self.message_input.delete(0, END)


    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.close_menu()
        else:
            self.is_show_menu = True
            self.show_menu()

    def show_menu(self):
        if self.frame_width < 200:
            self.frame_width += 5
            self.frame.configure(width=self.frame_width, height=self.winfo_height())
            self.btn.configure(width=max(self.frame_width, 30))
            if self.is_show_menu:
                self.after(10, self.show_menu)

    def close_menu(self):
        if self.frame_width > 0:
            self.frame_width -= 5
            self.frame.configure(width=self.frame_width, height=self.winfo_height())
            self.btn.configure(width=max(self.frame_width, 30))
            if not self.is_show_menu:
                self.after(10, self.close_menu)

if __name__ == "__main__":
    RegisterWindow().mainloop()

#pasxalko1488!