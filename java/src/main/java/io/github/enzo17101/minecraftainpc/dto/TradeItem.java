package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

/**
 * Represents a single item available for purchase from the NPC.
 */
@Data
@Builder
public class TradeItem {

    /**
     * Minecraft material ID or custom item name.
     */
    private String item;

    /**
     * Remaining physical quantity in the merchant's inventory.
     * Guaranteed to be >= 0 by the backend.
     */
    private int stock;

    /**
     * Unit cost in the server's economy currency.
     * Guaranteed to be >= 0.0 by the backend.
     */
    private double price;
}