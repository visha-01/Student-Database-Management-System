from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw, ImageFont
import random
import string

# ---------------- CAPTCHA Generation ---------------- #
def generate_captcha():
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    image = Image.new('RGB', (150, 50), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Optional: load system font, fallback to default if not available
    try:
        font = ImageFont.truetype('arial.ttf', 36)
    except:
        font = ImageFont.load_default()

    draw.text((20, 5), captcha_text, font=font, fill=(0, 0, 0))

    image.save('captcha.png')
    return captcha_text

# ---------------- Login Function ---------------- #
def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    elif captchaEntry.get().strip().upper() != captcha_code:
        messagebox.showerror('Error', 'CAPTCHA is incorrect')
        refresh_captcha()
    elif usernameEntry.get() == 'vis' and passwordEntry.get() == '123':
        messagebox.showinfo('Success', 'Welcome')
        window.destroy()
        import sms  # Replace with your own module
    else:
        messagebox.showerror('Error', 'Please enter correct credentials')

# ---------------- Toggle Password Visibility ---------------- #
def toggle_password():
    if showPassVar.get():
        passwordEntry.config(show='')
    else:
        passwordEntry.config(show='●')

# ---------------- Refresh CAPTCHA ---------------- #
def refresh_captcha():
    global captcha_code, captcha_photo
    captcha_code = generate_captcha()
    captcha_img = ImageTk.PhotoImage(Image.open('captcha.png'))
    captchaLabel.config(image=captcha_img)
    captchaLabel.image = captcha_img

# ---------------- Main Window ---------------- #
window = Tk()
window.geometry('1280x700+0+0')
window.title('Login System of Student Management System')
window.resizable(False, False)

# ---------------- Background ---------------- #
backgroundImage = ImageTk.PhotoImage(file='bg.jpg')  # Use your own bg image
bgLabel = Label(window, image=backgroundImage)
bgLabel.place(x=0, y=0)

# ---------------- Login Frame ---------------- #
loginFrame = Frame(window, bg='white', bd=2, relief=SOLID)
loginFrame.place(x=450, y=200)

# ---------------- Logo ---------------- #
logoImage = PhotoImage(file='logo.png')  # Use your own logo
logoLabel = Label(loginFrame, image=logoImage, bg='white')
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

# ---------------- Username ---------------- #
usernameImage = PhotoImage(file='user.png')  # Optional icon
usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT,
                      font=('times new roman', 18, 'bold'), bg='white', fg='black')
usernameLabel.grid(row=1, column=0, pady=10, padx=20)

usernameEntry = Entry(loginFrame, font=('times new roman', 18), bd=3)
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

# ---------------- Password ---------------- #
passwordImage = PhotoImage(file='password.png')  # Optional icon
passwordLabel = Label(loginFrame, image=passwordImage, text='Password', compound=LEFT,
                      font=('times new roman', 18, 'bold'), bg='white', fg='black')
passwordLabel.grid(row=2, column=0, pady=10, padx=20)

passwordEntry = Entry(loginFrame, font=('times new roman', 18), bd=3, show='●')
passwordEntry.grid(row=2, column=1, pady=10, padx=20)

# ---------------- Show Password Toggle ---------------- #
showPassVar = BooleanVar()
showPasswordLabel = Label(loginFrame, text='Show Password', bg='white', fg='black',
                          font=('times new roman', 12))
showPasswordLabel.grid(row=3, column=0, padx=20, sticky='e')

showPasswordCheck = Checkbutton(loginFrame, variable=showPassVar, command=toggle_password,
                                bg='white', activebackground='white')
showPasswordCheck.grid(row=3, column=1, sticky='w')

# ---------------- CAPTCHA Section ---------------- #
Label(loginFrame, text='CAPTCHA', font=('times new roman', 18, 'bold'),
      bg='white', fg='black').grid(row=4, column=0, pady=10, padx=20)

captchaFrame = Frame(loginFrame, bg='white')
captchaFrame.grid(row=4, column=1, pady=10, padx=10)

captcha_code = generate_captcha()
captcha_img = ImageTk.PhotoImage(Image.open('captcha.png'))

captchaLabel = Label(captchaFrame, image=captcha_img, bg='white', bd=1, relief=SOLID)
captchaLabel.pack(side=LEFT)

refreshButton = Button(captchaFrame, text='↻', font=('Arial', 12, 'bold'), command=refresh_captcha,
                       bg='white', relief=FLAT, padx=5)
refreshButton.pack(side=LEFT, padx=5)

captchaEntry = Entry(loginFrame, font=('times new roman', 18), bd=3)
captchaEntry.grid(row=5, column=0, columnspan=2, pady=10, padx=20)

# ---------------- Login Button ---------------- #
Button(loginFrame, text='Login', font=('times new roman', 14, 'bold'), bd=3,
       width=15, fg='white', bg='cornflowerblue', activebackground='blue',
       cursor='hand2', command=login).grid(row=6, column=0, columnspan=2, pady=20)

window.mainloop()
