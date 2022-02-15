from Reports import dataBase


def valid_Dato(dato):
    lista_dato = dato.split('-');
    return lista_dato[0].strip();


def valid_fecha(fech):
    anio, mes, dia = fech[1-1:4], fech[6-1:7], fech[9-1:10];
    return '{}/{}/{}'.format(dia, mes, anio);


def valid_Empresa(body_Info):
    empresa = body_Info['empresa']
    lista_empre = empresa.split('-')
    body_Info['id_empre'] = lista_empre[0].strip()
    body_Info['empresa'] = lista_empre[1].strip()
    return body_Info



def add_filter(contatros, inventario, cobranza, club):
    filter_1 = ''
    filter_2 = ''

    if contatros == 'APLICAN':
        if inventario == 'APLICADOS':
            filter_1 =  ''' and FECHA_INV IS NOT NULL AND ST.INVENTARIO = 'S' '''
        elif inventario == 'NO APLICADOS':
            filter_1 = ''' and FECHA_INV IS NULL AND ST.INVENTARIO = 'S' '''
            filter_2 = ' WHERE ARTICULOS > 0 '
        elif inventario == 'TODOS':
            filter_1 = ''' AND ST.INVENTARIO = 'S' '''
        elif inventario == 'NO APLICA':
            filter_1 = ''' NULL '''

        if cobranza == 'APLICADOS':
            filter_1 = filter_1 + ''' and FECHA_COBRANZA IS NOT NULL AND ST.COBRANZA = 'S' '''
        elif cobranza == 'NO APLICADOS':
            filter_1 = filter_1 + ''' and FECHA_COBRANZA IS NULL AND ST.COBRANZA = 'S' '''
        elif cobranza == 'TODOS':
            filter_1 = filter_1 + ''' AND ST.COBRANZA = 'S' '''
        elif cobranza == 'NO APLICA':
            filter_1 = filter_1

        if club == 'APLICADOS':
            filter_1 = filter_1 + ''' and FECHA_CL IS NOT NULL AND CON.TIENE_CL ='S' AND ST.COBRANZA = 'S' '''
        elif club == 'NO APLICADOS':
            filter_1 = filter_1 + ''' and FECHA_CL IS NULL AND CON.TIENE_CL = 'S' AND ST.COBRANZA = 'S' '''
        elif club == 'TODOS':
            filter_1 = filter_1 + ''' AND CON.TIENE_CL = 'S' AND ST.COBRANZA = 'S' '''
        elif club == 'NO APLICA':
            filter_1 = filter_1

    else:
        if inventario == 'APLICADOS':
            filter_1 = ''' and FECHA_INV IS NOT NULL '''
        elif inventario == 'NO APLICADOS':
            filter_1 = ''' and FECHA_INV IS NULL '''
            filter_2 = ' WHERE ARTICULOS > 0 '
        elif inventario == 'TODOS':
            filter_1 = ''' and (FECHA_INV IS NOT NULL OR FECHA_INV IS NULL) '''
            filter_2 = ''' WHERE ARTICULOS > 0 '''
        elif inventario == 'NO APLICA':
            filter_1 = " NULL "

        if cobranza == 'APLICADOS':
            filter_1 = filter_1 + ''' AND FECHA_COBRANZA IS NOT NULL '''
        elif cobranza == 'NO APLICADOS':
            filter_1 = filter_1 + ''' AND FECHA_COBRANZA IS NULL '''
        elif cobranza == 'TODOS':
            filter_1 = filter_1 + ''' AND (FECHA_COBRANZA IS NOT NULL OR FECHA_COBRANZA IS NULL) '''
        elif cobranza == 'NO APLICA':
            filter_1 = filter_1

        if club == 'APLICADOS':
            filter_1 = filter_1 + ''' AND FECHA_CL IS NOT NULL AND CON.TIENE_CL = 'S' '''
        elif club == 'NO APLICADOS':
            filter_1 = filter_1 + ''' and FECHA_CL IS NULL AND CON.TIENE_CL ='S' '''
        elif club == 'TODOS':
            filter_1 = filter_1 + ''' AND CON.TIENE_CL ='S' '''
        elif club == 'NO APLICA':
            filter_1 = filter_1
    
        
    return filter_1, filter_2