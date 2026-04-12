package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

/**
 * Represents the current state of the game world during the interaction.
 */
@Data
@Builder
public class WorldData {

    /**
     * The type of event that triggered this payload (e.g. "player_interact").
     */
    private String eventType;

    /**
     * Unix timestamp of the event.
     */
    private long timestamp;

    /**
     * Current time in the Minecraft world (in ticks).
     */
    private long worldTime;

    /**
     * Current weather condition in the world (e.g. "CLEAR", "STORM").
     */
    private String weather;
}
