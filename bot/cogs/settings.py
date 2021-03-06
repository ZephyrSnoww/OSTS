from typing import MappingView
from discord.ext import commands
from importlib import reload
import discord
import inspect
import helpers
import re


class Settings(commands.Cog, description=""):
    def __init__(self, bot):
        self.osts = bot
        self.cog_name = "Settings"
        self.data = helpers.get_toml("data")

    # ==================================================
    # Unload Event
    # ==================================================
    def cog_unload(self):
        helpers.log(text="Unloaded", cog=self.cog_name)


    # ==================================================
    # Server settings
    # ==================================================
    @commands.command(aliases=["ss"], brief="Change server-specific settings!", help="""\
        __**Server Settings**__
        Change server-specific settings to whatever you like!

        __Viewing Server Settings__
        `[prefix]server_settings list`
        
        __Changing the Bot's Prefix__
        `[prefix]server_settings prefix os.`
        `[prefix]server_settings prefix !`

        __Toggling Invocation Deletion__
        `[prefix]server_settings delete_command`
        """)
    @commands.has_permissions(manage_guild=True)
    async def server_settings(self, ctx, _one="", _two=""):
        server_data = helpers.get_toml(f"servers/{ctx.guild.id}")
        if server_data.get("delete_invocation") == True:
            await helpers.try_delete(ctx)
    
        if _one not in ["prefix", "delete_command", "list"]:
            return await helpers.give_output(
                embed_title = f"the {re.sub(r'_', ' ', inspect.stack()[0][3])} command!",
                embed_content = re.sub(r"\[prefix\]", self.osts.command_prefix(self.osts, ctx.message), self.osts.get_command(inspect.stack()[0][3]).help),
                ctx = ctx
            )
    
        # ==================================================
        # If theyre listing the servers settings
        # ==================================================
        if _one == "list":
            embed = helpers.make_embed(
                title = helpers.success_title(ctx),
                content = "Here are this server's settings!",
                ctx = ctx
            )

            embed.add_field(
                name = "Prefix",
                value = server_data.get("prefix"),
                inline = True
            )

            embed.add_field(
                name = "Command Message Deletion",
                value = "Enabled" if server_data.get("delete_invocation") else "Disabled"
            )

            return await helpers.give_output(
                embed = embed,
                log_text = "Listed server settings",
				cog = self.cog_name,
                ctx = ctx
            )
        
        # ==================================================
        # If theyre changing the bots prefix
        # ==================================================
        if _one == "prefix":
            previous_prefix = server_data.get("prefix")
            if not previous_prefix:
                previous_prefix = "None"
            server_data["prefix"] = _two

            return await helpers.give_output(
                embed_title = helpers.success_title(ctx),
                embed_content = f"My prefix has been changed from \"{previous_prefix}\" to \"{_two}\"!",
                log_text = f"Changed server prefix to {_two}",
                ctx = ctx,
				cog = self.cog_name,
                data = server_data,
                data_file = f"servers/{ctx.guild.id}"
            )

        # ==================================================
        # If theyre toggling invocation deletion
        # ==================================================
        if _one == "delete_command":
            if server_data.get("delete_invocation"):
                server_data["delete_invocation"] = not server_data["delete_invocation"]
            else:
                server_data["delete_invocation"] = True

            return await helpers.give_output(
                embed_title = helpers.success_title(ctx),
                embed_content = f"Command deletion has been {'enabled' if server_data['delete_invocation'] else 'disabled'}!",
                log_text = f"Toggled invocation deletion",
                ctx = ctx,
				cog = self.cog_name,
                data = server_data,
                data_file = f"servers/{ctx.guild.id}"
            )


    # ==================================================
    # User settings
    # ==================================================
    @commands.command(aliases=["us"], brief="Change user-specific settings!", help="""\
        __**User Settings**__
        Change user-specific settings to whatever you like!

        __Viewing Your Settings__
        `[prefix]user_settings list`
       
        __Changing Your Color__
        `[prefix]user_settings color FFFF00`

        __Changing Your Prefix__
        `[prefix]user_settings prefix os.`
        `[prefix]user_settings prefix !`

        __Changing Your Success Title__
        This is the title that gets displayed when a command is a success.
        `[prefix]user_settings success Alright!`

        __Changing Your Error Title__
        This is the title that gets displayed when a command is a error.
        `[prefix]user_settings error Whoops!`
        """)
    async def user_settings(self, ctx, _one="", *, _two=""):
        server_data = helpers.get_toml(f"servers/{ctx.guild.id}")
        if server_data.get("delete_invocation") == True:
            await helpers.tryDelete(ctx)
    
        # ==================================================
        # If they didnt enter a correct category
        # Give them the help message
        # ==================================================
        if _one not in ["list", "color", "prefix", "success", "error"]:
            return await helpers.give_output(
                embed_title = f"the {re.sub(r'_', ' ', inspect.stack()[0][3])} command!",
                embed_content = re.sub(r"\[prefix\]", self.osts.command_prefix(self.osts, ctx.message), self.osts.get_command(inspect.stack()[0][3]).help),
                ctx = ctx
            )

        # ==================================================
        # Yoink user data
        # ==================================================
        user_data = helpers.get_toml(f"users/{ctx.author.id}")
    
        # ==================================================
        # If theyre viewing their settings
        # ==================================================
        if _one == "list":
            embed = helpers.make_embed(
                title = helpers.success_title(ctx),
                content = "Here are your user settings",
                ctx = ctx
            )

            embed.add_field(
                name = "Color",
                value = user_data.get("color"),
                inline = True
            )

            embed.add_field(
                name = "Prefix",
                value = user_data.get("prefix"),
                inline = True
            )

            embed.add_field(
                name = "Success Title",
                value = user_data.get("success title"),
                inline = True
            )

            embed.add_field(
                name = "Error Title",
                value = user_data.get("error title"),
                inline = True
            )

            return await helpers.give_output(
                embed = embed,
                log_text = f"Listed their user settings",
				cog = self.cog_name,
                ctx = ctx
            )
        
        # ==================================================
        # If theyre changing the color
        # ==================================================
        if _one == "color":
            try:
                _temp = int("0x" + _two, 0)
            except:
                return await helpers.give_output(
                    embed_title = helpers.error_title(ctx),
                    embed_content = "That wasn't a valid color!",
                    log_text = f"Tried to change their color to an invalid color",
                    cog = self.cog_name,
                    ctx = ctx
                )

            previous_color = None
            if user_data.get("color"):
                previous_color = user_data["color"]

            user_data["color"] = _two

            return await helpers.give_output(
                embed_title = helpers.success_title(ctx),
                embed_content = f"Your color has been changed {'to' if not previous_color else f'from {previous_color} to'} {_two}",
                log_text = f"Changed user color to {_two}",
                ctx = ctx,
				cog = self.cog_name,
                data = user_data,
                data_file = f"users/{ctx.author.id}"
            )

        # ==================================================
        # If theyre changing their prefix
        # ==================================================
        if _one == "prefix":
            previous_prefix = None
            if user_data.get("prefix"):
                previous_prefix = user_data["prefix"]

            user_data["prefix"] = _two
            if _two == "":
                user_data["prefix"] = "os."

            return await helpers.give_output(
                embed_title = helpers.success_title(ctx),
                embed_content = f"Your prefix has been changed {'to' if not previous_prefix else f'from {previous_prefix} to'} {user_data['prefix']}",
                log_text = f"Changed user prefix to {_two}",
                ctx = ctx,
				cog = self.cog_name,
                data = user_data,
                data_file = f"users/{ctx.author.id}"
            )


        if _one == "success":
            user_data["success title"] = _two
            if _two == "":
                user_data["success title"] = "Alright!"

            return await helpers.give_output(
                embed_title = helpers.success_title(ctx),
                embed_content = f"Your success message is now \"{_two}\"!",
                log_text = f"Changed their user success title to {_two}",
                ctx = ctx,
                cog = self.cog_name,
                data = user_data,
                data_file = f"users/{ctx.author.id}"
            )


        if _one == "error":
            user_data["error title"] = _two
            if _two == "":
                user_data["error title"] = "Whoops!"

            return await helpers.give_output(
                embed_title = helpers.success_title(ctx),
                embed_content = f"Your error message is now \"{_two}\"!",
                log_text = f"Changed their user error title to {_two}",
                ctx = ctx,
                cog = self.cog_name,
                data = user_data,
                data_file = f"users/{ctx.author.id}"
            )


def setup(bot):
    helpers.log(text="Loaded", cog="Settings")
    bot.add_cog(Settings(bot))
    reload(helpers)