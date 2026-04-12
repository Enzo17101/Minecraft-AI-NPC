package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;
import java.util.List;

/**
 * Defines the merchant capabilities of an NPC.
 */
@Data
@Builder
public class TradeCapability {

    /**
     * True if this NPC is currently acting as a merchant.
     */
    private boolean isMerchant;

    /**
     * List of items currently available for sale.
     */
    private List<TradeItem> inventory;
}