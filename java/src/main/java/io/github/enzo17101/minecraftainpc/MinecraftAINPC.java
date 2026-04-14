package io.github.enzo17101.minecraftainpc;

import io.github.enzo17101.minecraftainpc.commands.TalkCommand;
import io.github.enzo17101.minecraftainpc.listeners.NpcInteractionListener;
import io.github.enzo17101.minecraftainpc.network.AiWebSocketClient;
import org.bukkit.plugin.java.JavaPlugin;
import org.checkerframework.checker.units.qual.Force;

import java.net.URI;
import java.net.URISyntaxException;

public class MinecraftAINPC extends JavaPlugin {

    private AiWebSocketClient webSocketClient;

    @Override
    public void onEnable() {
        getLogger().info("Initializing AI NPC Orchestrator...");
        connectToBackend("ws://localhost:8000/ws/chat");

        // Register Command and Listeners
        if (getCommand("talk") != null) {
            getCommand("talk").setExecutor(new TalkCommand(this));
        }
        getServer().getPluginManager().registerEvents(new NpcInteractionListener(this), this);
    }

    @Override
    public void onDisable() {
        // Force the main server thread to wait until the network thread is completely dead.
        // This prevents ClassLoader leaks and allows Plugman to cleanly release the .jar file.
        if (webSocketClient != null && !webSocketClient.isClosed()) {
            getLogger().info("Shutting down AI WebSocket connection...");
            try {
                webSocketClient.closeBlocking();
            } catch (InterruptedException e) {
                getLogger().severe("WebSocket shutdown was interrupted.");
                // Restore the interrupted status for the JVM thread manager
                Thread.currentThread().interrupt();
            }
        }

        // Kill all waiting tasks
        getServer().getScheduler().cancelTasks(this);

        getLogger().info("Plugin MinecraftAINPC successfully disabled.");
    }

    private void connectToBackend(String backendUri) {
        try {
            if(backendUri.isEmpty())
                backendUri = "ws://localhost:8000/ws/chat";

            // Default URI for the Python FastAPI backend
            URI uri = new URI(backendUri);
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