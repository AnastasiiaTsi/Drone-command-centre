from app.cor.base import Handler


class ReRouteHandler(Handler):
    def handle(self, request) -> bool:
        if request.get("type") == "obstacle_detected":
            print("ReRouteHandler: Obstacle detected, finding alternative route")
            # Implement rerouting logic
            return True
        return self._handle_next(request)