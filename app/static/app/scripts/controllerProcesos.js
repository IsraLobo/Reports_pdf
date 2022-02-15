var app = angular.module("MyControllerAngCntrts", []);
var rutaInfoPrcs = '/report_procesos/';
var rutadatosPrcs = '/datos_procesos/';
var rutainfoPrcs = '/info_procesos/';


app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


app.controller("ControllerHTTPCntrts", function ($scope, $http) {


    //Procesos
    $scope.ReporProcesos = function () {

        $http.get(rutadatosPrcs)
            .then(function (rspForm) {
                $scope.listaEstado = rspForm.data.estados;
                $scope.listaEstadoRevers = rspForm.data.estReverse;
                $scope.listaEmpresas = rspForm.data.empresas;
                $scope.rpPrcs = true;
            }, function (err) {
                console.log(err);
            });
    };
    //Fin Procesos



    //Generar PDF Procecsos
    $scope.generarPDF = function () {

        if ($scope.datosReport.claveIntr == null || $scope.datosReport.claveIntr == undefined || $scope.datosReport.claveIntr == "null" || $scope.datosReport.claveIntr == "undefined") { $scope.datosReport.claveIntr = "" }

        if ($scope.datosReport.eveIni == null || $scope.datosReport.eveIni == undefined || $scope.datosReport.eveIni == "null" || $scope.datosReport.eveIni == "undefined") { $scope.datosReport.eveIni = "" }

        if ($scope.datosReport.eveFin == null || $scope.datosReport.eveFin == undefined || $scope.datosReport.eveFin == "null" || $scope.datosReport.eveFin == "undefined") { $scope.datosReport.eveFin = "" }


        var requestData = {
            'empresa': $scope.datosReport.selecEmpresas,
            'estado': $scope.datosReport.selecEstado,
            'estaRv': $scope.datosReport.selecEstadoRever,
            'contrato': $scope.datosReport.selecContratos,
            'inventario': $scope.datosReport.selecInvent,
            'cobranza': $scope.datosReport.selecCobranza,
            'club': $scope.datosReport.selecClub,
            'cvintegradora': $scope.datosReport.claveIntr,
            'cvini': $scope.datosReport.eveIni,
            'cvfin': $scope.datosReport.eveFin,
            'fechI': $scope.datosReport.FechaInicial,
            'fechF': $scope.datosReport.FechaFin
        }

        $http.post(rutainfoPrcs, requestData, { responseType: 'blob' }).then(function (data, status, headers) {
            headers = data.headers();

            var contentType = headers['content-type'];
            var linkElement = document.createElement('a');

            try {
                var blob = new Blob([data.data], { type: "application/pdf" });
                var url = window.URL.createObjectURL(blob);

                linkElement.setAttribute('href', url);

                linkElement.setAttribute("download", "myProcePDF.pdf");

                var clickEvent = new MouseEvent("click", {
                    "view": window,
                    "bubbles": true,
                    "cancelable": false
                });

                linkElement.dispatchEvent(clickEvent);
            } catch (ex) {
                console.log(ex);
            }
        }), function (errInfo) {
            console.log(errInfo);
        }

    }
    //Fin Generar PDF Procecsos


});