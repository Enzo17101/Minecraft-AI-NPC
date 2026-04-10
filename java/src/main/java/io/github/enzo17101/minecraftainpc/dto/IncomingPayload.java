package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class IncomingPayload {
    private WorldData world;
    private PlayerData player;
    private NpcData npc;
    private Capabilities capabilities;
}