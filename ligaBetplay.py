import os  

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


equipos = []
jugadores_por_equipo = []
tecnicos_por_equipo = []


local_partido = []
visitante_partido = []
fechas_partido = []
goles_local = []
goles_visitante = []

def registrar_equipo():
    clear_console()
    while True:
        nombre = input("Ingresa el nombre del equipo: ").strip().capitalize()
        try:
            for c in nombre:
                if c.isdigit():
                    raise ValueError("No se permiten números en el nombre.")
            if nombre in equipos:
                raise ValueError("Ese equipo ya está registrado.")
            equipos.append(nombre)
            jugadores_por_equipo.append([])
            tecnicos_por_equipo.append([])
            print(f"Equipo '{nombre}' registrado correctamente.")
            break
        except ValueError as e:
            print(f"Error: {e}")
    input("\nPresiona Enter para continuar...")
    clear_console()

def registrar_jugador(indice_equipo):
    clear_console()
    nombre_jugador = input("Nombre del jugador: ").strip().capitalize()
    while True:
        dorsal_str = input("Dorsal (número entero): ").strip()
        if dorsal_str.isdigit():
            dorsal = int(dorsal_str)
            break
        print("Por favor, ingresa un número de dorsal válido.")
    posicion = input("Posición de juego: ").strip()
    jugadores_por_equipo[indice_equipo].append((nombre_jugador, dorsal, posicion))
    eq = equipos[indice_equipo]
    print(f"El jugador {nombre_jugador} con dorsal {dorsal} y posición {posicion} "
          f"se ha registrado correctamente en {eq}.")
    input("\nPresiona Enter para continuar...")
    clear_console()

def registrar_tecnico(indice_equipo):
    clear_console()
    nombre_tecnico = input("Nombre del técnico: ").strip().capitalize()
    cargo = input("Cargo: ").strip()
    tecnicos_por_equipo[indice_equipo].append((nombre_tecnico, cargo))
    eq = equipos[indice_equipo]
    print(f"Técnico '{nombre_tecnico}' con cargo '{cargo}' registrado en {eq}.")
    input("\nPresiona Enter para continuar...")
    clear_console()

def registrar_fecha():
    clear_console()
    if len(equipos) < 2:
        print("No hay suficientes equipos registrados.")
        input("\nPresiona Enter para continuar...")
        clear_console()
        return

    print("Equipos disponibles:")
    for i, nom in enumerate(equipos, 1):
        print(f"{i}. {nom}")
    try:
        idx_local = int(input("Selecciona número de equipo local: ")) - 1
        idx_visit = int(input("Selecciona número de equipo visitante: ")) - 1
        if idx_local == idx_visit or not (0 <= idx_local < len(equipos)) or not (0 <= idx_visit < len(equipos)):
            raise IndexError
    except (ValueError, IndexError):
        print("Selección inválida de equipos.")
        input("\nPresiona Enter para continuar...")
        clear_console()
        return

    while True:
        fecha = input("Ingresa la fecha (dd-mm-aa): ").strip()
        if fecha.count("-") != 2:
            print("Formato inválido. Usa dd-mm-aa.")
        elif fecha in fechas_partido:
            print("Ya existe un partido programado para ese día.")
            input("\nPresiona Enter para continuar...")
            clear_console()
            return
        else:
            break

    local_partido.append(equipos[idx_local])
    visitante_partido.append(equipos[idx_visit])
    fechas_partido.append(fecha)
    goles_local.append(None)
    goles_visitante.append(None)
    print(f"{equipos[idx_local]} vs {equipos[idx_visit]} se ha programado para {fecha}.")
    input("\nPresiona Enter para continuar...")
    clear_console()

def registrar_marcador():
    clear_console()
    if not fechas_partido:
        print("No hay partidos programados.")
        input("\nPresiona Enter para continuar...")
        clear_console()
        return

    print("Partidos registrados:")
    for i, fecha in enumerate(fechas_partido, 1):
        print(f"{i}. {local_partido[i-1]} vs {visitante_partido[i-1]} - {fecha}")
    try:
        sel = int(input("Selecciona el número del partido: ")) - 1
        if not (0 <= sel < len(fechas_partido)):
            raise IndexError
    except (ValueError, IndexError):
        print("Selección inválida.")
        input("\nPresiona Enter para continuar...")
        clear_console()
        return

    while True:
        gl = input(f"Goles de {local_partido[sel]}: ").strip()
        if gl.isdigit():
            goles_local[sel] = int(gl)
            break
        print("Ingresa un número válido.")
    while True:
        gv = input(f"Goles de {visitante_partido[sel]}: ").strip()
        if gv.isdigit():
            goles_visitante[sel] = int(gv)
            break
        print("Ingresa un número válido.")

    print(f"Marcador {local_partido[sel]} {goles_local[sel]} - {goles_visitante[sel]} {visitante_partido[sel]} registrado.")
    input("\nPresiona Enter para continuar...")
    clear_console()

def equipo_con_mas_goles_favor():
    clear_console()
    if all(g is None for g in goles_local + goles_visitante):
        print("Aún no hay marcadores registrados.")
    else:
        totales = {e: 0 for e in equipos}
        for eq, g in zip(local_partido, goles_local):
            if g is not None: totales[eq] += g
        for eq, g in zip(visitante_partido, goles_visitante):
            if g is not None: totales[eq] += g
        mejor = max(totales, key=totales.get)
        print(f"Equipo con más goles a favor: {mejor} ({totales[mejor]} goles)")
    input("\nPresiona Enter para continuar...")
    clear_console()

def equipo_con_mas_goles_contra():
    clear_console()
    if all(g is None for g in goles_local + goles_visitante):
        print("Aún no hay marcadores registrados.")
    else:
        totales = {e: 0 for e in equipos}
        for eq, g in zip(local_partido, goles_visitante):
            if g is not None: totales[eq] += g
        for eq, g in zip(visitante_partido, goles_local):
            if g is not None: totales[eq] += g
        peor = max(totales, key=totales.get)
        print(f"Equipo con más goles en contra: {peor} ({totales[peor]} goles)")
    input("\nPresiona Enter para continuar...")
    clear_console()

def mostrar_tabla_posiciones():
    clear_console()
    tabla = {e: {"pj":0,"pg":0,"pe":0,"pd":0,"gf":0,"gc":0} for e in equipos}
    for L, V, gl, gv in zip(local_partido, visitante_partido, goles_local, goles_visitante):
        if gl is None or gv is None: continue
        tabla[L]["pj"] += 1; tabla[V]["pj"] += 1
        tabla[L]["gf"] += gl; tabla[L]["gc"] += gv
        tabla[V]["gf"] += gv; tabla[V]["gc"] += gl
        if gl > gv:
            tabla[L]["pg"] += 1; tabla[V]["pd"] += 1
        elif gl < gv:
            tabla[V]["pg"] += 1; tabla[L]["pd"] += 1
        else:
            tabla[L]["pe"] += 1; tabla[V]["pe"] += 1

    for stats in tabla.values():
        stats["dg"] = stats["gf"] - stats["gc"]
        stats["pt"] = stats["pg"]*3 + stats["pe"]

    print(f"{'Equipo':<15}{'PJ':>3}{'PG':>4}{'PE':>4}{'PD':>4}"
          f"{'GF':>4}{'GC':>4}{'DG':>5}{'PT':>4}")
    for eq, st in sorted(tabla.items(), key=lambda x: x[1]["pt"], reverse=True):
        print(f"{eq:<15}{st['pj']:>3}{st['pg']:>4}{st['pe']:>4}"
              f"{st['pd']:>4}{st['gf']:>4}{st['gc']:>4}"
              f"{st['dg']:>5}{st['pt']:>4}")

    input("\nPresiona Enter para continuar...")
    clear_console()

def registrar_plantel():
    clear_console()
    if not equipos:
        print("No hay equipos registrados.")
        input("\nPresiona Enter para continuar...")
        clear_console()
        return

    print("Equipos disponibles:")
    for i, nom in enumerate(equipos, 1):
        print(f"{i}. {nom}")
    try:
        idx = int(input("Selecciona número del equipo: ")) - 1
        if not (0 <= idx < len(equipos)):
            raise IndexError
    except (ValueError, IndexError):
        print("Selección inválida.")
        input("\nPresiona Enter para continuar...")
        clear_console()
        return

    while True:
        print(f"\nPlantel de {equipos[idx]}:")
        print("1. Registrar jugador")
        print("2. Registrar cuerpo técnico")
        print("3. Volver")
        op = input("Elige una opción: ").strip()
        if op == "1":
            registrar_jugador(idx)
        elif op == "2":
            registrar_tecnico(idx)
        elif op == "3":
            break
        else:
            print("Opción no válida.")
    clear_console()

def menu_principal():
    while True:
        clear_console()
        print("=== Menú Principal ===")
        print("1. Registrar equipo")
        print("2. Registrar plantel")
        print("3. Registrar fecha")
        print("4. Registrar marcador")
        print("5. Equipo con más goles a favor")
        print("6. Equipo con más goles en contra")
        print("7. Tabla de posiciones")
        print("8. Salir")
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            registrar_equipo()
        elif opcion == "2":
            registrar_plantel()
        elif opcion == "3":
            registrar_fecha()
        elif opcion == "4":
            registrar_marcador()
        elif opcion == "5":
            equipo_con_mas_goles_favor()
        elif opcion == "6":
            equipo_con_mas_goles_contra()
        elif opcion == "7":
            mostrar_tabla_posiciones()
        elif opcion == "8":
            clear_console()
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida.")
            input("\nPresiona Enter para continuar...")
            clear_console()

if __name__ == "__main__":
    menu_principal()
