from Reports import dataBase


def valid_Dato(dato):
    lista_dato = dato.split('-');
    return lista_dato[0].strip();


def valid_fecha(fech):
    anio, mes, dia = fech[1-1:4], fech[6-1:7], fech[9-1:10];
    return '{}/{}/{}'.format(dia, mes, anio);