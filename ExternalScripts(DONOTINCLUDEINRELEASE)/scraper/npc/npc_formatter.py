import json
from pathlib import Path


class NPCFormatter:

    def __call__(self, **kwargs):
        self.__format()

    def __format(self) -> None:
        npc_input = self.__load_json_file("npc_data.json")
        with Path("npc_data.lua").open("w", encoding="utf-8") as g:
            g.write("return {\n")
            for item in npc_input:
                g.write("    [{id}] = {{\n".format(id=item["npcId"]))
                g.write("        [npcKeys.name] = \"{name}\",\n".format(name=item["name"]))
                g.write("        [npcKeys.minLevel] = {min_level},\n".format(min_level=item["minLevel"] if int(item["minLevel"]) < 99 else 99))  # "Son of Arugal" has level 9999
                g.write("        [npcKeys.maxLevel] = {max_level},\n".format(max_level=item["maxLevel"] if int(item["maxLevel"]) < 99 else 99))  # "Son of Arugal" has level 9999
                g.write("        [npcKeys.zoneID] = {zone_id},\n".format(zone_id=item["zoneId"] if "zoneId" in item else 0))
                g.write("        [npcKeys.spawns] = {spawns},\n".format(spawns=self.__get_spawns(item["spawns"] if "spawns" in item else [])))
                g.write("        [npcKeys.friendlyToFaction] = \"{friendly_to}\",\n".format(friendly_to=self.__get_race_string(item["reactAlliance"], item["reactHorde"])))
                g.write("    },\n")
            g.write("}\n")

    def __load_json_file(self, file_name: str):
        print("Loading '{}'...".format(file_name))
        with Path(file_name).open("r", encoding="utf-8") as f:
            data = json.load(f)
        sorted_data = sorted(data, key=lambda x: x.get('npcId', 0))
        print("Data contains {} entries".format(len(sorted_data)))
        return sorted_data

    def __get_race_string(self, react_alliance: str, react_horde) -> str:
        friendly_to = ""
        if react_alliance == "1":
            friendly_to += "A"
        if react_horde == "1":
            friendly_to += "H"
        if not friendly_to:
            friendly_to = "nil"

        return friendly_to

    def __get_spawns(self, spawns) -> str:
        spawns_string = ""
        for spawn in spawns:
            spawns_string += "            [{}] = {{".format(spawn[0])
            # coords_string has the format "[51.8,48.8],[53.4,47.4],[53.4,47.8],[53.6,47.2],[53.6,47.6]"
            coords_string = spawn[1]
            spawn_entries = json.loads("[" + coords_string + "]")
            for entry in spawn_entries:
                spawns_string += "{{{}, {}}},".format(entry[0], entry[1])
            spawns_string += "},\n"
        if not spawns_string:
            spawns_string = "nil"
        else:
            spawns_string = "{\n" + spawns_string + "        }"
        return spawns_string


if __name__ == '__main__':
    formatter = NPCFormatter()
    formatter()
