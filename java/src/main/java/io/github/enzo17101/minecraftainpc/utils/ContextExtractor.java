package io.github.enzo17101.minecraftainpc.utils;

import io.github.enzo17101.minecraftainpc.dto.*;
import org.bukkit.World;
import org.bukkit.attribute.Attribute;
import org.bukkit.attribute.AttributeInstance;
import org.bukkit.entity.Entity;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;

import java.util.ArrayList;
import java.util.List;

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

        AttributeInstance maxHealthAttr = player.getAttribute(Attribute.MAX_HEALTH);
        double maxHealth = (maxHealthAttr != null) ? maxHealthAttr.getValue() : 20.0;

        PlayerData playerData = PlayerData.builder()
                .playerUuid(player.getUniqueId().toString())
                .playerName(player.getName())
                .message(message)
                .heldItem(player.getInventory().getItemInMainHand().getType().name())
                .playerHealth(player.getHealth())
                .playerMaxHealth(maxHealth)
                .economyBalance(0.0)
                .build();

        double npcHealth = (npc instanceof LivingEntity livingEntity) ? livingEntity.getHealth() : 20.0;

        NpcData npcData = NpcData.builder()
                .npcUuid(npc.getUniqueId().toString())
                .npcName(npc.getName().isEmpty()? npc.getName() : npc.getType().name())
                .npcHealth(npcHealth)
                .npcLocation(LocationData.builder()
                        .x(npc.getLocation().getX())
                        .y(npc.getLocation().getY())
                        .z(npc.getLocation().getZ())
                        .build())
                .build();

        List<TradeItem> simulatedInventory = new ArrayList<>();
        simulatedInventory.add(TradeItem.builder().item("apple").stock(18).price(6.0).build());

        TradeCapability tradeCapability = TradeCapability.builder()
                .isMerchant(true)
                .inventory(simulatedInventory)
                .build();

        Capabilities capabilities = Capabilities.builder()
                .availableQuests(new ArrayList<>())
                .trade(tradeCapability)
                .canAssist(false)
                .build();

        return IncomingPayload.builder()
                .world(worldData)
                .player(playerData)
                .npc(npcData)
                .capabilities(capabilities)
                .build();
    }
}
