# Introducción

La recolección de evidencias es una parte fundamental en la realización de un forense, ya que disponer de la información clara y organizada es algo que puede facilitar su labor.


# Objetivo

Crear un programa que, dado un rango de fechas, sea capaz de extraer diversa información de un sistema Windows como la actividad del usuario, los programas abiertos, el historial de navegación, distinta información del registro de Windows... en dicho rango de tiempo.

- [x] Fechas de cambio de ramas de registro (*CurrentVersionRun*).
- [x] Archivos recientes.
- [x] Archivos temporales.
- [x] Programas instalados.
- [x] Programas abiertos.
- [x] Historial de navegación.

Si no se facilita un rango de tiempo, podría tomar un valor por defecto, por ejemplo, las últimas 24 horas, la última semana o el último mes.


# Funcionamiento

El programa puede recibir (o no) una fecha de inicio (argumento de $\texttt{-i}$) y una fecha de fin (argumento de $\texttt{-f}$) y mostrará por pantalla, de forma ordenada, la información que se ha extraído.

```console
$ python3 recovery.py -h

usage: recovery.py [-h] [-i inicio] [-f final]

Programa para obtener información de un sistema Windows.

options:
  -h, --help  show this help message and exit
  -i inicio   Fecha inicial del rango de fechas en formato 'DD-MM-AAAA'
              (por defecto, '01-01-1970').
  -f final    Fecha final del rango de fechas en formato 'DD-MM-AAAA'
              (por defecto, hoy).

Ejercicio 'recovery' del Bootcamp de Ciberseguridad de la Fundación 42 (Málaga).
```

Si el programa **no recibe alguna** de las 2 fechas requeridas, se usarán sus valores por defecto; si el programa **no recibe ninguna** de las 2 fechas, se usará un rango de un mes (30 días) a partir de hoy.
