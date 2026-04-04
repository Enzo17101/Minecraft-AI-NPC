package io.github.enzo17101.minecraftainpc.dto;

import com.google.gson.annotations.SerializedName;
import java.util.List;
import lombok.Data;

@Data
public class OutgoingPayload {
    private String status;
    private String message;
    @SerializedName("action_intent")
    private String actionIntent;
    private List<String> commands;
}