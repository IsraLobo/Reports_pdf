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



def cosult_repor_ventas(body_Info):
    try:
        query_inf_vent = ''' select estado_id,
                                   descripcion,
                              (select sum(total_eventos)
                               from cm_control_recepcion
                            where estado = estado_id
                            and venta_del = nvl(TO_DATE('{fechI}','DD/MM/RRRR'), venta_del)
                            and venta_al = nvl(TO_DATE('{fechF}','DD/MM/RRRR'), venta_al)) total_eventos,
                              (select sum(monto)
                               from cm_control_recepcion
                            where estado = estado_id
                            and venta_del = nvl(TO_DATE('{fechI}','DD/MM/RRRR'), venta_del)
                            and venta_al = nvl(TO_DATE('{fechF}','DD/MM/RRRR'), venta_al)) monto_recibido,
                                              (select sum(monto_ventas)
                               from cm_control_recepcion
                            where estado = estado_id
                            and venta_del = nvl(TO_DATE('{fechI}','DD/MM/RRRR'), venta_del)
                            and venta_al = nvl(TO_DATE('{fechF}','DD/MM/RRRR'), venta_al)) monto_ventas,
                                            (select sum(eventos_ventas)
                               from cm_control_recepcion
                            where estado = estado_id
                            and venta_del = nvl(TO_DATE('{fechI}','DD/MM/RRRR'), venta_del)
                            and venta_al = nvl(TO_DATE('{fechF}','DD/MM/RRRR'), venta_al)) eventos_ventas
                            from cm_estado
                            where se_vende = 'S'
                            and estado_id between nvl('{estado}', estado_id) and nvl('{estaRv}', estado_id)
                            order by estado_id '''.format(**body_Info)
        conex = OracleConnection()
        resulVent = conex.exeute_query_descr(query_inf_vent)
        conex.close()
        return resulVent
    except Exception as errVnt:
        return 'No se pudo conectar a la BD [ERROR]: ', errVnt
pass



def complement_vnts(inf_compl):
    try:
        query_complmnt = ''' SELECT region, monto, estado FROM cm_reporte_ventas WHERE venta_del = NVL( TO_DATE('{fechI}','DD/MM/RRRR'), venta_del)
                             AND venta_al = NVL( TO_DATE('{fechF}','DD/MM/RRRR'), venta_al) AND ESTADO = '{estado}' ORDER BY region '''.format(**inf_compl)
        
        conex = OracleConnection()
        resulCompl = conex.exeute_query_descr(query_complmnt)
        conex.close()
        return resulCompl
    except Exception as errCmplV:
        return 'No se pudo conectar a la BD [ERROR]: ', errCmplV
pass



def empresas_Contratos():
    try:
        query_consul_empre = ''' select empresa_id, descripcion from cm_estructura_empresa Union all select 'T' empresa, 'TODAS' nombre  
                                 From Dual order by descripcion '''
        conex = OracleConnection()
        resul_cosul_empre = conex.exeute_query_descr(query_consul_empre)
        conex.close()
        return resul_cosul_empre
    except Exception as errEmpre:
        return 'No se pudo conectar a la BD [ERROR]: ', errEmpre
pass



def consul_ifn_Ctrts(body_Info):
    try:
        query_Prin_Ctrs = ''' SELECT * FROM(select  est.descripcion  estado_n, (select nombre_corto from cm_estructura_empresa where 
                              empresa_id = eve.empresa) empresa, eve.evento_id, con.vale, con.fecha_inicio_cobro, con.cuota, con.afiliado,
                              con.categoria_contrato, eve.fecha, con.status, con.fecha_inv, con.fecha_cl, con.transferido, con.fecha_cobranza,
                              decode(fecha_inv, '', 2,1) inventario, decode(fecha_inv, '', 1,0) No_aplicados_inv, decode(fecha_inv, '', 0,1)
                              aplicados_inv, decode(fecha_cobranza, '', 1,0) No_aplicados_cob, decode(fecha_cobranza, '', 0,1) Aplicados_cob,
                              decode(fecha_cl, '', 1,0) No_Aplicados_cl, decode(fecha_cl, '', 0,1) Aplicados_cl,
                              (select count(*) from cm_contrato_det where  contrato = con.contrato_prin_id) articulos from cm_evento eve,
                              cm_contrato_principal con, cm_status_vta st, cm_estado est where  eve.evento_id = con.evento 
                              and eve.estado = est.estado_id and st.status_id = con.status and st.puesto = con.puesto 
                              and eve.VENTA_TOTAL = eve.CIFRA_CONTROL 
                              and eve.estado between Nvl('{estado}',eve.estado) and Nvl('{estaRv}', eve.estado) and eve.fecha  between Nvl(TO_DATE('{fechI}','DD/MM/RRRR'), eve.fecha) and Nvl(TO_DATE('{fechF}','DD/MM/RRRR'), eve.fecha) and eve.empleado = Nvl('{cvintegradora}', eve.empleado) and eve.evento_id between Nvl('{cvini}', eve.evento_id) and Nvl('{cvfin}', eve.evento_id) and eve.empresa in (decode('{id_empre}', 'T', eve.empresa), '{id_empre}') {filter_1} order by eve.evento_id, con.vale) {filter_2}       
                               '''.format(**body_Info)
        conex = OracleConnection()
        resulInfCtrs = conex.exeute_query_descr(query_Prin_Ctrs)
        conex.close()
        return resulInfCtrs
    except Exception as errInfCtrs:
        return 'No se pudo conectar a la BD [ERROR]: ', errInfCtrs
pass


#C:\app\Israel-Perez\product\11.2.0\client_1

#'DPI-1047: Cannot locate a 32-bit Oracle Client library: 

#"C:\\app\\Israel-Perez\\product\\11.2.0\\client_1\\oci.dll is not the correct architecture". 

#See https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html for help'









#01/JAN/2015
#15/MAR/2021