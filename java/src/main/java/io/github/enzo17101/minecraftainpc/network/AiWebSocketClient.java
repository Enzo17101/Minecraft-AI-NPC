package io.github.enzo17101.minecraftainpc.network;

import io.github.enzo17101.minecraftainpc.MinecraftAINPC;
import io.github.enzo17101.minecraftainpc.dto.IncomingPayload;
import io.github.enzo17101.minecraftainpc.dto.OutgoingPayload;
import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;
import org.bukkit.Bukkit;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.MiniMessage;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;

import java.net.URI;
import java.util.logging.Level;

public class AiWebSocketClient extends WebSocketClient {
    private final MinecraftAINPC plugin;
    private final Gson gson;

    public AiWebSocketClient(URI serverUri, MinecraftAINPC plugin) {
        super(serverUri);
        this.plugin = plugin;
        this.gson = new Gson();
    }

    @Override
    public void onOpen(ServerHandshake handshakedata) {
        plugin.getLogger().info("[WebSocket] Connected to AI Backend successfully.");
    }

    @Override
    public void onMessage(String message) {
        // This method is called on an ASYNCHRONOUS thread.
        try {
            // Deserialize the JSON from Python into our Java DTO
            OutgoingPayload response = gson.fromJson(message, OutgoingPayload.class);

            // Dispatch the logic back to the Bukkit Main Thread to safely interact with the game
            Bukkit.getScheduler().runTask(plugin, () -> handleAiResponse(response));

        } catch (JsonSyntaxException e) {
            plugin.getLogger().log(Level.SEVERE, "[WebSocket] Failed to parse JSON from backend: " + message, e);
        }
    }

    @Override
    public void onClose(int code, String reason, boolean remote) {
        plugin.getLogger().warning("[WebSocket] Disconnected from AI Backend. Reason: " + reason);
        // Note: Automatic reconnection logic will be added here later if needed.
    }

    @Override
    public void onError(Exception ex) {
        plugin.getLogger().log(Level.SEVERE, "[WebSocket] An error occurred.", ex);
    }

    /**
     * Serializes an IncomingPayload to JSON and sends it to the Python backend.
     * @param payload The data context to send.
     */
    public void sendAiRequest(IncomingPayload payload) {
        if (this.isOpen()) {
            String json = gson.toJson(payload);
            this.send(json);
            plugin.getLogger().info("[WebSocket] Sent request to AI Backend.");
        } else {
            plugin.getLogger().warning("[WebSocket] Cannot send request: Connection is closed.");
        }
    }

    /**
     * Processes the response from the AI strictly on the main server thread.
     * @param response The parsed outgoing payload from Python.
     */
    private void handleAiResponse(OutgoingPayload response) {
        // We are now safely on the Bukkit Main Thread.
        // For Sprint 1 (Echo test), we will just broadcast the message to the entire server to test it
        MiniMessage mm = MiniMessage.miniMessage();

        if ("ERROR".equals(response.getStatus())) {
            Component errorMsg = mm.deserialize("<red>[AI ERROR]</red> <white>" + response.getMessage() + "</white>");
            Bukkit.getServer().broadcast(errorMsg);
            return;
        }

        Component npcMsg = mm.deserialize("<gold>[NPC AI]</gold> <white>" + response.getMessage() + "</white>");
        Bukkit.getServer().broadcast(npcMsg);

        // Command execution stub (will be fully implemented in Sprint 4)
        if (response.getCommands() != null && !response.getCommands().isEmpty()) {
            for (String cmd : response.getCommands()) {
                plugin.getLogger().info("Executing command: " + cmd);
                // Bukkit.dispatchCommand(Bukkit.getConsoleSender(), cmd);
            }
        }
    }
}
