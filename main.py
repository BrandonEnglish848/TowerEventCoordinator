from interactions import slash_command, slash_option, SlashContext, OptionType
import discord
import table_functions as tf
import interactions
from config import *

bot = interactions.Client()

@interactions.listen()
async def on_startup():
	await tf.initialize_tables()

@slash_command(name="get_current_event_id")
async def get_current_event_id(ctx: SlashContext):
	result = await tf.get_current_event_id(ctx.guild.id)
	if result:
		await ctx.send(result)
	else:
		await ctx.send("No Current Event ID.")

@slash_command(name="get_next_team_id")
async def get_next_team_id(ctx: SlashContext):
	# Lookup the current Event ID
	event_id = await tf.get_current_event_id(ctx.guild.id)
	if event_id:
		# Use the current Event ID to find the next Team ID
		await ctx.send(await tf.get_next_team_id_by_event_id(event_id))
	else:
		await ctx.send("No Current Event ID.")

@slash_command(name="initialize")
async def initialize(ctx: SlashContext):
	await ctx.send(await tf.initialize_tables())

@slash_command(name="drop")
async def drop(ctx: SlashContext):
	await ctx.send(await tf.drop_tables())

@slash_command(name="get_teams")
async def get_teams(ctx: SlashContext):
	event_id = await tf.get_current_event_id(ctx.guild.id)
	if event_id:
		result = await tf.get_teams_query(event_id)
		output = result.join("\n")
		await ctx.send(output)

@slash_command(name="create_team")
async def create_team(ctx: SlashContext):
	# Get the current event number
	event_number = await tf.get_current_event_id(ctx.guild.id)

	# Get the next available team number
	team_number = await tf.get_next_team_id_by_event_id(event_number)

	# Get the current guild
	current_guild: discord.Guild = ctx.guild
	# Generate a new role
	role:discord.Role = await current_guild.create_role(name=team_number)
	# Insert Role
	await tf.insert_role(event_number, role.id, role.name)

	# Generate a new category channel
	category:discord.CategoryChannel = await current_guild.create_category_channel(name=team_number)
	# Insert Channel
	await tf.insert_channel(event_number, team_number, category.id, "Category")

	# Set Category Permissions
	await category.set_permissions(target=role, view_channel=True, read_message_history=True, send_messages=True, connect=True, speak=True)
	await category.set_permissions(target=ctx.guild.default_role, view_audit_log=False, view_channel=False, read_message_history=False, connect=False)

	# Create Text Channel
	current_channel = await current_guild.create_text_channel(name=f"text-{role.id}", category=category)
	# Insert Channel
	await tf.insert_channel(event_number, team_number, current_channel.id, "Text")

	# Create Voice Channel
	current_channel = await current_guild.create_voice_channel(name=f"voice-{role.id}", category=category)
	# Insert Channel
	await tf.insert_channel(event_number, team_number, current_channel.id, "Voice")

@slash_command(name="create_admin")
async def create_admin(ctx: SlashContext):
	# Get the current event number
	event_number = await tf.get_current_event_id(ctx.guild.id)

	# Set the current guild
	current_guild:discord.Guild = ctx.guild

	# Create the Admin Role for this Event
	role:discord.Role = await current_guild.create_role(name=f"admin_{event_number}")
	# Insert Role
	await tf.insert_role(event_number, role.id, role.name)

	# Create Admin Category
	category:discord.CategoryChannel = await current_guild.create_category(name=f"admin_channels_{event_number}")
	# Insert Channel
	await tf.insert_channel(event_number, 0, category.id, "Category")

	# Set Category Permissions
	await category.set_permissions(target=role, view_channel=True, read_message_history=True, send_messages=True, connect=True, speak=True)
	await category.set_permissions(target=ctx.guild.default_role, view_audit_log=False, view_channel=False, read_message_history=False, connect=False)

	# Create BotCommand Channel
	current_channel = await current_guild.create_text_channel(name=f"botcommands-{role.id}", category=category)
	# Insert Channel
	await tf.insert_channel(event_number, 0, current_channel.id, "Text")

	# Create Text Channel
	current_channel = await current_guild.create_text_channel(f"text-{role.id}", category=category)
	# Insert Channel
	await tf.insert_channel(event_number, 0, current_channel.id, "Text")

	# Create Voice Channel
	await current_guild.create_voice_channel(f"voice-{role.id}", category=category)
	# Insert Channel
	await tf.insert_channel(event_number, 0, current_channel.id, "Voice")

@slash_command(name="set_admin")
@slash_option(name="member", description="The user to give the admin role", required=True, opt_type=OptionType.USER)
async def set_admin(ctx, member:discord.Member):
	# Get the current event number
	event_number = await tf.get_current_event_id(ctx.guild.id)
	role = await discord.utils.get(ctx.guild.roles, name=f"admin_{event_number}")
	await member.add_roles(role)

bot.start(token)
