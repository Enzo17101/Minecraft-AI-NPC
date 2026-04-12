package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

/**
 * Represents a single quest that an NPC can provide or update.
 */
@Data
@Builder
public class QuestCapability {

    /**
     * Unique identifier for the quest.
     */
    private String id;

    /**
     * Descriptive lore text of the quest to be presented to the player.
     */
    private String loreDescription;

    /**
     * The current state of this quest for the player (e.g. "AVAILABLE", "IN_PROGRESS", "COMPLETED").
     */
    private String status;
}