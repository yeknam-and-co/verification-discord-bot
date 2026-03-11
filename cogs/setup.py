import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View, ChannelSelect, RoleSelect
from helper.db import add_guild
from helper.verification import verification_message
class SetupView(View):
    def __init__(self, bot): # this initalizes everything and adds itself on
        super().__init__(timeout=None)
        self.selected_channel = None
        self.bot = bot
        self.channel_select = ChannelSelect(
            placeholder="select the verification channel",
            min_values=1,
            max_values=1,
            channel_types=[discord.ChannelType.text],
        )
        self.channel_select.callback = self.on_channel_select # set the what we did to this function
        self.add_item(self.channel_select)

    async def on_channel_select(self, interaction: discord.Interaction): # this runs when the user selects a channel and we move to the roles
        self.selected_channel = self.channel_select.values[0]
        self.clear_items()
        self.role_select = RoleSelect(
            placeholder="select a verified role",
            min_values=1,
            max_values=1,
        )
        self.role_select.callback = self.on_role_select
        self.add_item(self.role_select)
        await interaction.response.edit_message(
            content=f"channel selected: {self.selected_channel.mention}. now select a role.",
            view=self,
        ) # edit the message to show the channel and now we go to the role select

    async def on_role_select(self, interaction: discord.Interaction): # this runs when the user selects a role and we move to the end
        self.selected_role = self.role_select.values[0]
        self.clear_items()
        print("role selected")
        self.staff_channel_select = ChannelSelect(
        placeholder="select a text channel for staff logs",
        min_values=1,
        max_values=1,
        channel_types=[discord.ChannelType.text],
        )
        self.staff_channel_select.callback = self.on_staff_channel_select
        self.add_item(self.staff_channel_select)
        await interaction.response.edit_message(
            content=f"channel selected: {self.selected_channel.mention}. role: {self.selected_role.mention}. now select a channel for staff logs.",
            view=self,
        ) # edit the message to show the channel and now we go to the staff channel select


    async def on_staff_channel_select(self, interaction: discord.Interaction): # this runs when the user selects a staff channel and we are done
        self.selected_staff_channel = self.staff_channel_select.values[0]
        self.clear_items()
        await interaction.response.edit_message(
            content=f"setup complete! {self.selected_channel.mention} and {self.selected_role.mention} and {self.selected_staff_channel.mention} are now set up.",
            view=None,
            embed=None,
        ) # edit the message to show the channel and now we are done

        add_guild(interaction.guild.id, self.selected_channel.id, self.selected_role.id, self.selected_staff_channel.id)
        print("guild added")
        print("calling verifcaiton message")
        await verification_message(interaction, self.bot, self.selected_channel.id)
    

class setupcommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # steal bot from parent class

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self.qualified_name} is loaded.') # debug log to check if the cog is loaded

    @app_commands.command(name="setup", description="setup the bot for ur server, just resetup if you wanna change anything")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def setup(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=SetupView(self.bot)) # send the embed and now we go to the setup view
     
async def setup(bot):
    await bot.add_cog(setupcommand(bot))