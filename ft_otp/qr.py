import random
import qrcode

from PIL import Image


# Muestra un código QR aleatorio por pantalla.
def mostrar_qr():
    # Generar un código QR aleatorio
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(random.randint(0, 1000000))
    qr.make(fit=True)

    # Mostrar el código QR
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr.png")
    img.show()
    img.close()


if __name__ == "__main__":
    mostrar_qr()
    print("Fin del programa")
    input("Pulsa ENTER para salir")
    exit(0)
