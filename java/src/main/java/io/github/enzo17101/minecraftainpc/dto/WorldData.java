package io.github.enzo17101.minecraftainpc.dto;
import com.google.gson.annotations.SerializedName;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class WorldData {
    @SerializedName("event_type")
    private String eventType;
    private long timestamp;

    @SerializedName("world_time")
    private long worldTime;
    private String weather;
}
