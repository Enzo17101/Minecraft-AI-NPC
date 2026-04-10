package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class PlayerData {
    private String playerUuid;
    private String playerName;
    private String message;
    private String heldItem;
    private double economyBalance;
    private double playerHealth;
    private double playerMaxHealth;
}