package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

/**
 * Represents the current state and context of the interacting player.
 */
@Data
@Builder
public class PlayerData {

    /**
     * Unique identifier for the player.
     */
    private String playerUuid;

    /**
     * Display name of the player.
     */
    private String playerName;

    /**
     * Chat message sent by the player, if applicable.
     */
    private String message;

    /**
     * The item currently held in the player's main hand.
     */
    private String heldItem;

    /**
     * Player's current balance in the server's economy.
     */
    private double economyBalance;

    /**
     * Player's current health amount.
     */
    private double playerHealth;

    /**
     * Player's maximum health capacity.
     */
    private double playerMaxHealth;
}