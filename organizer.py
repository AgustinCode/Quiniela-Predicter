import csv
from datetime import datetime

def procesar_archivo(nombre_archivo_entrada, nombre_archivo_salida):
    dias_es_en = {
        'Lun': 'Mon', 'Mar': 'Tue', 'Mie': 'Wed', 'Jue': 'Thu',
        'Vie': 'Fri', 'Sab': 'Sat', 'Dom': 'Sun'
    }

    with open(nombre_archivo_entrada, 'r', encoding='utf-8') as archivo_entrada, \
         open(nombre_archivo_salida, 'w', newline='', encoding='utf-8') as archivo_salida:
        
        lector_csv = csv.reader(archivo_entrada)
        escritor_csv = csv.writer(archivo_salida)
        
        escritor_csv.writerow(['Fecha', 'Turno', 'Posicion', 'Numero'])
        
        next(lector_csv, None)
        
        lineas_procesadas = 0
        lineas_con_error = 0
        
        for num_linea, fila in enumerate(lector_csv, start=2):  # start=2 porque ya saltamos la cabecera
            try:
                fecha_completa, numero_completo = fila
                
                fecha, turno = fecha_completa.rsplit(' - ', 1)
                
                dia_es, resto_fecha = fecha.split(' ', 1)
                dia_en = dias_es_en.get(dia_es, dia_es)
                fecha_en = f"{dia_en} {resto_fecha}"
                
                fecha_obj = datetime.strptime(fecha_en, '%a %d/%m/%Y')
                fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
                
                posicion, numero = numero_completo.split('.')
                
                escritor_csv.writerow([fecha_formateada, turno, posicion, numero])
                lineas_procesadas += 1
            except Exception as e:
                print(f"Error en la línea {num_linea}: {e}")
                print(f"Contenido de la línea: {fila}")
                lineas_con_error += 1

    print(f"Total de líneas procesadas: {lineas_procesadas}")
    print(f"Total de líneas con error: {lineas_con_error}")

# Uso de la función
procesar_archivo('data.csv', 'results.csv')