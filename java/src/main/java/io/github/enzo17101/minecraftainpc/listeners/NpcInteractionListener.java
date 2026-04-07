package io.github.enzo17101.minecraftainpc.listeners;

import io.github.enzo17101.minecraftainpc.MinecraftAINPC;
import io.github.enzo17101.minecraftainpc.dto.IncomingPayload;
import io.github.enzo17101.minecraftainpc.utils.ContextExtractor;
import org.bukkit.entity.Entity;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerInteractEntityEvent;

public class NpcInteractionListener implements Listener {

    private final MinecraftAINPC plugin;

    public NpcInteractionListener(MinecraftAINPC plugin) {
        this.plugin = plugin;
    }

    @EventHandler
    public void onNpcRightClick(PlayerInteractEntityEvent event) {
        Entity clickedEntity = event.getRightClicked();

        // Temporary identifier
        // TODO: Replace with PersistentDataContainer (PDC) check for production to securely identify AI NPCs
        if (clickedEntity.getName().isEmpty() || !clickedEntity.getName().contains("Eldon")) {
            return;
        }

        // Prevent vanilla behaviors like opening trades or mounting
        event.setCancelled(true);

        Player player = event.getPlayer();

        IncomingPayload payload = ContextExtractor.buildPayload(
                player,
                clickedEntity,
                "RIGHT_CLICK",
                null
        );

        plugin.getWebSocketClient().sendAiRequest(payload);
    }
}