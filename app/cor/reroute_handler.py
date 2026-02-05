from app.cor.base import Handler

class RerouteHandler(Handler):
    def handle(self, request) -> bool:
        if request.get("type") == "obstacle_detected":
            print("RerouteHandler: Obstacle detected, finding alternative route")
            return True
        return self._handle_next(request)