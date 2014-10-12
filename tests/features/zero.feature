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

Escenario: Crear un appoitment
	Dado que vaya a "http://127.0.0.1:5000/appointments/create/"
	Debo llenar el campo "title" con "Cita con el dentista"
	Debo llenar el campo "start" con "2010-11-11 12:00:00"
	Debo llenar el campo "end" con "2010-11-11 13:00:00"
	Debo llenar el campo "location" con "Av. Universidad, Guadalupe, Zac."
	Debo llenar el campo "description" con "Cita urgente!!!"
	y enviare el formulario

Escenario: Consultar un appoitment
	Dado que vaya a "http://127.0.0.1:5000/appointments/2/"
	Debo ver que el elemento con clase "appointment-detail" contiene "Past Meeting"

Escenario: Consultar un appoitment que no existe
	Dado que vaya a "http://127.0.0.1:5000/appointments/0/"
	Debo ver que el titulo de la pagina contiene "Not Found"

Escenario: Editar un appoitment
	Dado que vaya a "http://127.0.0.1:5000/appointments/1/edit"
	Debo llenar el campo "title" con "Nuevo Titulo"
	y enviare el formulario
	Debo ver que el elemento con clase "appointment-detail" contiene "Nuevo Titulo"

Escenario: Editar la fecha de un appoitment
	Dado que vaya a "http://127.0.0.1:5000/appointments/1/edit"
	Debo llenar el campo con id "start" con una "fecha actual"
	y enviare el formulario

Escenario: Eliminar un appoitment
	Dado que vaya a "http://127.0.0.1:5000/appointments/"
	Debo seleccionar el appoitment con el titulo "Cita al dentista"
	Debo hacer clic en el boton "Appointment-delete-link"
	Debo ir a "http://127.0.0.1:5000/appoitments/"
	Debo ver que el elemento con la clase  "appointment-detail" no contiene "Cita con el dentista"