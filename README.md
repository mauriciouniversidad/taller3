# 🚀 Taller: Chat Multihilo con Sockets TCP
**Asignatura:** Sistemas Operativos | **Docente:** Juan Torres Ossandón 
**Fecha:** 26 de abril de 2026

---

## 👥 Equipo de Trabajo
**Integrantes:** Mauricio Hernandez, Ignacio Brizuela, Francisco Seura, Cristian Rojo, Pablo Manque, Raul Muñoz, Gabriel Muñoz. 
---

## 📋 Resumen del Taller
Este proyecto consiste en la implementación de una aplicación de chat distribuida para aplicar conceptos fundamentales de **Sistemas Operativos**.El propósito es utilizar la comunicación entre procesos mediante red y la gestión de tareas simultáneas. 

### 🎯 Objetivos Logrados
**Conectividad de Red:** Aplicación de la API de **Sockets** para el envío y recepción de datos en computadoras remotas. 
**Concurrencia Eficiente:** Uso de **Threads** (hilos) para ejecutar instrucciones de manera independiente y realizar múltiples tareas. 
**Sincronización:** Resolución de desafíos en la coordinación de hilos que acceden a recursos compartidos.

---

## 🛠️ Desarrollo de la Actividad
Para asegurar la replicabilidad, el desarrollo se ejecutó en las siguientes etapas:

1.  **Servidor (Ubuntu):** Se creó un servidor capaz de esperar mensajes de clientes y reenviarlos a toda la sala mediante un bucle "for". 
2.  **Cliente (Windows):** Implementación de una GUI que solicita nombre de usuario y permite la interacción en tiempo real. 
3.  **Optimizaciones Realizadas:**
    * Inclusión de mensaje de salida (`exit`) para desconexión limpia. 
    * Mejoras para evitar errores al cerrar sockets e hilos. 
    * Identificación de usuario visible para todos los integrantes. 
---

## 📈 Resultados y Conclusiones
* **Estabilidad:** Se logró eliminar usuarios de la lista al desconectarse, cerrando el hilo de comunicación de forma correcta. 
* **Flexibilidad:** Los sockets permitieron crear una aplicación cliente-servidor funcional en un entorno de red real. 
* **Observación:** Es vital el diseño cuidadoso al usar múltiples hilos para evitar comportamientos no deseados en recursos compartidos. 

---

## 📚 Referencias
* Guía de Laboratorio #3: Procesos con hilos (Threads) y Socket. 
