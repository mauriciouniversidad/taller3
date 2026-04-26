import socket
import threading

clientes = {}
clientes_lock = threading.Lock()

def transmitir(mensaje, remitente_socket):
    """Envía un mensaje de texto normal a todos los clientes excepto al remitente."""
    with clientes_lock:
        for sock in clientes:
            if sock != remitente_socket:
                try:
                    sock.sendall(mensaje.encode('utf-8'))
                except BrokenPipeError:
                    pass 

def transmitir_usuarios():
    """Envía la lista exacta de nombres conectados a todos los clientes."""
    with clientes_lock:
        nombres = list(clientes.values())
    
    datos = "|".join(nombres)
    mensaje_oculto = f"/users {datos}"
    
    with clientes_lock:
        for sock in clientes:
            try:
                sock.sendall(mensaje_oculto.encode('utf-8'))
            except:
                pass

def manejar_cliente(sc, addr):
    nombre = ""
    try:
        data_nombre = sc.recv(1024)
        if not data_nombre: return
        
        nombre = data_nombre.decode('utf-8').strip()
        if not nombre: nombre = f"Anonimo_{addr[1]}"

        with clientes_lock:
            clientes[sc] = nombre
        
        aviso_union = f"[SISTEMA]: *** {nombre} se ha unido al chat ***"
        print(f"[{addr[0]}] {aviso_union}")
        transmitir(aviso_union, sc)
        transmitir_usuarios() # Actualiza la lista al entrar

        while True:
            data = sc.recv(1024)
            if not data: break 
            
            msg = data.decode('utf-8').strip()
            if msg.lower() == "exit": break 
            
            msg_final = f"{nombre}: {msg}"
            print(f"[{addr[0]}] {msg_final}")
            transmitir(msg_final, sc)

    except ConnectionResetError:
        print(f"[AVISO] {nombre} ({addr[0]}) cerró la conexión abruptamente.")
    except Exception as e:
        print(f"[ERROR] Problema con {addr}: {e}")
    finally:
        aviso_salida = ""
        with clientes_lock:
            if sc in clientes:
                del clientes[sc]
                aviso_salida = f"[SISTEMA]: *** {nombre} ha abandonado el chat ***"
        
        if aviso_salida:
            print(f"[{addr[0]}] {aviso_salida}")
            transmitir(aviso_salida, sc)
            transmitir_usuarios() # Actualiza la lista al salir
            
        sc.close()

def iniciar_servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    s.bind(("0.0.0.0", 25565))
    s.listen(15)
    s.settimeout(1.0)
    
    print("========================================")
    print(" SERVIDOR DE CHAT ROBUSTO (Puerto 25565)")
    print("========================================")

    try:
        while True:
            try:
                sc, addr = s.accept()
                hilo = threading.Thread(target=manejar_cliente, args=(sc, addr))
                hilo.daemon = True 
                hilo.start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\n[!] Apagando servidor...")
    finally:
        s.close()

if __name__ == "__main__":
    iniciar_servidor()