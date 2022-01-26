from Reports import controllerInfo, dataBase, creacionPDF, createPDFarts
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
import json, io, tempfile
from fpdf import FPDF
from django.views.decorators.csrf import csrf_exempt


#Proyectores
def report_Pro(request):
    try:
        sess = request.GET['sesion_id']; user = request.GET['u'];
        valid_user = dataBase.consult_user(user);
        valid_id = dataBase.consult_id(sess);
        if valid_user == True and valid_id == 1:
            return render(request, 'reporPrincipal.html', {'alert':None});
        else:
            return HttpResponse('<h1>Bad Request (403) Forbidden</h1>')
    except Exception as errorPro:
        return HttpResponse('<h1>Bad Request (403) Forbidden</h1>')
pass


@csrf_exempt
def datos_Proyec(request):
    try:
        body_Pro = json.loads(request.body.decode('utf-8'));
        infogeneral = {};
        infogeneral['estados'] = dataBase.list_Estado();
        infogeneral['estReverse'] = infogeneral['estados'];
        infogeneral['status'] = dataBase.list_status();
        infogeneral['clasif'] = body_Pro['clasif'];
        return HttpResponse(json.dumps(infogeneral));
    except Exception as errorDatPro:
        return HttpResponse(errorDatPro);
pass


@csrf_exempt
def info_Proyec(request):
    try:
        info_pdf = {};
        body_Info = json.loads(request.body.decode('utf-8'));
        body_Info['estado'] = controllerInfo.valid_Dato(body_Info['estado']);
        body_Info['estaRv'] = controllerInfo.valid_Dato(body_Info['estaRv']);
        body_Info['status'] = controllerInfo.valid_Dato(body_Info['status']);
        body_Info['fechI'] = controllerInfo.valid_fecha(body_Info['fechI']);
        body_Info['fechF'] = controllerInfo.valid_fecha(body_Info['fechF']);
        info_pdf['info_Repor'] = dataBase.cosult_Info_Gral_Pro(body_Info);
        info_pdf['info_Cntr'] = dataBase.concentrado_Status(body_Info);
        info_pdf['lista_status'] = dataBase.list_status();
        pdf = creacionPDF.generate_PDF(info_pdf, body_Info);
        pdf.output('myPDF.pdf', 'F');
        response = FileResponse(open('myPDF.pdf', 'rb'), content_type='application/pdf');
        response['Content-Disposition'] = 'attachment; filename="hello.pdf"';
        return response;
    except Exception as errorInfPro:
        return HttpResponse(errorInfPro);
pass



#Articulos
def report_Art(request):
    try:
        sess = request.GET['sesion_id']; user = request.GET['u'];
        valid_user = dataBase.consult_user(user);
        valid_id = dataBase.consult_id(sess);
        if valid_user == True and valid_id == 1:
            return render(request, 'reportPrinArt.html', {'alert':None});
        else:
            return HttpResponse('<h1>Bad Request (403) Forbidden</h1>')
    except Exception as errorPro:
        return HttpResponse('<h1>Bad Request (403) Forbidden</h1>')
pass



@csrf_exempt
def datos_Art(request):
    try:
        selectInfo = {};
        selectInfo['estados'] = dataBase.list_Estado();
        selectInfo['estReverse'] = selectInfo['estados'];
        return HttpResponse(json.dumps(selectInfo));
    except Exception as errorDatPro:
        return HttpResponse(errorDatPro);
pass



@csrf_exempt
def info_Arts(request):
    try:
        info_pdf = {};
        body_Info = json.loads(request.body.decode('utf-8'));
        body_Info['estado'] = controllerInfo.valid_Dato(body_Info['estado']);
        body_Info['estaRv'] = controllerInfo.valid_Dato(body_Info['estaRv']);
        body_Info['fechI'] = controllerInfo.valid_fecha(body_Info['fechI']);
        body_Info['fechF'] = controllerInfo.valid_fecha(body_Info['fechF']);
        info_pdf['inf_Arts'] = dataBase.consult_inf_Art(body_Info);
        pdf = createPDFarts.generate_PDF_arts(info_pdf, body_Info);
        pdf.output('myArtsPDF.pdf', 'F');
        response = FileResponse(open('myArtsPDF.pdf', 'rb'), content_type='application/pdf');
        response['Content-Disposition'] = 'attachment; filename="hello.pdf"';
        return response;
    except Exception as errorInfPro:
        return HttpResponse(errorInfPro);
pass