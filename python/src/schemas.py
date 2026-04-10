from typing import List, Optional
from pydantic import BaseModel

class LocationData(BaseModel):
    x: float
    y: float
    z: float

class WorldData(BaseModel):
    event_type: str
    timestamp: int
    world_time: int
    weather: str

class PlayerData(BaseModel):
    player_uuid: str
    player_name: str
    # None if the interaction is a physical click without chat input
    message: Optional[str] = None
    held_item: str
    economy_balance: float
    player_health: float
    player_max_health: float

class QuestCapability(BaseModel):
    id: str
    lore_description: str
    status: str

class TradeItem(BaseModel):
    item: str
    stock: int
    price: float

class TradeCapability(BaseModel):
    is_merchant: bool
    inventory: list[TradeItem] = []

class Capabilities(BaseModel):
    available_quests: list[QuestCapability] = []
    trade: Optional[TradeCapability] = None
    can_assist: bool = False

class NPCData(BaseModel):
    npc_uuid: str
    npc_name: str
    npc_health: float
    npc_location: LocationData
    capabilities: Capabilities

class IncomingPayload(BaseModel):
    world: WorldData
    player: PlayerData
    npc: NPCData

class OutgoingPayload(BaseModel):
    status: str
    message: str
    action_intent: Optional[str] = None