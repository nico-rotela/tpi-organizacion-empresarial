import csv

# funcion para cargar los empleados 
def cargar_empleados():
    empleados = []

    with open("empleados.csv", "r", encoding="utf-8") as archivo:
        # convierto cada fila en diccionario usando los encabezados
        lector = csv.DictReader(archivo)

        for fila in lector:
            # vienen como texto los paso a int
            fila["legajo"] = int(fila["legajo"])
            fila["dias_disponibles"] = int (fila["dias_disponibles"])
        
            empleados.append(fila)

    return empleados

# filtro empleado
def buscar_empleado(empleados, legajo):

    # busco el empleado y lo retorno
    for empleado in empleados:
        if empleado["legajo"] == legajo:
            return empleado

    # no se encuentra el empleado
    return None

# funcion para guardar los cambios realizados en los empleados
def guardar_empleados(empleados):

    with open("empleados.csv", "w", newline="", encoding="utf-8") as archivo:

        # encabezados del archivo csv
        campos = ["legajo", "nombre", "dias_disponibles"]

        # crea el escritor para guardar los datos
        escritor = csv.DictWriter(archivo, fieldnames=campos)

        # escribe los encabezados
        escritor.writeheader()

        # escribe todos los empleados actualizados
        escritor.writerows(empleados)

# funcion para registrar las solicitudes realizadas por los empleados
def registrar_solicitud(legajo, nombre, dias_solicitados, estado):

    # obtiene el siguiente id disponible
    with open("solicitudes.csv", "r", encoding="utf-8") as archivo:
        lineas = list(csv.reader(archivo))
        nuevo_id = len(lineas)

    with open("solicitudes.csv", "a", newline="", encoding="utf-8") as archivo:

        # crea el escritor para agregar una nueva solicitud
        escritor = csv.writer(archivo)

        #  guarda la solicitud en el archivo csv
        escritor.writerow([
            nuevo_id,
            legajo,
            nombre,
            dias_solicitados,
            estado
        ])

# FUNCION PRINCIPAL PARA GESTIONAR LA SOLICITUD DE VACACIONES
def solicitar_vacaciones():

    # cargo los empleados desde el csv
    empleados = cargar_empleados()

    # solicito legajo del empleado
    try:
        legajo = int(input("Ingrese su número de legajo: "))
    except ValueError:
        print("Debe ingresar un número válido.")
        return

    # se busca el empleado por legajo
    empleado = buscar_empleado(empleados, legajo)

    # valido que exista
    if empleado is None:
        print("Legajo inexistente.")
        return

    print(f"\nEmpleado: {empleado['nombre']}")
    print(f"Días disponibles: {empleado['dias_disponibles']}")

    # valido que posea dias disponibles
    if empleado["dias_disponibles"] <= 0:
        print("No posee días disponibles.")
        return

    # solicita al usuario la cantidad de dias a pedir
    try:
        dias_solicitados = int(input("¿Cuántos días desea solicitar?: "))
    except ValueError:
        print("Debe ingresar un número válido.")
        return

    # valida que la cantidad sea mayor a cero 
    if dias_solicitados <= 0:
        print("La cantidad de días debe ser mayor a cero.")
        return

    # valido que no solicite mas dias de los dispopnibles
    if dias_solicitados > empleado["dias_disponibles"]:
        print("Saldo insuficiente. Solicitud rechazada.")

        # registra la solicitud rechazada
        registrar_solicitud(
            legajo,
            empleado["nombre"],
            dias_solicitados,
            "Rechazada"
        )

        return

    # descuenta los dias aprobados al empleado
    empleado["dias_disponibles"] -= dias_solicitados

    # guarda los cambios en el archivo de empleados
    guardar_empleados(empleados)

    # registro solicitud aprobada
    registrar_solicitud(
        legajo,
        empleado["nombre"],
        dias_solicitados,
        "Aprobada"
    )

    print("\nSolicitud aprobada.")
    print(f"Nuevo saldo: {empleado['dias_disponibles']} días.")

while True:
    print("\nBOT RRHH")
    print("1. Solicitar vacaciones")
    print("2. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        solicitar_vacaciones()

    elif opcion == "2":
        break

    else:
        print("Opción inválida.")
