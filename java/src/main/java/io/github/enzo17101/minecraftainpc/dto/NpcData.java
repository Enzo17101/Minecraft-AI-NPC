package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class NpcData {
    private String npcUuid;
    private String npcName;
    private double npcHealth;
    private LocationData npcLocation;
    private Capabilities capabilities;
}