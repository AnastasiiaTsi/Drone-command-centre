from app.cor.base import Handler


class EmergencyLandHandler(Handler):
    def handle(self, request) -> bool:
        if request.get("type") == "critical_failure":
            print("EmergencyLandHandler: Critical failure, initiating emergency landing")
            return True
        return self._handle_next(request)