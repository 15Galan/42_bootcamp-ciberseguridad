# Objetivo

Crear una página web y hacerla accesible a través de la **red Tor** mediante la creación de un **servicio oculto**.


## Requisitos

- [x] El servicio debe contar con una página web estática: un solo archivo `index.html`.
	- La página será accesible a través de una URL del tipo *xxxxxxxx.onion*.
	- El contenido de la página será "*up to you*".
- [x] Se utilizará Nginx para configurar el servidor web.
	- No se permite ningún otro servidor o framework.
- [x] Se podrá acceder a la página web por HTTP en el puerto 80.
- [x] El acceso al servidor estará habilitado por SSH en el puerto 4242.
- [x] No debe abrirse ningún otro puerto ni establecerse reglas de firewall.

**Se deben entregar los archivos: `index.html`, `nginx.conf`, `sshd_config` y `torrc`.**


# Funcionamiento

## Instalación

Será necesario usar `Nginx` y `Tor` para poder crear el servicio oculto.

Opcionalmente, también puede usarse una máquina virtual donde montar el servicio oculto (recomiendo usar `VirtualBox` y
`Vagrant`), aunque para ello será necesario hacer un mapeo de puertos para que el servicio sea accesible desde fuera.

1. Crear una máquina virtual con `Vagrant`.
2. Sobre esa máquina: `Ajustes > Red : NAT`.
3. Sobre esa máquina: `Opciones avanzadas > Port forwarding`.
	- Añadir una regla para el puerto _80:80_ (HTTP).
    - Añadir una regla para el puerto _4242:4242_ (SSH).

Una vez instalados los paquetes necesarios, basta con sustituir los archivos entregados por los originales para que se
aplique la configuración indicada y por último, reiniciar los servicios de `Nginx` y `Tor`.


## Comprobación

Para comprobar que el ejercicio es correcto, puede hacerse lo siguiente:

1. Generar un QR de la dirección `onion` del servicio oculto.
   - Por ejemplo, desde [aquí](https://www.qrcode-monkey.com/es)
2. Acceder al servicio oculto usando el navegador Tor del móvil.
   - Disponible [aquí](https://play.google.com/store/apps/details?id=org.torproject.torbrowser&gl=ES).

Si la página es accesible, entonces el servidor se ha montado correctamente.
