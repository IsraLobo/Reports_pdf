from Reports import dataBase
from fpdf import FPDF
import locale


def generate_PDF_ventas(info_pdf, body_Info):
    try:
        inf_compl = {}
        inf_compl['fechI'] = body_Info['fechI']
        inf_compl['fechF'] = body_Info['fechF']


        class PDF(FPDF):

            def header(self):
                self.image('C:\\Users\\Israel-Perez\\Desktop\\Reports\\Reports\\app\\static\\app\\images\\edilar01.png', 12, 13, 30, 0);
                self.set_text_color(5, 85, 125);
                self.set_font('Arial', 'BU', 10);
                self.cell(w = 0, h = 15, txt = 'EDILAR, S.A. DE C.V.', border = 1, ln = 0, align = 'C', fill = 0);
                self.set_text_color(0, 0, 0);
                self.set_font('Arial', '', 8);
                self.cell(w = 0, h = 5, txt = 'Del Estado: {estado} Al Estado: {estaRv}'.format(**body_Info), border = 0, ln = 0, align = 'R', fill = 0);
                self.cell(w = 0, h = 15, txt = 'De la Fecha: {fechI} A la Fecha: {fechF}'.format(**body_Info), border = 0, ln = 1, align = 'R', fill = 0);
                self.ln(5);
                
                self.set_font('Arial', 'B', 9);
                self.set_fill_color(228, 232, 235);
                self.cell(55, 6, 'Ventas', 1, 0, 'C', 1);
                self.cell(45, 6, 'Reportadas', 1, 0, 'C', 1);
                self.cell(45, 6, 'Recibidas', 1, 0, 'C', 1);
                self.cell(0, 6, 'Cedis', 1, 1, 'C', 1);

                self.cell(55, 6, 'Estado', 1, 0, 'C', 1);
                self.cell(15, 6, 'Región', 1, 0, 'C', 1);
                self.cell(30, 6, 'Monto', 1, 0, 'C', 1);
                self.cell(15, 6, 'Eventos', 1, 0, 'C', 1);
                self.cell(30, 6, 'Monto', 1, 0, 'C', 1);
                self.cell(15, 6, 'Eventos', 1, 0, 'C', 1);
                self.cell(0, 6, 'Monto', 1, 1, 'C', 1);


            def footer(self):
                self.set_y(-20)
                self.set_font('Arial', 'B', 7)
                self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 'T', 0, 'R')
        pass

        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf = body_pdf(pdf, info_pdf['inf_Vnts'], inf_compl)
        return pdf
    except Exception as errpdf:
        return 'Error en PDF: ', errpdf
pass



def body_pdf(pdf, infogral, inf_compl):
    try:
        total_event_1 = 0
        total_event_2 = 0
        monto = 0
        monto_gral = 0
        monto_gral_1 = 0
        monto_gral_2 = 0
        for i in infogral:
            inf_compl['estado'] = i['ESTADO_ID']
            complements = dataBase.complement_vnts(inf_compl)
            pdf.set_font('Arial', 'B', 9)
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(55, 6, str(i['DESCRIPCION']), 'TBL', 0, 'L', 1)
            pdf.set_font('Arial', '', 9)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(15, 6, '', 'TB', 0, 'L', 1)
            if len(complements) != 0:
                for u in complements:
                    monto = monto + u['MONTO']
                monto_gral = monto_gral + monto
                pdf.cell(30, 6, conever_to_number(monto), 'TBR', 0, 'R', 1)
                monto = 0
            else:
                pdf.cell(30, 6, '$0.00', 'TBR', 0, 'R', 1)

            ############################################################################################
            pdf.cell(15, 6, str(i['EVENTOS_VENTAS']) if i['EVENTOS_VENTAS'] else "", 1, 0, 'C', 1)
            pdf.cell(30, 6, conever_to_number(i['MONTO_VENTAS']) if i['MONTO_VENTAS'] else "$0.00", 1, 0, 'R', 1)
            if i['MONTO_VENTAS']:
                monto_gral_1 = monto_gral_1 + i['MONTO_VENTAS']
            if i['EVENTOS_VENTAS']:
                total_event_1 = total_event_1 + i['EVENTOS_VENTAS']
            
            
            ############################################################################################
            pdf.cell(15, 6, str(i['TOTAL_EVENTOS']) if i['TOTAL_EVENTOS'] else "", 1, 0, 'C', 1)
            pdf.cell(30, 6, conever_to_number(i['MONTO_RECIBIDO']) if i['MONTO_RECIBIDO'] else "$0.00", 1, 1, 'R', 1)
            if i['MONTO_RECIBIDO']:
                monto_gral_2 = monto_gral_2 + i['MONTO_RECIBIDO']
            if i['TOTAL_EVENTOS']:
                total_event_2 = total_event_2 + i['TOTAL_EVENTOS']


            if len(complements) != 0:
                for n in complements:
                    pdf.cell(55, 6, '', 'LR', 0, 'C', 0)
                    pdf.cell(15, 6, str(n['REGION']), 1, 0, 'C', 0)
                    pdf.cell(30, 6, conever_to_number(n['MONTO']), 1, 0, 'R', 0)
                    pdf.cell(0, 6, '', 'LR', 1, 'C', 0)

        pdf.set_font('Arial', 'B', 10)
        pdf.ln(3)
        pdf.cell(70, 6, 'Totales:', 0, 0, 'R', 0)
        pdf.set_font('Arial', '', 9)
        pdf.cell(30, 6, conever_to_number(monto_gral), 0, 0, 'R', 0)
        pdf.cell(15, 6, str(total_event_1), 0, 0, 'C', 0)
        pdf.cell(30, 6, conever_to_number(monto_gral_1), 0, 0, 'R', 0)
        pdf.cell(15, 6, str(total_event_2), 0, 0, 'C', 0)
        pdf.cell(30, 6, conever_to_number(monto_gral_2), 0, 0, 'R', 0)
        return pdf
    except Exception as errBody:
        return 'Error en Body PDF: ', errBody
pass



def conever_to_number(valor):
    try:
        locale.setlocale(locale.LC_ALL, '')
        monto = locale.currency(valor, grouping=True)
        return str(monto)
    except Exception as errConver:
        return 'Error en la converción: ', errConver
pass