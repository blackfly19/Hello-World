import tkinter as tk
import requests as rq
import json
import threading
import hashlib

LARGE_FONT = ("Courier 10 Pitch",18,"bold","italic")
USERNAME = ""
LOCAL = "http://blackfly19.pythonanywhere.com/"
RECEIVE_THREAD = None


class page_controller(tk.Tk):


	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		self.configure(background='white')
		self.title("Hello World")
		self.geometry("400x400")

		container = tk.Frame(self,bg='white')

		container.pack(side="top",fill="both",expand=True)

		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)

		self.frames = {}

		for F in (Login, Register,Chat):	
		
			frame = F(container,self)
			self.frames[F] = frame
			frame.grid(row=0,column=0,sticky="nsew")

		self.show_frame(Login,"Login")

	def show_frame(self,cont,frame_name):

		global RECEIVE_THREAD
		if frame_name == "Chat":
			RECEIVE_THREAD.start()
		frame = self.frames[cont]
		frame.tkraise()

class Login(tk.Frame):

	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent,bg='white')

		self.head_frame = tk.Frame(self,bg='white')
		self.head_frame.pack()

		self.body_frame = tk.Frame(self,bg='white')
		self.body_frame.pack()

		self.error_msg = tk.StringVar()

		self.head = tk.Label(self.head_frame,text="Hello World",font = LARGE_FONT,bg='white',fg='red')
		self.head.pack()

		self.page_head = tk.Label(self.head_frame,text="Login",font = LARGE_FONT,bg='white',fg='green')
		self.page_head.pack(side="bottom",pady = (20,0))

		self.username = tk.Label(self.body_frame,text = 'username',bg='white')
		self.password = tk.Label(self.body_frame,text='password',bg='white')
		self.username_entry = tk.Entry(self.body_frame)
		self.password_entry = tk.Entry(self.body_frame,show='*')
		self.login = tk.Button(self.body_frame,text="Login",command = lambda: self.check_login_credentials(controller,self.username_entry.get(),self.password_entry.get()))
		self.create = tk.Button(self.body_frame,text="Create New Account",command=lambda: controller.show_frame(Register,"Register"))

		self.username.grid(row=0,pady=(100,5),padx=10)
		self.password.grid(row=1,pady=(10,5))
		self.username_entry.grid(row=0,column=1,pady=(100,5),padx=10)
		self.password_entry.grid(row=1,column=1,pady=(10,5))
		self.login.grid(columnspan =  2,pady = (30,10))
		self.create.grid(columnspan=2,pady=(0,20))

	def check_login_credentials(self,controller,username,password):

		global USERNAME
		temp = hashlib.md5(password.encode())
		password = temp.hexdigest()
		credentials = rq.get(LOCAL+'userdetails/'+username)
		self.error_msg.set('')
		self.error = tk.Label(self.body_frame,textvariable = self.error_msg,bg='white')
		self.error.grid(columnspan = 2,pady = (5,15))

		if credentials.status_code != 404:
			login = json.loads(credentials.text)
			if login['username'] == username and login['password'] == password:
				USERNAME = username
				controller.show_frame(Chat,"Chat")
			else:
				self.error_msg.set('Password entered is incorrect')
		else:
			self.error_msg.set('Account does not exist')

class Register(tk.Frame):

	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent,bg='white')

		self.head_frame = tk.Frame(self,bg='white')
		self.head_frame.pack()

		self.body_frame = tk.Frame(self,bg='white')
		self.body_frame.pack()

		self.head = tk.Label(self.head_frame,text="Hello World",font = LARGE_FONT,bg='white',fg='red')
		self.head.pack()

		self.page_head = tk.Label(self.head_frame,text="Register",font = LARGE_FONT,bg='white',fg='green')
		self.page_head.pack(side="bottom",pady=(20,0))

		self.username = tk.Label(self.body_frame,text = 'username',bg='white')
		self.password = tk.Label(self.body_frame,text='password',bg='white')
		self.username_entry = tk.Entry(self.body_frame)
		self.password_entry = tk.Entry(self.body_frame,show='*')
		self.create = tk.Button(self.body_frame,text="Create",command=lambda: self.send_data_to_Rest(controller,self.username_entry.get(),self.password_entry.get()))

		self.username.grid(row=0,pady=(100,5),padx=10)
		self.password.grid(row=1,pady=(10,5))
		self.username_entry.grid(row=0,column=1,pady=(100,5),padx=10)
		self.password_entry.grid(row=1,column=1,pady=(10,5))
		self.create.grid(columnspan=2,pady=(30,10))


	def send_data_to_Rest(self,controller,username,password):
		global USERNAME
		temp = hashlib.md5(password.encode())
		password = temp.hexdigest()
		user = rq.get(LOCAL+'userdetails/'+username)
		if(user.status_code != 404):
			self.error = tk.Label(self.body_frame,text="Account already exists!",bg='white')
			self.error.grid(columnspan=2,pady=(5,15))
		else:
			rq.post(LOCAL+'users/',data={'username':username,'password':password})
			USERNAME = username
			controller.show_frame(Chat,"Chat")

class Chat(tk.Frame):

	def __init__(self,parent,controller):
		global RECEIVE_THREAD

		tk.Frame.__init__(self,parent,bg='white')
		self.message = tk.StringVar()
		self.scroll = tk.Scrollbar(self)

		self.message_list = tk.Listbox(self,height=19,width=47,yscrollcommand=self.scroll.set)
		self.scroll.pack(side=tk.RIGHT,fill=tk.Y)
		self.message_list.pack()
		
		self.send_message = tk.Entry(self,textvariable=self.message)
		self.send_message.bind("<Return>",self.send)
		self.send_message.pack()
		self.send_button = tk.Button(self,text="Send",command = self.send)
		self.send_button.pack(side="bottom")
		self.stack = []
		self.stack_len = len(self.stack)
		RECEIVE_THREAD = threading.Thread(target=self.receive)


	def send(self,event=None):
		post_message = self.message.get()
		display = USERNAME+': '+post_message
		self.message_list.insert(tk.END,display)
		self.stack.append(display)
		self.stack_len += 1
		self.message.set("")
		rq.post(LOCAL+'chat/',data={'username':USERNAME,'message':post_message})

	def receive(self):

		while True:
			req = rq.get(LOCAL+'chat/')
			values = req.text
			messages = json.loads(values)
			display = ""
			if len(messages) > self.stack_len:
				for i in range(len(messages) - self.stack_len):
					display = messages[i + self.stack_len]['username']+': '+messages[i + self.stack_len]['message']
					self.stack.append(display)
					self.message_list.insert(tk.END,display)
					display = ""
				self.stack_len = len(self.stack)

app = page_controller()
app.mainloop()
