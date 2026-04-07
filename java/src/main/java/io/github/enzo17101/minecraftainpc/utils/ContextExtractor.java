package io.github.enzo17101.minecraftainpc.utils;

import io.github.enzo17101.minecraftainpc.dto.IncomingPayload;
import io.github.enzo17101.minecraftainpc.dto.LocationData;
import io.github.enzo17101.minecraftainpc.dto.NpcData;
import io.github.enzo17101.minecraftainpc.dto.PlayerData;
import io.github.enzo17101.minecraftainpc.dto.WorldData;
import org.bukkit.World;
import org.bukkit.entity.Entity;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;

public class ContextExtractor {
    /**
     * Snapshots the current server state and maps it to the Python backend DTO schema.
     */
    public static IncomingPayload buildPayload(Player player, Entity npc, String eventType, String message) {
        World world = player.getWorld();

        WorldData worldData = WorldData.builder()
                .eventType(eventType)
                .timestamp(System.currentTimeMillis())
                .worldTime(world.getTime())
                .weather(world.hasStorm() ? "STORM" : "CLEAR")
                .build();

        PlayerData playerData = PlayerData.builder()
                .playerUuid(player.getUniqueId().toString())
                .playerName(player.getName())
                .message(message)
                .heldItem(player.getInventory().getItemInMainHand().getType().name())
                .playerHealth(player.getHealth())
                .economyBalance(0.0) // TODO: Integrate Vault API for real economy tracking
                .build();

        double npcHealth = (npc instanceof LivingEntity) ? ((LivingEntity) npc).getHealth() : 20.0;

        NpcData npcData = NpcData.builder()
                .npcUuid(npc.getUniqueId().toString())
                .npcName(!npc.getName().isEmpty() ? npc.getName() : npc.getType().name())
                .npcHealth(npcHealth)
                .npcLocation(LocationData.builder()
                        .x(npc.getLocation().getX())
                        .y(npc.getLocation().getY())
                        .z(npc.getLocation().getZ())
                        .build())
                .build();

        return IncomingPayload.builder()
                .world(worldData)
                .player(playerData)
                .npc(npcData)
                .build();
    }
}