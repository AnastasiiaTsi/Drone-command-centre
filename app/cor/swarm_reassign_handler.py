from app.cor.base import Handler


class SwarmReassignHandler(Handler):
    def handle(self, request) -> bool:
        if request.get("type") == "swarm_member_failed":
            print("SwarmReassignHandler: Swarm member failed, reassigning tasks")
            return True
        return self._handle_next(request)