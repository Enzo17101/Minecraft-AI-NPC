package io.github.enzo17101.minecraftainpc;

import io.github.enzo17101.minecraftainpc.commands.TalkCommand;
import io.github.enzo17101.minecraftainpc.listeners.NpcInteractionListener;
import io.github.enzo17101.minecraftainpc.network.AiWebSocketClient;
import org.bukkit.plugin.java.JavaPlugin;

import java.net.URI;
import java.net.URISyntaxException;

public class MinecraftAINPC extends JavaPlugin {

    private AiWebSocketClient webSocketClient;

    @Override
    public void onEnable() {
        getLogger().info("Initializing AI NPC Orchestrator...");
        connectToBackend();

        // Register Command and Listeners
        if (getCommand("talk") != null) {
            getCommand("talk").setExecutor(new TalkCommand(this));
        }
        getServer().getPluginManager().registerEvents(new NpcInteractionListener(this), this);
    }

    @Override
    public void onDisable() {
        getLogger().info("Shutting down AI NPC Orchestrator...");
        if (webSocketClient != null && !webSocketClient.isOpen()) {
            webSocketClient.close();
        }
    }

    private void connectToBackend() {
        try {
            // Default URI for the Python FastAPI backend
            URI uri = new URI("ws://localhost:8000/ws/chat");
            webSocketClient = new AiWebSocketClient(uri, this);
            webSocketClient.connect();
        } catch (URISyntaxException e) {
            getLogger().severe("Invalid WebSocket URI formatting.");
        }
    }

    public AiWebSocketClient getWebSocketClient() {
        return webSocketClient;
    }
}