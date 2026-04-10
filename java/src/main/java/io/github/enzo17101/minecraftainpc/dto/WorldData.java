package io.github.enzo17101.minecraftainpc.dto;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class WorldData {
    private String eventType;
    private long timestamp;
    private long worldTime;
    private String weather;
}
