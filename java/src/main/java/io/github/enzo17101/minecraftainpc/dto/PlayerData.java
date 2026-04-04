package io.github.enzo17101.minecraftainpc.dto;

import com.google.gson.annotations.SerializedName;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class PlayerData {
    @SerializedName("player_uuid")
    private String playerUuid;
    @SerializedName("player_name")
    private String playerName;
    private String message;
    @SerializedName("held_item")
    private String heldItem;
    @SerializedName("economy_balance")
    private double economyBalance;
    @SerializedName("player_health")
    private double playerHealth;
}