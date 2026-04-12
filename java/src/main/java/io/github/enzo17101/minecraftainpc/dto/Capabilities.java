package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;
import java.util.List;

/**
 * Defines the features and interactions supported by a specific NPC.
 */
@Data
@Builder
public class Capabilities {

    /**
     * List of quests the NPC can offer or participate in.
     */
    private List<QuestCapability> availableQuests;

    /**
     * The merchant capabilities of this NPC, including inventory.
     */
    private TradeCapability trade;

    /**
     * Indicates whether the NPC can physically assist the player (e.g., following, fighting).
     */
    private boolean canAssist;
}