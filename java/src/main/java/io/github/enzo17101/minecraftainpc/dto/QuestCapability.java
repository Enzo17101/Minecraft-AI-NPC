package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class QuestCapability {
    private String id;
    private String loreDescription;
    private String status;
}