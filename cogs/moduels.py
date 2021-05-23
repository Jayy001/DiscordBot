import json
from search_that_hash import api
from name_that_hash.runner import api_return_hashes_as_json
from pywhat import identifier
import discord
import requests


class hacking_modules:
    def __init__(self):
        self.id = identifier.Identifier()
        self.colors = {"Failed": 0xDC143C, "Success": 0x00FF00}

    def get_embed(self, type, message, title):
        embed = discord.Embed(title=title, description=message, color=self.colors[type])
        embed.set_footer(
            text="HDB is licensed under GPLv3 - Join our discord http://discord.skerritt.blog"
        )
        return embed

    def get_link(self, embed, link):
        embed.add_field(
            name="Links",
            inline=False,
            value=f"Our github: {link}",
        )
        return embed

    def nth(self, hash):
        to_print = ""

        types = json.loads(api_return_hashes_as_json([hash]))

        if len(types[hash]) != 0:
            for i in range(len(types[hash])):
                if i > 100:
                    break
                to_print += types[hash][i]["name"] + "\n"

            embed = self.get_embed(
                "Success", "I found some possible hash types", "Success 👍"
            )

            embed.add_field(name="Found Hash Types", value=to_print)
        else:
            embed = self.get_embed(
                "Failed", "Could not find any hash types", "Failed 😕"
            )

        return embed

    def what(self, text):
        out = self.id.identify(text, api=True)

        if out["Regexes"]:
            embed = self.get_embed(
                "Success", f"I identified this text: {text}", "Success 👍"
            )
            for possible_regex in out["Regexes"]:
                embed.add_field(
                    name="Possible type",
                    inline=False,
                    value=f"Name: {possible_regex['Regex Pattern']['Name']}\nInfo: {possible_regex['Regex Pattern']['Description']}",
                )
        else:
            embed = self.get_embed(
                "Failed", "Could not identify with PyWhat", "Failed 😕"
            )

            if out["Language"]:
                text = ""

                for lang in out["Language"]:
                    text += str(lang).split(":")[0] + "\n"

                embed.add_field(name="Possible language found", value=text)

        return embed

    def ciphey(self, text):
        out = requests.get(
            f"https://pl8u5p7v00.execute-api.us-east-2.amazonaws.com/default/ciphey_lambda_api?ctext={text}"
        ).text.strip('"')

        if out == '{"message": "Internal server error"}':
            embed = self.get_embed("Failed", "Took too long to decrypt!", "Try the CLI version instead https://github.com/ciphey/ciphey 😕")
        elif out == "Failed to crack":
            embed = self.get_embed(
                "Failed", "Ciphey could not decrypt this text", "Failed 😕"
            )
        else:
            embed = self.get_embed(
                "Success", "Ciphey decrypted this text", "Success 👍"
            )
            embed.add_field(name="Result:", value=out)

        return embed

    def sth(self, hash):
        out = api.return_as_fast_json([hash.lower()])[0]
        if hash in out:
            if out[hash] == "No types found for this hash.":
                embed = self.ciphey(hash)
            elif out[hash] == "Could not crack hash":
                embed = self.nth(hash)
            else:
                embed = self.get_embed("Success", "STH cracked the hash", "Success 👍")
                embed.add_field(name="Result:", value=out[hash]["plaintext"])
                embed.add_field(
                    name="Type:", value="\n".join(out[hash]["types"]), inline=False
                )

                if not out[hash]["verified"]:
                    embed.add_field(
                        name="Warning:",
                        value="This hash is NOT verified so it could be incorrect.",
                    )

        else:
            embed = self.get_embed("Failed", "STH Broke", "Failed 😕")

        return embed
