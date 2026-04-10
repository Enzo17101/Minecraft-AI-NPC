package io.github.enzo17101.minecraftainpc.utils;

import io.github.enzo17101.minecraftainpc.dto.OutgoingPayload;
import net.kyori.adventure.text.minimessage.MiniMessage;
import org.bukkit.Bukkit;
import org.bukkit.entity.Player;
import org.bukkit.potion.PotionEffect;
import org.bukkit.potion.PotionEffectType;

import java.util.UUID;

public class ActionDispatcher {

    public static void dispatch(OutgoingPayload payload) {
        if (payload.getTargetPlayerUuid() == null) {
            Bukkit.getLogger().warning("[AI] No target player UUID provided in the payload.");
            return;
        }

        Player player = Bukkit.getPlayer(UUID.fromString(payload.getTargetPlayerUuid()));
        if (player == null || !player.isOnline()) {
            return; // The player disconnected before the AI could answer
        }

        MiniMessage mm = MiniMessage.miniMessage();

        player.sendMessage(mm.deserialize("<gold>[Eldon]</gold> <white>" + payload.getMessage() + "</white>"));

        String intent = payload.getActionIntent() != null ? payload.getActionIntent() : "CHAT_ONLY";

        switch (intent) {
            case "TRIGGER_ASSISTANCE":
                player.addPotionEffect(new PotionEffect(PotionEffectType.REGENERATION, 200, 1));
                player.sendMessage(mm.deserialize("<gray><i>Vous ressentez une chaleur apaisante...</i></gray>"));
                break;

            case "TRIGGER_TRADE":
                player.sendMessage(mm.deserialize("<yellow>[Système] Ouverture de l'inventaire du marchand...</yellow>"));
                break;

            case "TRIGGER_QUEST":
                player.sendMessage(mm.deserialize("<aqua>[Système] Redirection vers Typewriter...</aqua>"));
                break;

            case "CHAT_ONLY":
            default:
                break;
        }
    }
}