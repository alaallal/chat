import socket
from tkinter import *
from tkinter import ttk
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8000))

# Главное окно
r = Tk()
r.geometry("200x200")
r.resizable(False, False)
r.title("Бу, испугался? Не бойся!")

client_name = ""
separator_token = "<SEP>"


def new_wind():
    r.withdraw()  # Скрываем основное окно
    window = Toplevel(r)  # Создаем новое окно
    window.geometry("400x500")
    window.resizable(False, False)
    window.title("Бу, испугался? Не бойся!")

    # Поле для сообщений
    message_area = Text(window, wrap='word', state='disabled')
    message_area.pack(expand=True, fill='both', padx=10, pady=10)

    # Поле для ввода сообщения
    input_message = ttk.Entry(window)
    input_message.pack(fill='x', padx=10, pady=10)

    def send_message():
        msg = input_message.get()
        if msg:
            full_msg = f"{client_name}{separator_token}{msg}"
            client_socket.send(full_msg.encode())  # Отправляем сообщение
            display_message(f"{client_name}: {msg}")  # Отображаем собственное сообщение
            input_message.delete(0, END)  # Очищаем поле после отправки

    send_button = ttk.Button(window, text="Отправить", command=send_message)
    send_button.pack(pady=5)

    def display_message(msg):
        message_area.config(state='normal')  # Даем возможность редактировать текстовое поле
        message_area.insert(END, f"{msg}\n")  # Добавляем сообщения в текстовое поле
        message_area.see(END)  # Прокручиваем к последнему сообщению
        message_area.config(state='disabled')  # Блокируем редактирование

    def listen_for_messages():
        while True:
            try:
                msg = client_socket.recv(1024).decode()
                if separator_token in msg:
                    sender_name, message = msg.split(separator_token, 1)
                    if message.strip():  # Показать сообщение только если оно не пустое
                        display_message(f"{sender_name}: {message.strip()}")  # Отображаем полученные сообщения
                else:
                    display_message(f"{msg} присоединился")  # Изменяем строку для присоединения
            except Exception as e:
                print(f"[!] Ошибка: {e}")
                break

    # Отображаем сообщение о том, что клиент присоединился
    display_message(f"{client_name} присоединился")

    # Запускаем поток для прослушивания сообщений от сервера
    threading.Thread(target=listen_for_messages, daemon=True).start()


def show_message():
    global client_name
    n = name.get()
    if n:  # Проверяем, что имя не пустое
        client_name = n  # Сохраняем имя клиента
        client_socket.send(n.encode())  # Отправляем имя на сервер    name.delete(0, END)  # Очищаем поле после отправки
        new_wind()

name = ttk.Entry(r)
name.pack(anchor=CENTER, padx=8, pady=20)

reg = ttk.Button(r, text="Join", command=show_message)
reg.pack(anchor=CENTER)

r.mainloop()

