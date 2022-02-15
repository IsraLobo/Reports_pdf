from fpdf import FPDF
import locale



def generate_PDF_procesos(body_Info, info_pdf):
    try:
        inf_compl = {}
        inf_compl['fechI'] = body_Info['fechI']
        inf_compl['fechF'] = body_Info['fechF']
        estados = lista_estados(info_pdf['inf_Procs'])


        class PDF(FPDF):

            def header(self):
                self.image('C:\\Users\\Israel-Perez\\Desktop\\Reports\\Reports\\app\\static\\app\\images\\edilar01.png', 12, 13, 30, 0)
                self.set_text_color(5, 85, 125)
                self.set_font('Arial', 'BU', 10)
                self.cell(w = 0, h = 15, txt = 'EDILAR, S.A. DE C.V.', border = 1, ln = 0, align = 'C', fill = 0)
                self.set_text_color(0, 0, 0)
                self.set_font('Arial', '', 8)
                self.cell(w = 0, h = 5, txt = 'Del Estado: {estado} Al Estado: {estaRv}'.format(**body_Info), border = 0, ln = 0, align = 'R', fill = 0)
                self.cell(w = 0, h = 15, txt = 'De la Fecha: {fechI} A la Fecha: {fechF}'.format(**body_Info), border = 0, ln = 0, align = 'R', fill = 0)
                self.cell(w = 0, h = 25, txt = 'Del evento: {cvini} Al Evento: {cvfin}'.format(**body_Info), border = 0, ln = 0, align = 'R', fill = 0)
                self.ln(18)

                self.set_font('Arial', 'BU', 10)
                self.cell(w = 0, h = 6, txt = '{empresa}'.format(**body_Info), border = 0, ln = 1, align = 'L', fill = 0)
                self.ln(1)
                
                self.set_font('Arial', 'B', 8)
                self.set_fill_color(228, 232, 235)
                self.cell(30, 6, 'Evento', 1, 0, 'C', 1)
                self.cell(15, 6, 'Fecha', 1, 0, 'C', 1)
                self.cell(8, 6, 'Cto.', 1, 0, 'C', 1)
                self.cell(10, 6, 'Status', 1, 0, 'C', 1)
                self.cell(15, 6, 'Inicio Cob', 1, 0, 'C', 1)
                self.cell(15, 6, 'Cuota', 1, 0, 'C', 1)
                self.cell(8, 6, 'Cat.', 1, 0, 'C', 1)
                self.cell(10, 6, 'Trans.', 1, 0, 'C', 1)
                self.cell(30, 6, 'Afiliado', 1, 0, 'C', 1)
                self.cell(17, 6, 'Fecha Inv.', 1, 0, 'C', 1)
                self.cell(17, 6, 'Fecha Cob.', 1, 0, 'C', 1)
                self.cell(0, 6, 'Fecha CI', 1, 1, 'C', 1)
                self.ln(2)


            def footer(self):
                self.set_y(-20)
                self.set_font('Arial', '', 8)
                self.cell(50, 5, 'CONTRATOS: {contrato}'.format(**body_Info), 0, 0, 'C', 0)
                self.cell(50, 5, 'INVENTARIO: {inventario}'.format(**body_Info), 0, 0, 'L', 0)
                self.cell(40, 5, 'COBRANZA: {cobranza}'.format(**body_Info), 0, 0, 'C', 0)
                self.cell(0, 5, 'CLUB LECTORES: {club}'.format(**body_Info), 0, 1, 'C', 0)
                self.set_font('Arial', 'B', 7)
                self.cell(0, 5, 'Página ' + str(self.page_no()) + '/{nb}', 'T', 0, 'R')
        pass

        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf = body_pdf(pdf, info_pdf['inf_Procs'], estados)
        return pdf
    except Exception as errpdf:
        return 'Error en PDF: ', errpdf
pass



def lista_estados(listaEstados):
    try:
        estados = [];
        for e in listaEstados:
            if e['ESTADO_N'] not in estados:
                estados.append(e['ESTADO_N']);
        return estados;
    except Exception as errEst:
        return 'Error en PDF: ', errEst;
pass



def body_pdf(pdf, info_body, estados):
    try:
        max_contratos = 0; max_inv = 0; max_cob = 0; max_cl = 0; max_NOinv = 0; max_NOcob = 0; max_NOcl = 0
        for p in estados:
            estado_unit = list(filter(lambda eu: eu['ESTADO_N'] == p , info_body))
            pdf, totales = write_pdf(pdf, p, estado_unit)
            max_contratos = totales['n_contratos'] + max_contratos
            max_inv = totales['tot_inv'] + max_inv
            max_cob = totales['tot_cob'] + max_cob
            max_cl = totales['tot_cl'] + max_cl
            max_NOinv = totales['tot_NOinv'] + max_NOinv
            max_NOcob = totales['tot_NOcob'] + max_NOcob
            max_NOcl = totales['tot_NOcl'] + max_NOcl

        pdf.ln(5)
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(101, 6, 'Total Contratos:', 0, 0, 'R', 0)
        pdf.cell(10, 6, str(max_contratos), 0, 0, 'C', 0)
        pdf.cell(30, 6, 'Total Aplicados:', 0, 0, 'R', 0)
        pdf.cell(17, 6, str(max_inv), 0, 0, 'C', 0)
        pdf.cell(17, 6, str(max_cob), 0, 0, 'C', 0)
        pdf.cell(0, 6, str(max_cl), 0, 1, 'C', 0)
        pdf.cell(141, 6, 'Total No Aplicados:', 0, 0, 'R', 0)
        pdf.cell(17, 6, str(max_NOinv), 0, 0, 'C', 0)
        pdf.cell(17, 6, str(max_NOcob), 0, 0, 'C', 0)
        pdf.cell(0, 6, str(max_NOcl), 0, 0, 'C', 0)
        return pdf;
    except Exception as errBody:
        return 'Error en Body PDF: ', errBody;
pass



def write_pdf(pdf, estd, estado_unit):
    try:
        totales = {}
        #Estado
        pdf.set_font('Arial', 'B', 9)
        pdf.cell(0, 6, str(estd), 0, 1)
        #Tabla Información
        n_contratos = 0
        n_inv = 0
        n_cob = 0
        n_cl = 0
        n_NOinv = 0
        n_NOcob = 0
        n_NOcl = 0
        for x in estado_unit:
            pdf.set_font('Arial', '', 8)
            pdf.cell(30, 6, str(x['EVENTO_ID']), 1, 0, 'L', 0)
            pdf.cell(15, 6, coneversorDate(x['FECHA']) if x['FECHA'] else "", 1, 0, 'C', 0)
            pdf.cell(8, 6, str(x['VALE']) if x['VALE'] else "", 1, 0, 'C', 0)
            pdf.cell(10, 6, str(x['STATUS']), 1, 0, 'C', 0)
            pdf.cell(15, 6, coneversorDate(x['FECHA_INICIO_COBRO']) if x['FECHA_INICIO_COBRO'] else "", 1, 0, 'C', 0)
            pdf.cell(15, 6, conever_to_number(x['CUOTA']) if x['CUOTA'] else "$0.00", 1, 0, 'C', 0)
            pdf.cell(8, 6, str(x['CATEGORIA_CONTRATO']) if x['CATEGORIA_CONTRATO'] else "", 1, 0, 'C', 0)
            pdf.cell(10, 6, str(x['TRANSFERIDO']) if x['TRANSFERIDO'] else "", 1, 0, 'C', 0)
            pdf.cell(30, 6, str(x['AFILIADO']), 1, 0, 'L', 0)
            pdf.cell(17, 6, coneversorDate(x['FECHA_INV']) if x['FECHA_INV'] else "", 1, 0, 'C', 0)
            pdf.cell(17, 6, coneversorDate(x['FECHA_COBRANZA']) if x['FECHA_COBRANZA'] else "", 1, 0, 'C', 0)
            pdf.cell(0, 6, coneversorDate(x['FECHA_CL']) if x['FECHA_CL'] else "", 1, 1, 'C', 0)
            n_inv += x['APLICADOS_INV']
            n_cob += x['APLICADOS_COB']
            n_cl += x['APLICADOS_CL']
            n_NOinv += x['NO_APLICADOS_INV']
            n_NOcob += x['NO_APLICADOS_COB']
            n_NOcl += x['NO_APLICADOS_CL']
            n_contratos += 1
        pdf.set_font('Arial', 'B', 8)
        pdf.cell(101, 6, 'No Contratos:', 0, 0, 'R', 0)
        pdf.cell(10, 6, str(n_contratos), 0, 0, 'C', 0)
        pdf.cell(30, 6, 'Aplicados:', 0, 0, 'R', 0)
        pdf.cell(17, 6, str(n_inv), 0, 0, 'C', 0)
        pdf.cell(17, 6, str(n_cob), 0, 0, 'C', 0)
        pdf.cell(0, 6, str(n_cl), 0, 1, 'C', 0)
        pdf.cell(141, 6, 'No Aplicados:', 0, 0, 'R', 0)
        pdf.cell(17, 6, str(n_NOinv), 0, 0, 'C', 0)
        pdf.cell(17, 6, str(n_NOcob), 0, 0, 'C', 0)
        pdf.cell(0, 6, str(n_NOcl), 0, 0, 'C', 0)
        pdf.ln(5)
        totales['n_contratos'] = n_contratos
        totales['tot_inv'] = n_inv
        totales['tot_cob'] = n_cob
        totales['tot_cl'] = n_cl
        totales['tot_NOinv'] = n_NOinv
        totales['tot_NOcob'] = n_NOcob
        totales['tot_NOcl'] = n_NOcl
        return pdf, totales
    except Exception as errEst:
        return 'Error en PDF: ', errEst;
pass



def coneversorDate(fech):
    a = fech.strftime('%d/%m/%Y')
    return str(a)



def conever_to_number(valor):
    try:
        locale.setlocale(locale.LC_ALL, '')
        monto = locale.currency(valor, grouping=True)
        return str(monto)
    except Exception as errConver:
        return 'Error en la converción: ', errConver
pass