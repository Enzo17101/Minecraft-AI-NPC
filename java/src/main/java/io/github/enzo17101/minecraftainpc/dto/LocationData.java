package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class LocationData {
    private double x;
    private double y;
    private double z;
}
