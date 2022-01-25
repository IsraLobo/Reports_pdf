from fpdf import FPDF


def generate_PDF(info_pdf, body_Info):
    try:
        estados = lista_estados(info_pdf['info_Repor']);
        regiones = lista_regiones(info_pdf['info_Repor']);

        class PDF(FPDF):

            def header(self):
                self.image('C:\\Users\\Israel-Perez\\Desktop\\Reports\\Reports\\app\\static\\app\\images\\edilar01.png', 12, 13, 30, 0);
                self.set_text_color(5, 85, 125);
                self.set_font('Arial', 'BU', 10);
                self.cell(w = 0, h = 15, txt = 'EDILAR, S.A. DE C.V.', border = 1, ln = 0, align = 'C', fill = 0);
                self.set_text_color(0, 0, 0);
                self.set_font('Arial', '', 7);
                self.cell(w = 0, h = 5, txt = 'Del Estado: {estado} Al Estado: {estaRv}'.format(**body_Info), border = 0, ln = 0, align = 'R', fill = 0);
                self.cell(w = 0, h = 15, txt = 'De la Fecha: {fechI} A la Fecha: {fechF}'.format(**body_Info), border = 0, ln = 0, align = 'R', fill = 0);
                self.cell(w = 0, h = 25, txt = 'STATUS: {status}'.format(**body_Info), border = 0, ln = 0, align = 'R', fill = 0);
                self.ln(18);

            def footer(self):
                self.set_y(-20);
                self.set_font('Arial', 'B', 7);
                self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 'T', 0, 'R');
        pass


        pdf = PDF();
        pdf.alias_nb_pages();
        pdf.add_page();
        pdf = body_pdf(pdf, estados, regiones, info_pdf['info_Repor']);
        pdf = table_Concntr_Sts(pdf, info_pdf['info_Cntr']);
        pdf = table_status(pdf, info_pdf['lista_status']);
        #pdf.output('myPDF.pdf', 'F');#C:\\Users\\Israel-Perez\\Desktop\\, 'S'
        return pdf;
    except Exception as errpdf:
        return 'Error en PDF: ', errpdf;
pass



def lista_estados(listaEstados):
    try:
        estados = [];
        for e in listaEstados:
            if e['DESCRIPCION_ESTADO'] not in estados:
                estados.append(e['DESCRIPCION_ESTADO']);
        return estados;
    except Exception as errEst:
        return 'Error en PDF: ', errEst;
pass



def lista_regiones(listaRegiones):
    try:
        regiones = [];
        for r in listaRegiones:
            if r['REGION'] not in regiones:
                regiones.append(r['REGION']);
        regiones = sorted(regiones);
        return regiones;
    except Exception as errReg:
        return 'Error en PDF: ', errReg;
pass



def body_pdf(pdf, estados, regiones, infogral):
    try:
        for p in estados:
            estado_unit = list(filter(lambda eu: eu['DESCRIPCION_ESTADO'] == p ,infogral));
            pdf = add_estado(pdf, p, estado_unit, regiones);
        return pdf;
    except Exception as errBody:
        return 'Error en Body PDF: ', errBody;
pass



def table_Concntr_Sts(pdf, concentrado_status):
    try:
        #Tablita Concentrado por status
        pdf.set_font('Arial', 'UB', 9);
        pdf.cell(0, 10, 'Concentrado por Status:', 0, 1);
        #Cabezera Tabla Concentrado Status
        pdf.set_font('Arial', '', 9);
        pdf.set_fill_color(228, 232, 235);
        pdf.cell(20, 4, 'Status', 1, 0, 'C', 1);
        pdf.cell(20, 4, 'Contratos', 1, 1, 'C', 1);
        #Recorrido Concentrado
        contratos = 0;
        for y in concentrado_status:
            pdf.set_font('Arial', '', 9);
            pdf.cell(20, 4, str(y['STATUS']), 1, 0, 'C', 0);
            pdf.cell(20, 4, str(y['CONTRATOS']), 1, 1, 'R', 0);
            contratos = contratos + y['CONTRATOS'];
        pdf.ln(2);
        pdf.cell(20, 4, 'Total: ', 0, 0, 'R', 0);
        pdf.cell(20, 4, str(contratos), 0, 1, 'R', 0);
        pdf.ln(8);
        return pdf;
    except Exception as errTCS:
        return 'Error en PDF: ', errTCSS;
pass



def table_status(pdf, lista_status):
    try:
        #Tablita status
        pdf.set_font('Arial', 'UB', 9);
        pdf.cell(0, 10, 'Status', 0, 1);
        #Cabezera Tabla Status
        pdf.set_font('Arial', '', 9);
        pdf.set_fill_color(228, 232, 235);
        pdf.cell(30, 4, 'Status', 1, 0, 'C', 1);
        pdf.cell(60, 4, 'Descripción', 1, 1, 'C', 1);
        #Recorrido Lista Status
        for z in lista_status:
            pdf.set_font('Arial', '', 8);
            pdf.cell(30, 5, str(z['STATUS_ID']), 1, 0, 'C', 0);
            pdf.cell(60, 5, str(z['DESCRIPCION']), 1, 1, 'L', 0);
        return pdf;
    except Exception as errTS:
        return 'Error en PDF: ', errTS;
pass



def add_estado(pdf, std, estados, regiones):
    try:
        #Estado
        pdf.set_font('Arial', 'U', 9);
        pdf.cell(0, 10, str(std), 0, 1);
        for r in regiones:
            region_unit = list(filter(lambda ru: ru['REGION'] == r ,estados));
            if len(region_unit) != 0:
                pdf = add_region(pdf, r, region_unit);
        return pdf;
    except Exception as errEst:
        return 'Error en PDF: ', errEst;
pass



def add_region(pdf, reg, regiones):
    try:
        #Region
        pdf.set_font('Arial', 'I', 8);
        pdf.cell(0, 10, 'Región: ' + str(reg), 0, 1);
        #Cabezera Tabla Body
        pdf.set_font('Arial', '', 8);
        pdf.set_fill_color(228, 232, 235);
        pdf.cell(25, 6, 'Evento - Vale', 1, 0, 'C', 1);
        pdf.cell(35, 6, 'Asesor', 1, 0, 'C', 1);
        pdf.cell(35, 6, 'Profesor', 1, 0, 'C', 1);
        pdf.cell(14, 6, 'Fecha', 1, 0, 'C', 1);
        pdf.cell(15, 6, 'Cantidad', 1, 0, 'C', 1);
        pdf.cell(55, 6, 'Motivo', 1, 0, 'C', 1);
        pdf.cell(0, 6, 'Status', 1, 1, 'C', 1);
        #Recorrido información
        cantidad = 0;
        for x in regiones:
            #Tabla Información
            pdf.set_font('Arial', '', 7);
            pdf.cell(25, 6, str(x['EVENTO']), 1, 0, 'C', 0);
            pdf = v_cell2(pdf, 35, 6, pdf.get_x(), str(x['NOMBRE_ASESOR']), 'N');
            pdf = v_cell2(pdf, 35, 6, pdf.get_x(), str(x['NOMBRE_PROFESOR']), 'N');
            pdf.cell(14, 6, str(x['FECHA']), 1, 0, 'C', 0);
            pdf.cell(15, 6, str(x['CANTIDAD_DETALLE']), 1, 0, 'C', 0);
            cantidad = cantidad + x['CANTIDAD_DETALLE'];
            pdf = v_cell2(pdf, 55, 6, pdf.get_x(), str(x['MOTIVO']), 'M');
            pdf.cell(0, 6 , str(x['STATUS']), 1, 1, 'C', 0);
        pdf.cell(103, 6, 'Dispositivos: ', 0, 0, 'R', 0);
        pdf.cell(27, 6, str(cantidad), 0, 0, 'C', 0);
        pdf.cell(45, 6, 'Total Contratos: ', 0, 0, 'R', 0);
        pdf.cell(20, 6, str(cantidad), 0, 0, 'C', 0);
        pdf.ln(8);
        return pdf;
    except Exception as errAddR:
        return 'Error en PDF: ', errAddR;
pass



def v_cell2(pdf, width, height, axis, txt, band):
    try:
        n = 29;
        m = 39;

        if band == 'N':
            if len(txt) > n:
                pdf.set_x(axis)
                pdf.set_font('Arial', '', 5);
                pdf.cell(width, height, str(txt), 1, 0, 'L', 0)
                pdf.set_font('Arial', '', 7);
                return pdf;
            else:
                pdf.set_font('Arial', '', 7);
                pdf.cell(width, height, str(txt), 1, 0, 'L', 0);
                return pdf;

        else:
            if len(txt) > m:
                pdf.set_x(axis)
                pdf.set_font('Arial', '', 4);
                pdf.cell(width, height, str(txt)[:63], 1, 0, 'L', 0)
                medi = pdf.get_string_width(txt)
                print(medi)
                pdf.set_font('Arial', '', 7);
                return pdf;

            elif txt == None or txt == 'None':
                pdf.set_font('Arial', '', 7);
                pdf.cell(width, height, '', 1, 0, 'L', 0);
                return pdf;

            else:
                pdf.set_font('Arial', '', 7);
                pdf.cell(width, height, str(txt), 1, 0, 'L', 0);
                return pdf;
    except Exception as errV:
        return 'Error en PDF: ', errV;
pass