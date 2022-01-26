var app = angular.module("MyControllerAngArts", []);
var rutaInfoArts = '/report_Art/';
var rutadatosArt = '/datos_Art/';
var rutainfoArt = '/info_Arts/';


app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


app.controller("ControllerHTTPArts", function ($scope, $http) {
    $scope.rpArt = false;


    //Formulario Ingreso Report
    $scope.envArt = function (articulo) {

        if (articulo == null || articulo == "Sin") { return; };

        $http.post(rutadatosArt, {
            "articulo": articulo
        })
            .then(function (rspDatasArt) {
                $scope.listaEstado = rspDatasArt.data.estados;
                $scope.listaEstadoRevers = rspDatasArt.data.estReverse;
                $scope.rpArt = true;
            }), function (errArt) {
                console.log(errArt)
            };
    };
    //Fin Formulario Ingreso Report



    //Generar PDF Art
    $scope.generarPDF = function (art) {

        var requestData = {
            'art': $scope.datosReport.idart,
            'estado': $scope.datosReport.selecEstado,
            'estaRv': $scope.datosReport.selecEstadoRever,
            'fechI': $scope.datosReport.FechaInicial,
            'fechF': $scope.datosReport.FechaFin
        }

        $http.post(rutainfoArt, requestData, { responseType: 'blob' }).then(function (data, status, headers) {
            headers = data.headers();
            var contentType = headers['content-type'];
            var linkElement = document.createElement('a');

            try {
                var blob = new Blob([data.data], { type: "application/pdf" });
                var url = window.URL.createObjectURL(blob);

                linkElement.setAttribute('href', url);

                linkElement.setAttribute("download", "myArtsPDF.pdf");

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
    //Fin Generar PDF Art


});