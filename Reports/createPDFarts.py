from fpdf import FPDF


def generate_PDF_arts(info_pdf, body_Info):
    try:
        estados = lista_estados(info_pdf['inf_Arts']);
        regiones = lista_regiones(info_pdf['inf_Arts']);

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
                self.cell(w = 0, h = 25, txt = 'ARTICULO: {art}'.format(**body_Info), border = 0, ln = 0, align = 'R', fill = 0);
                self.ln(18);

            def footer(self):
                self.set_y(-20);
                self.set_font('Arial', 'B', 7);
                self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 'T', 0, 'R');
        pass


        pdf = PDF();
        pdf.alias_nb_pages();
        pdf.add_page();
        pdf = body_pdf(pdf, estados, regiones, info_pdf['inf_Arts']);
        return pdf;
    except Exception as errpdf:
        return 'Error en PDF: ', errpdf;
pass



def lista_estados(listaEstados):
    try:
        estados = [];
        for e in listaEstados:
            if e['DESCRIPCION'] not in estados:
                estados.append(e['DESCRIPCION']);
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
            estado_unit = list(filter(lambda eu: eu['DESCRIPCION'] == p ,infogral));
            pdf = add_estado(pdf, p, estado_unit, regiones);
        return pdf;
    except Exception as errBody:
        return 'Error en Body PDF: ', errBody;
pass



def add_estado(pdf, std, estados, regiones):
    try:
        #Estado
        pdf.set_font('Arial', 'BU', 9);
        pdf.cell(40, 4, str(std), 0, 0);
        pdf.set_fill_color(172, 172, 172);
        pdf.cell(8, 4, str(''), 1, 0, 'L',1);
        pdf.set_font('Arial', '', 8);
        pdf.cell(35, 4, str('Computadora Factoraje'), 0, 1, 'C');
        suma = 0;
        for r in regiones:
            region_unit = list(filter(lambda ru: ru['REGION'] == r ,estados));
            if len(region_unit) != 0:
                pdf, cantidad = add_region(pdf, r, region_unit);
                suma = suma + cantidad
        pdf.cell(175, 6, 'Total Contratos: ', 0, 0, 'R', 0);
        pdf.cell(20, 6, str(suma), 0, 1, 'C', 0);
        pdf.ln(5);
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
        pdf.cell(38, 6, 'Asesor', 1, 0, 'C', 1);
        pdf.cell(38, 6, 'Profesor', 1, 0, 'C', 1);
        pdf.cell(14, 6, 'Fecha', 1, 0, 'C', 1);
        pdf.cell(66, 6, 'Motivo', 1, 0, 'C', 1);
        pdf.cell(0, 6, 'Status', 1, 1, 'C', 1);
        #Recorrido información
        cantidad = 0;
        for x in regiones:
            #Tabla Información
            pdf.set_font('Arial', '', 7);
            pdf.cell(25, 6, str(x['EVENTO']), 1, 0, 'C', 0);
            pdf = v_cell2(pdf, 38, 6, pdf.get_x(), str(x['NOMBRE_ASESOR']), 'N');
            #pdf.cell(38, 6, str(x['NOMBRE_ASESOR']), 1, 0, 'L', 0)
            pdf = v_cell2(pdf, 38, 6, pdf.get_x(), str(x['NOMBRE_PROFESOR']), 'N');
            #pdf.cell(38, 6, str(x['NOMBRE_PROFESOR']), 1, 0, 'L', 0)
            pdf.cell(14, 6, str(x['FECHA']), 1, 0, 'C', 0);
            cantidad += 1;
            pdf = v_cell2(pdf, 66, 6, pdf.get_x(), str(x['COMENTARIOS_REP']), 'M');
            pdf.cell(0, 6 , str(x['STATUS']), 1, 1, 'C', 0);
        #pdf.cell(175, 6, 'Total Contratos: ', 0, 0, 'R', 0);
        #pdf.cell(20, 6, str(cantidad), 0, 0, 'C', 0);
        pdf.ln(2);
        return pdf, cantidad;
    except Exception as errAddR:
        return 'Error en PDF: ', errAddR;
pass



def v_cell2(pdf, width, height, axis, txt, band):
    try:
        n = 30;
        m = 39;

        if band == 'N':
            if len(txt) >= n:
                if len(txt) >= 39:
                    pdf.set_x(axis)
                    pdf.set_font('Arial', '', 5);
                    pdf.cell(width, height, str(txt), 1, 0, 'L', 0)
                    pdf.set_font('Arial', '', 7);
                    return pdf;
                else:
                    pdf.set_x(axis)
                    pdf.set_font('Arial', '', 5.5);
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