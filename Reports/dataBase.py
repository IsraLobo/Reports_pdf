from Reports import controllerInfo
import cx_Oracle, json


class OracleConnection():
    connection = None;
    databaseConn = None;
    cursor = None;

    def __init__(self):
        try:
            self.connection = 'CL/C1594EDI@192.168.82.181:1521/EDI83';
            self.databaseConn = cx_Oracle.connect(self.connection);
            self.cursor = self.databaseConn.cursor();
        except Exception as errorDB:
            return 'Error en la BD: ', errorDB;

    def execute_query(self, query):
        self.cursor.execute(query);
        return self.cursor.fetchall();

    def exeute_query_descr(self, query):
        curs = self.cursor.execute(query);
        colums = [column[0] for column in curs.description];
        resl = [dict(zip(colums, row)) for row in curs.fetchall()];
        return resl;

    def execute_Trans(self, query):
        self.cursor.execute(query);
        return self.cursor;

    def commit(self):
        self.databaseConn.commit();

    def close(self):
        self.databaseConn.close();




def consult_user(user):
    try:
        query_user = '''SELECT usuario_id"usuario", e_mail"email", nombre"nombre" FROM cl_sys_usuario WHERE upper(usuario_id)=upper('{}')'''.format(user);
        conex = OracleConnection();
        resul_user = conex.exeute_query_descr(query_user);
        conex.close();
        if len(resul_user) != 0:
            return True
        else:
            return False
    except Exception as errUser:
        return 'No se pudo conectar a la BD [ERROR]: ', errUser;
pass



def consult_id(id):
    try:
        query_id = ''' SELECT count(*) no FROM v$session WHERE sid||audsid = {} '''.format(id);
        conex = OracleConnection();
        resul_id = conex.execute_query(query_id);
        conex.close();
        return resul_id[0][0];
    except Exception as errId:
        return 'No se pudo conectar a la BD [ERROR]: ', errId;
pass



def cosult_Info_Gral_Pro(body_Info):
    try:
        query_Pro = '''  SELECT DESCRIPCION_ESTADO, REGION, EVENTO, NOMBRE_ASESOR, NOMBRE_PROFESOR, TO_CHAR(FECHA, 'DD/MM/RRRR') FECHA,
                        (SELECT COUNT(ARTICULO) FROM CM_CONTRATO_DET D, AL_ARTICULOS A, AL_CLASIFICACION C
                          WHERE CONTRATO = V.CONTRATO_PRIN_ID AND A.CLASIFICACION = C.CVE_CLASIFICACION
                            AND C.CVE_CLASIFICACION = '{clasif}' AND D.ARTICULO = A.CVE_ARTICULO) CANTIDAD_DETALLE,
                        (SELECT COMENTARIO FROM CL_COMENTARIOS_ASESORES WHERE CONTRATO_PRIN = V.CONTRATO_PRIN_ID
                            AND FECHA_CAPTURA = (SELECT MAX(FECHA_CAPTURA) FROM CL_COMENTARIOS_ASESORES 
                          WHERE CONTRATO_PRIN = V.CONTRATO_PRIN_ID)) MOTIVO, STATUS FROM V_RP_CONTRATOS_PROYECTOR V
                          WHERE ESTADO BETWEEN '{estado}' AND '{estaRv}' AND FECHA BETWEEN TO_DATE('{fechI}','DD/MM/RRRR') 
                            AND TO_DATE('{fechF}','DD/MM/RRRR') AND CLASIFICACION = '{clasif}'
                            AND STATUS = CASE WHEN '{status}' = 'TODOS' THEN STATUS ELSE '{status}' END '''.format(**body_Info);

        conex = OracleConnection();
        resulPro = conex.exeute_query_descr(query_Pro);
        conex.close();
        return resulPro;
    except Exception as errPro:
        return 'No se pudo conectar a la BD [ERROR]: ', errPro;
pass



def concentrado_Status(body_Info):
    try:
        query_Cntr_sts = ''' SELECT STATUS, COUNT (DISTINCT CONTRATO_PRIN_ID) CONTRATOS FROM V_RP_CONTRATOS_PROYECTOR 
                              WHERE CLASIFICACION = '{clasif}' AND ESTADO BETWEEN '{estado}' AND '{estaRv}' 
                                AND FECHA BETWEEN NVL (TO_DATE('{fechI}', 'DD-MM-RRRR'), FECHA) 
                                AND NVL (TO_DATE('{fechF}', 'DD-MM-RRRR'), FECHA)
                                AND STATUS = CASE WHEN '{status}' = 'TODOS' THEN STATUS ELSE '{status}' END
                              GROUP BY STATUS ORDER BY STATUS '''.format(**body_Info);

        conex = OracleConnection();
        resulCntr = conex.exeute_query_descr(query_Cntr_sts);
        conex.close();
        return resulCntr;
    except Exception as errCntrSts:
        return 'No se pudo conectar a la BD [ERROR]: ', errCntrSts;
pass



def list_Clasif():
    try:
        query_clsf = ''' SELECT CVE_CLASIFICACION, DESCRIPCION FROM AL_CLASIFICACION WHERE CVE_CLASIFICACION IN ('PRO','TEL') ''';
        conex = OracleConnection();
        resulClasf = conex.exeute_query_descr(query_clsf);
        conex.close();
        return resulClasf;
    except Exception as errClsf:
        return 'No se pudo conectar a la BD [ERROR]: ', errClsf;
pass



def list_Estado():
    try:
        query_Estd = ''' SELECT ESTADO_ID, DESCRIPCION FROM CM_ESTADO ORDER BY ESTADO_ID ''';
        conex = OracleConnection();
        resultEstad = conex.exeute_query_descr(query_Estd);
        conex.close();
        return resultEstad;
    except Exception as errEst:
        return 'No se pudo conectar a la BD [ERROR]: ', errEst;
pass



def list_status():
    try:
        query_Sts = ''' SELECT STATUS_ID, DESCRIPCION FROM CM_STATUS_VTA WHERE TIPO_VENTA = 'PNBM' 
                        AND STATUS_ID IN ('PDTC','CTOC','PDTS','CTOS','VACC','VACS','CFCC','CFCS') ''';
        conex = OracleConnection();
        resulStatus = conex.exeute_query_descr(query_Sts);
        conex.close();
        return resulStatus;
    except Exception as errSts:
        return 'No se pudo conectar a la BD [ERROR]: ', errSts;
pass



def consult_inf_Art(body_Info):
    try:
        query_info_arts = ''' SELECT DISTINCT EVE.ESTADO, CE.DESCRIPCION, CON.EVENTO || ' - ' || CON.VALE EVENTO,
                             (SELECT INITCAP (PATERNO || ' ' || MATERNO || ' ' || NOMBRE) FROM CM_EMPLEADO WHERE EMPLEADO_ID = EVE.EMPLEADO)
                                     NOMBRE_ASESOR, (SELECT INITCAP (PATERNO || ' ' || MATERNO || ' ' || NOMBRE) FROM CM_AFILIADO
                               WHERE AFILIADO_ID = CON.AFILIADO) NOMBRE_PROFESOR, CON.STATUS, TO_CHAR(EVE.FECHA, 'DD/MM/RRRR') FECHA, CON.COMENTARIOS_REP,
                                     EVE.REGION_ESC REGION FROM CM_CONTRATO_PRINCIPAL CON, CM_STATUS_VTA ST, CM_EVENTO EVE, CM_CONTRATO_DET DET,
                                     CM_ESTADO CE WHERE CON.EVENTO = EVE.EVENTO_ID AND CON.STATUS = ST.STATUS_ID AND CON.CONTRATO_PRIN_ID = DET.CONTRATO 
                                 AND ST.VTA_APLICADA = 'S' AND EVE.ESTADO BETWEEN '{estado}' AND '{estaRv}'
                                 AND EVE.FECHA BETWEEN NVL (TO_DATE('{fechI}','DD/MM/RRRR'), EVE.FECHA) AND NVL (TO_DATE('{fechF}','DD/MM/RRRR'), EVE.FECHA)
                                 AND CON.TIPO_VENTA = 'PNBM' AND DET.ARTICULO = '{art}' AND CE.ESTADO_ID = EVE.ESTADO
                            ORDER BY EVE.ESTADO, EVENTO '''.format(**body_Info);
        conex = OracleConnection();
        resulArts = conex.exeute_query_descr(query_info_arts);
        conex.close();
        return resulArts
    except Exception as errInfoArt:
        return 'No se pudo conectar a la BD [ERROR]: ', errInfoArt;
pass






#C:\app\Israel-Perez\product\11.2.0\client_1

#'DPI-1047: Cannot locate a 32-bit Oracle Client library: 

#"C:\\app\\Israel-Perez\\product\\11.2.0\\client_1\\oci.dll is not the correct architecture". 

#See https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html for help'