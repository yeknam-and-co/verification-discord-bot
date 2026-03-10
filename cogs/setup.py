import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View, ChannelSelect, RoleSelect
class setupcommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self.qualified_name} is loaded.')

    @app_commands.command(name="setup", description="setup the bot for ur server")
    async def setup(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="setup",
            description="setup the bot for ur server",
            color=discord.Color.blurple()
        )
        channel_select = ChannelSelect(
            placeholder="select a text channel",
            min_values=1,
            max_values=1,
            channel_types=[discord.ChannelType.text]
        )
        async def channel_select_callback(interaction: discord.Interaction):

            role_select = RoleSelect(
                placeholder="select a role for verification",
                min_values=1,
                max_values=1
            )

            async def role_select_callback(role_interaction: discord.Interaction):
                await role_interaction.response.edit_message(
                    content=f"channel selected: {channel_select.values[0]}\nrole selected: {role_select.values[0].mention}",
                    view=None
                )

            role_select.callback = role_select_callback

            new_view = View()
            new_view.add_item(role_select)

            await interaction.response.edit_message(
                content=f"channel selected: {channel_select.values[0]}. now select a role.",
                view=new_view
            )
            
        channel_select.callback = channel_select_callback
        view = View()
        view.add_item(channel_select)
        await interaction.response.send_message(embed=embed, view=view)


        
async def setup(bot):
    await bot.add_cog(setupcommand(bot))