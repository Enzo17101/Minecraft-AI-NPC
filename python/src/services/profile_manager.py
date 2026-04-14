import yaml
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ProfileManager:
    def __init__(self, profiles_dir: str = "npc_profiles"):
        self.profiles_dir = profiles_dir
        self.profiles: Dict[str, dict] = {}
        self.load_all_profiles()

    def load_all_profiles(self):
        """
        Parses all YAML files in the profiles directory and stores them in memory.
        This prevents disk read operations during real-time game interactions.
        """
        if not os.path.exists(self.profiles_dir):
            logger.warning(f"Profiles directory '{self.profiles_dir}' not found. Creating it.")
            os.makedirs(self.profiles_dir)
            return

        for filename in os.listdir(self.profiles_dir):
            if filename.endswith((".yaml", ".yml")):
                npc_id = os.path.splitext(filename)[0]
                filepath = os.path.join(self.profiles_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        self.profiles[npc_id] = yaml.safe_load(file) or {}
                    logger.info(f"Loaded NPC profile: {npc_id}")
                except Exception as e:
                    logger.error(f"Failed to load profile {filename}: {e}")

    def get_action_commands(self, npc_id: str, intent: str, player_name: str) -> List[str]:
        """
        Retrieves the configured commands for a specific intent and injects the player's name.
        Defaults to an empty list if no action is configured.
        """
        profile = self.profiles.get(npc_id.lower())
        if not profile:
            return []

        actions = profile.get("actions", {})
        raw_commands = actions.get(intent, [])

        return [cmd.replace("{player}", player_name) for cmd in raw_commands]