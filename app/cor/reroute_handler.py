from app.cor.base import Handler

# БУЛО: class ReRouteHandler(Handler):
# СТАЛО: class RerouteHandler(Handler):
class RerouteHandler(Handler):
    def handle(self, request) -> bool:
        if request.get("type") == "obstacle_detected":
            print("RerouteHandler: Obstacle detected, finding alternative route")
            # Implement rerouting logic
            return True
        return self._handle_next(request)