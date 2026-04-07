package io.github.enzo17101.minecraftainpc.commands;

import io.github.enzo17101.minecraftainpc.MinecraftAINPC;
import io.github.enzo17101.minecraftainpc.dto.IncomingPayload;
import io.github.enzo17101.minecraftainpc.utils.ContextExtractor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Entity;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

import java.util.Comparator;

public class TalkCommand implements CommandExecutor {

    private final MinecraftAINPC plugin;

    public TalkCommand(MinecraftAINPC plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String label, @NotNull String[] args) {
        if (!(sender instanceof Player player)) {
            sender.sendMessage("Only players can talk to NPCs.");
            return true;
        }

        if (args.length == 0) {
            player.sendMessage("§cUsage: /talk <your message here>");
            return true;
        }

        // Reconstruct the message from arguments
        String message = String.join(" ", args);

        // Find the nearest AI NPC to act as the target of this message
        // Search radius: 10 blocks
        Entity targetNpc = player.getNearbyEntities(10, 10, 10).stream()
                .filter(e -> e.getName() != null && e.getName().contains("Eldon"))
                .min(Comparator.comparingDouble(e -> e.getLocation().distanceSquared(player.getLocation())))
                .orElse(null);

        if (targetNpc == null) {
            player.sendMessage("§cThere is no one nearby to hear you.");
            return true;
        }

        IncomingPayload payload = ContextExtractor.buildPayload(
                player,
                targetNpc,
                "CHAT",
                message
        );

        plugin.getWebSocketClient().sendAiRequest(payload);
        player.sendMessage("§7[You] " + message);

        return true;
    }
}