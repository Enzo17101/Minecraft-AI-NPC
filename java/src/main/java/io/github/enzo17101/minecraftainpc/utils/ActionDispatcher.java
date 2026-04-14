package io.github.enzo17101.minecraftainpc.utils;

import io.github.enzo17101.minecraftainpc.dto.OutgoingPayload;
import net.kyori.adventure.text.minimessage.MiniMessage;
import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.potion.PotionEffect;
import org.bukkit.potion.PotionEffectType;

import java.util.UUID;

public class ActionDispatcher {

    public static void dispatch(OutgoingPayload payload) {
        if (payload.getTargetPlayerUuid() == null) {
            Bukkit.getLogger().warning("[AI] No target player UUID provided in the payload.");
            return;
        }

        Player player = Bukkit.getPlayer(UUID.fromString(payload.getTargetPlayerUuid()));
        if (player == null || !player.isOnline()) {
            return; // The player disconnected before the AI could answer
        }

        MiniMessage mm = MiniMessage.miniMessage();

        String npcDisplayName = payload.getNpcName() != null ? payload.getNpcName() : "???";
        player.sendMessage(mm.deserialize("<gold>[" + npcDisplayName + "]</gold> <white>" + payload.getMessage() + "</white>"));

        // Executes all commands mapped by the Python backend securely via the server console
        if (payload.getCommands() != null && !payload.getCommands().isEmpty()) {
            for (String rawCommand : payload.getCommands()) {
                Bukkit.getScheduler().runTask(
                    Bukkit.getPluginManager().getPlugin("MinecraftAINPC"),
                    () -> {
                        // Check if the command should be forced as the player
                        if (rawCommand.startsWith("[PLAYER] ")) {
                            String cmd = rawCommand.replace("[PLAYER] ", "");
                            // The player silently executes the command themselves
                            player.performCommand(cmd);
                        } else {
                            // Default to Console execution, stripping the tag if explicitly provided
                            String cmd = rawCommand.replace("[CONSOLE] ", "");
                            Bukkit.dispatchCommand(Bukkit.getConsoleSender(), cmd);
                        }
                    }
                );
            }
        }
    }
}