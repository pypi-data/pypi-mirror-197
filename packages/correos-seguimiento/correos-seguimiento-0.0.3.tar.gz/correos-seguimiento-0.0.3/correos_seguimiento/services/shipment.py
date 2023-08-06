import requests


class UndefinedCredentials(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class InvalidEndpoint(Exception):
    pass


class UnknownApiResponse(Exception):
    pass


class InvalidApiResponse(Exception):
    pass


class TrackingShipment:
    def __init__(self, user, pwd, shipment_number):
        self.shipment_number = shipment_number
        self.user = user
        self.pwd = pwd

    def is_delivered(self):
        if not self.user or not self.pwd:
            raise UndefinedCredentials
        response = requests.get(
            "https://localizador.correos.es/"
            "canonico/eventos_envio_servicio_auth/"
            "{}?indUltEvento=S".format(self.shipment_number),
            auth=(self.user, self.pwd),
        )
        if response.status_code == 401:
            raise InvalidCredentials
        elif response.status_code != 200:
            raise InvalidEndpoint
        try:
            json = response.json()
        except requests.JSONDecodeError:
            raise InvalidApiResponse
        try:
            evento = json[0]["eventos"][0]
            status = evento["desTextoResumen"]
        except (IndexError, KeyError):
            raise UnknownApiResponse
        return status == "Entregado"
