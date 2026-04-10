package io.github.enzo17101.minecraftainpc.dto;

import lombok.Data;

@Data
public class OutgoingPayload {
    private String targetPlayerUuid;
    private String status;
    private String message;
    private String actionIntent;
}