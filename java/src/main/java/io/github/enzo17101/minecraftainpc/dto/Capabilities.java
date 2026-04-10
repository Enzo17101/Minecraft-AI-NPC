package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;
import java.util.List;

@Data
@Builder
public class Capabilities {
    private List<QuestCapability> availableQuests;
    private TradeCapability trade;
    private boolean canAssist;
}