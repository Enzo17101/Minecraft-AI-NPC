package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;
import java.util.List;

@Data
@Builder
public class TradeCapability {
    private boolean isMerchant;
    private List<TradeItem> inventory;
}