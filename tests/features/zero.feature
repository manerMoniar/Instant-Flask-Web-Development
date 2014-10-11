# -*- coding: utf-8 -*-
# language: es

Funcionalidad: Administrar agenda

Escenario: Ingresar al sistema
    Dado que vaya a "http://127.0.0.1:5000/login/"
    Debo llenar el campo "username" con "admin@mail.com"
    Debo llenar el campo "password" con "pass"
    Y enviare el formulario

Escenario: Ver lista de citas
    Dado que vaya a "http://127.0.0.1:5000/appointments/"
    Debo ver la "1" cita "Day Off"
    Debo ver la "2" cita "Past Meeting"
    Debo ver la "3" cita "Important Meeting"
    Debo ver la "4" cita "Follow Up"
