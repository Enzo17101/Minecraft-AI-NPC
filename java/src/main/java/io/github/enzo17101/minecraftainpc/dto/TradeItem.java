package io.github.enzo17101.minecraftainpc.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class TradeItem {
    private String item;
    private int stock;
    private double price;
}