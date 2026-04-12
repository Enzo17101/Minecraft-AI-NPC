package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

/**
 * Represents the current state and capabilities of the NPC interacting with the player.
 */
@Data
@Builder
public class NpcData {

    /**
     * Unique identifier for the NPC entity.
     */
    private String npcUuid;

    /**
     * Display name of the NPC.
     */
    private String npcName;

    /**
     * Current health of the NPC.
     */
    private double npcHealth;

    /**
     * Current coordinates of the NPC in the game world.
     */
    private LocationData npcLocation;

    /**
     * Set of capabilities available to this NPC, such as quests and trades.
     */
    private Capabilities capabilities;
}