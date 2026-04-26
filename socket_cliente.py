import socket
import threading
import sys
import tkinter as tk
import random
import winsound 
from tkinter import scrolledtext, simpledialog, messagebox
from plyer import notification  

# --- CONFIGURACIÓN ---
# Si tus amigos se conectan desde fuera, cambia esto por tu IP Pública
IP_SERVIDOR = "201.246.129.205" 
PUERTO = 25565

class ClienteChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat en Línea")
        self.root.geometry("550x650")
        self.root.configure(bg="#2C2F33")

        self.colores_disponibles = ["#FF5733", "#33FF57", "#5733FF", "#FF33A8", "#33FFF6", "#FFD700", "#FF8C33"]
        self.animando = False 

        self.root.withdraw()
        self.username = simpledialog.askstring("Identificación", "Ingresa tu nombre de usuario:", parent=self.root)
        
        if not self.username or not self.username.strip():
            self.root.destroy()
            sys.exit()
            
        self.root.deiconify()
        self.crear_interfaz()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root.protocol("WM_DELETE_WINDOW", self.desconectar)

        threading.Thread(target=self.conectar_al_servidor, daemon=True).start()

    def crear_interfaz(self):
        # --- BARRA SUPERIOR (Contador) ---
        frame_superior = tk.Frame(self.root, bg="#2C2F33")
        frame_superior.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        self.lbl_contador = tk.Label(frame_superior, text="Online: Conectando...", bg="#2C2F33", fg="#43B581", font=("Arial", 10, "bold"))
        self.lbl_contador.pack(side=tk.RIGHT)

        # --- ÁREA DE CHAT ---
        self.area_chat = scrolledtext.ScrolledText(self.root, state='disabled', bg="#23272A", fg="white", font=("Arial", 11), wrap=tk.WORD)
        self.area_chat.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # --- BARRA INFERIOR (Controles) ---
        frame_inferior = tk.Frame(self.root, bg="#2C2F33")
        frame_inferior.pack(padx=10, pady=(0, 10), fill=tk.X)

        self.entrada_msg = tk.Entry(frame_inferior, bg="#40444B", fg="white", font=("Arial", 12), borderwidth=0, insertbackground="white")
        self.entrada_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=8)
        self.entrada_msg.bind("<Return>", lambda event: self.enviar_mensaje())
        self.entrada_msg.focus_set()

        btn_temblor = tk.Button(frame_inferior, text="💢", bg="#E67E22", fg="white", font=("Arial", 12, "bold"), 
                                 command=self.enviar_zumbido, relief=tk.FLAT, padx=10)
        btn_temblor.pack(side=tk.LEFT, padx=2)

        btn_enviar = tk.Button(frame_inferior, text="Enviar", bg="#5865F2", fg="white", font=("Arial", 10, "bold"), 
                               command=self.enviar_mensaje, relief=tk.FLAT, padx=15)
        btn_enviar.pack(side=tk.LEFT, padx=2)

        btn_salir = tk.Button(frame_inferior, text="Salir", bg="#ED4245", fg="white", font=("Arial", 10, "bold"), 
                              command=self.desconectar, relief=tk.FLAT, padx=10)
        btn_salir.pack(side=tk.LEFT, padx=2)

    def reproducir_sonido(self):
        try:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except: pass

    def animar_zumbido(self, contador=0, orig_x=None, orig_y=None):
        if contador == 0:
            if self.animando: return 
            self.animando = True
            
            self.reproducir_sonido()
            self.root.deiconify()
            self.root.attributes('-topmost', True)
            self.root.focus_force()
            self.root.attributes('-topmost', False)

            self.root.update_idletasks()
            orig_x = self.root.winfo_x()
            orig_y = self.root.winfo_y()

        if contador < 25: 
            dx = random.randint(-15, 15)
            dy = random.randint(-15, 15)
            self.root.geometry(f"+{orig_x + dx}+{orig_y + dy}")
            self.root.after(15, self.animar_zumbido, contador + 1, orig_x, orig_y)
        else:
            self.root.geometry(f"+{orig_x}+{orig_y}")
            self.animando = False

    def enviar_zumbido(self):
        try:
            self.s.sendall("/zum".encode('utf-8'))
            self.mostrar_mensaje(f"{self.username}: /zum")
        except OSError:
            self.mostrar_mensaje("Error: No se puede enviar, sin conexión.", es_sistema=True)

    def mostrar_mensaje(self, mensaje, es_sistema=False):
        self.area_chat.config(state='normal')
        if es_sistema:
            self.area_chat.insert(tk.END, f" {mensaje}\n", "sistema")
            self.area_chat.tag_config("sistema", foreground="#95A5A6", font=("Arial", 10, "italic"))
        else:
            if "/zum" in mensaje.lower():
                nombre = mensaje.split(":")[0] if ":" in mensaje else "Alguien"
                self.area_chat.insert(tk.END, f"\n💢 {nombre.strip()} ha enviado un zumbido 💢\n", "zumbido")
                self.area_chat.tag_config("zumbido", foreground="#E67E22", font=("Arial", 11, "bold"), justify="center")
                self.animar_zumbido()
            elif ":" in mensaje:
                try:
                    nombre_parte, texto_parte = mensaje.split(":", 1)
                    nombre_parte = nombre_parte.strip()
                    color = self.obtener_color_por_nombre(nombre_parte)
                    self.area_chat.insert(tk.END, f"{nombre_parte}:", nombre_parte)
                    self.area_chat.tag_config(nombre_parte, foreground=color, font=("Arial", 11, "bold"))
                    self.area_chat.insert(tk.END, f" {texto_parte.strip()}\n")
                    if nombre_parte != self.username:
                        self.lanzar_notificacion(f"Mensaje de {nombre_parte}", texto_parte.strip())
                except: self.area_chat.insert(tk.END, f"{mensaje}\n")
            else: self.area_chat.insert(tk.END, f"{mensaje}\n")
        
        self.area_chat.config(state='disabled')
        self.area_chat.yview(tk.END)

    def conectar_al_servidor(self):
        try:
            self.mostrar_mensaje(f"Conectando a {IP_SERVIDOR}...", es_sistema=True)
            self.s.connect((IP_SERVIDOR, PUERTO))
            self.s.sendall(self.username.encode('utf-8'))
            self.mostrar_mensaje("¡Conectado!", es_sistema=True)
            threading.Thread(target=self.recibir_datos, daemon=True).start()
        except ConnectionRefusedError:
            self.mostrar_mensaje("Error: Servidor apagado o inaccesible.", es_sistema=True)
        except Exception as e:
            self.mostrar_mensaje(f"Error de conexión: {e}", es_sistema=True)

    def recibir_datos(self):
        while True:
            try:
                data = self.s.recv(1024).decode('utf-8')
                if not data: 
                    self.root.after(0, self.mostrar_mensaje, "Servidor cerrado.", True)
                    self.root.after(0, lambda: self.lbl_contador.config(text="Online: 0", fg="#ED4245"))
                    break
                
                # Intercepta el comando oculto del servidor
                if data.startswith("/users "):
                    cantidad = data.split(" ")[1] 
                    self.root.after(0, lambda c=cantidad: self.lbl_contador.config(text=f"Online: {c}"))
                else:
                    self.root.after(0, self.mostrar_mensaje, data)
                    
            except ConnectionResetError:
                self.root.after(0, self.mostrar_mensaje, "Conexión perdida con el servidor.", True)
                self.root.after(0, lambda: self.lbl_contador.config(text="Online: Error", fg="#ED4245"))
                break
            except ConnectionAbortedError:
                break
            except OSError:
                break

    def enviar_mensaje(self):
        msg = self.entrada_msg.get().strip()
        if msg:
            try:
                self.s.sendall(msg.encode('utf-8'))
                self.mostrar_mensaje(f"{self.username}: {msg}")
                self.entrada_msg.delete(0, tk.END)
            except BrokenPipeError:
                self.mostrar_mensaje("Error: Se perdió la conexión al enviar.", es_sistema=True)
            except Exception as e:
                self.mostrar_mensaje(f"Error inesperado: {e}", es_sistema=True)

    def desconectar(self):
        try:
            self.s.sendall("exit".encode('utf-8'))
            self.s.close()
        except: pass
        self.root.destroy()
        sys.exit()

    def lanzar_notificacion(self, t, m):
        if not self.root.focus_displayof():
            try: notification.notify(title=t, message=m, app_name='Chat', timeout=5)
            except: pass

    def obtener_color_por_nombre(self, n):
        return self.colores_disponibles[sum(ord(c) for c in n) % len(self.colores_disponibles)]

if __name__ == "__main__":
    root = tk.Tk()
    app = ClienteChatGUI(root)
    root.mainloop()