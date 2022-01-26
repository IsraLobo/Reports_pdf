var app = angular.module("MyControllerAng", []);
var rutaDtsPro = '/datos_Proyec/';
var rutaInfo = '/info_Proyec/';
var rutaInfoArts = '/report_Art/';


app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


app.controller("ControllerHTTP", function ($scope, $http) {
    $scope.estado = false;
    $scope.datosReport = {};


    //Formulario Ingreso Report
    $scope.invocReport = function (clasif) {

        if (clasif == null) { return; };

        $http.post(rutaDtsPro, {
            "clasif": clasif
        })
            .then(function (rspFormulario) {
                $scope.listaEstado = rspFormulario.data.estados;
                $scope.listaEstadoRevers = rspFormulario.data.estReverse;
                $scope.listaStatus = rspFormulario.data.status;
                $scope.tipoClasf = rspFormulario.data.clasif;
                $scope.estado = true;
            }), function (errForm) {
                console.log(errForm);
            };
    };
    //Fin Formulario Ingreso Report


    //Generar Repor PDF
    $scope.generarReport = function (clas) {

        var requestData = {
            'clasif': clas,
            'estado': $scope.datosReport.selecEstado,
            'estaRv': $scope.datosReport.selecEstadoRever,
            'status': $scope.datosReport.selecEstatus,
            'fechI': $scope.datosReport.FechaInicial,
            'fechF': $scope.datosReport.FechaFin
        }

        $http.post(rutaInfo, requestData, { responseType: 'blob' }).then(function (data, status, headers) {
            headers = data.headers();
            var contentType = headers['content-type'];
            var linkElement = document.createElement('a');

            try {
                var blob = new Blob([data.data], { type: "application/pdf" });
                var url = window.URL.createObjectURL(blob);

                linkElement.setAttribute('href', url);

                linkElement.setAttribute("download", "mypdf.pdf");

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
    //Fin Generar Repor

});




//$http.get(rutaInfo + "/" + estd + "/" + estdRv + "/" + status + "/" + fechIni + "/" + fechFin + "/")