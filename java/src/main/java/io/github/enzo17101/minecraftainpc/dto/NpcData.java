package io.github.enzo17101.minecraftainpc.dto;

import com.google.gson.annotations.SerializedName;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class NpcData {
    @SerializedName("npc_uuid")
    private String npcUuid;
    @SerializedName("npc_name")
    private String npcName;
    @SerializedName("npc_health")
    private double npcHealth;
    @SerializedName("npc_location")
    private LocationData npcLocation;
}