package io.github.enzo17101.minecraftainpc.dto;

import lombok.Data;

import java.util.List;

/**
 * The expected response structure from the AI backend to the Minecraft plugin.
 */
@Data
public class OutgoingPayload {

    /**
     * Unique identifier of the player who should receive the response.
     */
    private String targetPlayerUuid;

    /**
     * Name of the NPC who answer to the player.
     */
    private String npcName;


    /**
     * Status of the backend processing (e.g. "SUCCESS", "ERROR").
     */
    private String status;

    /**
     * The dialog line the NPC should speak to the player.
     */
    private String message;

    /**
     * Specific action the NPC should perform.
     */
    private String actionIntent;

    /**
     * Specific commands linked ton the action
     */

    private List<String> commands;
}