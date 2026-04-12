package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

/**
 * The main data structure sent from the Minecraft plugin to the AI backend.
 * Contains full context of the interaction including world, player, and NPC data.
 */
@Data
@Builder
public class IncomingPayload {

    /**
     * Contextual information about the Minecraft world at the time of the event.
     */
    private WorldData world;

    /**
     * Specific details and context regarding the interacting player.
     */
    private PlayerData player;

    /**
     * Details about the NPC entity involved in the interaction.
     */
    private NpcData npc;
}