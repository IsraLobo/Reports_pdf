var app = angular.module("MyControllerAngVnts", []);
var rutaInfoVnts = '/report_ventas/';
var rutadatosVts = '/datos_ventas/';
var rutainfoVts = '/info_ventas/';


app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


app.controller("ControllerHTTPVnts", function ($scope, $http) {
    

    //Ventas
    $scope.ReporVent = function () {

        $http.get(rutadatosVts)
            .then(function (rspForm) {
                $scope.listaEstado = rspForm.data.estados;
                $scope.listaEstadoRevers = rspForm.data.estReverse;
                $scope.rpVnt = true;
            }, function (err) {
                console.log(err);
            });
    };
    //Fin Ventas



    //Generar PDF Vnt
    $scope.generarPDF = function () {

        var requestData = {
            'estado': $scope.datosReport.selecEstado,
            'estaRv': $scope.datosReport.selecEstadoRever,
            'fechI': $scope.datosReport.FechaInicial,
            'fechF': $scope.datosReport.FechaFin
        }

        $http.post(rutainfoVts, requestData, { responseType: 'blob' }).then(function (data, status, headers) {
            headers = data.headers();
            var contentType = headers['content-type'];
            var linkElement = document.createElement('a');

            try {
                var blob = new Blob([data.data], { type: "application/pdf" });
                var url = window.URL.createObjectURL(blob);

                linkElement.setAttribute('href', url);

                linkElement.setAttribute("download", "myVtnsPDF.pdf");

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
    //Fin Generar PDF Vnt


});