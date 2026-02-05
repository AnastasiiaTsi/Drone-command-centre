from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.factory.mission_factory import MissionFactory
from app.config.mission_config import MissionConfig

router = APIRouter()
# Тимчасове сховище результатів у пам'яті
missions_db = {}

@router.post("/mission/run")
def run_mission(cfg: Dict[str, Any]):
    try:
        config = MissionConfig(**cfg)
        drone, environment, controller, strategy, cor_chain = MissionFactory.create_from_config(config)
        
        result = drone.execute_mission()
        
        mission_id = config.mission_id
        missions_db[mission_id] = {
            "status": "completed",
            "result": result,
            "drone_type": drone.get_drone_type(),
            "environment": environment.__class__.__name__
        }
        
        return {"mission_id": mission_id, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/mission/result/{mission_id}")
def get_mission_result(mission_id: str):
    if mission_id not in missions_db:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    data = missions_db[mission_id]
    return {
        "mission_id": mission_id,
        "drone_type": data["drone_type"],
        "environment": data["environment"],
        "result": data["result"]
    }