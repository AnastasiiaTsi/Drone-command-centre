from app.cor.base import Handler


class AdjustAltitudeHandler(Handler):
    def handle(self, request) -> bool:
        if request.get("type") == "low_visibility":
            print("AdjustAltitudeHandler: Low visibility, adjusting altitude")
            return True
        return self._handle_next(request)