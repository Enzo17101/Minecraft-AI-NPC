from typing import Optional, List
from pydantic import BaseModel, Field

class LocationData(BaseModel):
    """Physical coordinates within the Minecraft world."""
    x: float = Field(description="Exact X coordinate in the world")
    y: float = Field(description="Exact Y coordinate (vertical height)")
    z: float = Field(description="Exact Z coordinate in the world")

class WorldData(BaseModel):
    """Contextual state of the Minecraft server environment."""
    event_type: str = Field(description="Trigger type, e.g., 'CHAT' or 'RIGHT_CLICK'")
    timestamp: int = Field(description="Unix timestamp of the interaction in milliseconds")
    world_time: int = Field(ge=0, le=24000, description="In-game server ticks (0 to 24000)")
    weather: str = Field(description="Current weather state, e.g., 'CLEAR' or 'STORM'")

class PlayerData(BaseModel):
    """Real-time statistics and state of the interacting player."""
    player_uuid: str = Field(description="Unique Minecraft UUID of the player")
    player_name: str = Field(description="In-game username")
    message: Optional[str] = Field(
        default=None, 
        description="The chat message sent by the player. None for physical interactions."
    )
    held_item: str = Field(description="Raw material ID of the item in the main hand")
    economy_balance: float = Field(ge=0.0, description="Current vault balance of the player")
    player_health: float = Field(ge=0.0, description="Current health points")
    player_max_health: float = Field(gt=0.0, description="Maximum possible health points (depends on server plugins)")

class QuestCapability(BaseModel):
    """Defines a quest currently available to be triggered by this NPC."""
    id: str = Field(description="Internal quest ID matching the Typewriter/Quest plugin database")
    lore_description: str = Field(description="Short narrative summary of the quest requirements")
    status: str = Field(description="Current state of the quest, e.g., 'NOT_STARTED' or 'IN_PROGRESS'")

class TradeItem(BaseModel):
    """Represents a single item available for purchase from the NPC."""
    item: str = Field(description="Minecraft material ID or custom item name")
    stock: int = Field(ge=0, description="Remaining physical quantity in the merchant's inventory")
    price: float = Field(ge=0.0, description="Unit cost in the server's economy currency")

class TradeCapability(BaseModel):
    """Encapsulates the merchant profile and inventory limits of the NPC."""
    is_merchant: bool = Field(description="True if the NPC has the authority to sell items")
    inventory: List[TradeItem] = Field(default_factory=list, description="List of items currently for sale")

class Capabilities(BaseModel):
    """
    The declarative constraint engine. 
    Defines strictly what actions the NPC is legally allowed to execute based on the Java server's state.
    """
    available_quests: List[QuestCapability] = Field(
        default_factory=list, 
        description="Quests the player meets the requirements for"
    )
    trade: Optional[TradeCapability] = Field(
        default=None, 
        description="Merchant data, or None if the NPC does not trade"
    )
    can_assist: bool = Field(
        default=False, 
        description="True if the NPC is allowed to cast healing or buffing spells"
    )

class NPCData(BaseModel):
    """Current state and identity of the artificial entity being spoken to."""
    npc_uuid: str = Field(description="Unique identifier of the entity (MythicMobs UUID or Citizens ID)")
    npc_name: str = Field(description="Display name of the NPC")
    npc_health: float = Field(ge=0.0, description="Current health points of the entity")
    npc_location: LocationData = Field(description="Exact physical location to calculate distances if needed")
    capabilities: Capabilities = Field(description="The active limitations and authorizations for this interaction")

class IntentResult(BaseModel):
    """
    Data transfer object mapping the local LLM JSON output to Python types.
    Represents the mathematical classification of a player's interaction.
    """
    intent: str = Field(description="The detected intent matched against the predefined taxonomy")
    extracted_target: Optional[str] = Field(
        default=None, 
        description="Specific item, quest name, or subject the player focused on"
    )

class IncomingPayload(BaseModel):
    """The master DTO received from the Java WebSocket client."""
    world: WorldData = Field(description="Environment context")
    player: PlayerData = Field(description="Player context")
    npc: NPCData = Field(description="NPC context and limits")

class OutgoingPayload(BaseModel):
    """The master DTO sent back to the Java WebSocket client for execution."""
    target_player_uuid: Optional[str] = Field(
        default=None, 
        description="Used by the Java server to route the response to the correct player"
    )
    npc_name: Optional[str] = Field(
        default="NPC",
        description="The display name of the entity currently speaking"
    )
    status: str = Field(
        default="SUCCESS", 
        description="'SUCCESS' or 'ERROR' based on pipeline execution"
    )
    message: str = Field(description="The immersive roleplay text generated by the Cloud LLM")
    action_intent: Optional[str] = Field(
        default=None, 
        description="The declarative action code intercepted by the Java rules engine"
    )
    commands: List[str] = Field(
        default_factory=list,
        description="Raw Minecraft console commands mapped to the intent"
    )