package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

/**
 * Represents geographical coordinates within the Minecraft world.
 */
@Data
@Builder
public class LocationData {

    /**
     * The X coordinate.
     */
    private double x;

    /**
     * The Y coordinate (height).
     */
    private double y;

    /**
     * The Z coordinate.
     */
    private double z;
}
