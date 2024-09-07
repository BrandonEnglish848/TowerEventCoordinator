import interactions
from interactions import subcommand, listen, slash_option, SlashContext, OptionType, check, is_owner, guild_only

import table_functions as tf
from config import *

# def initialize_memory_storage():
#
#
#

bot = interactions.Client()

@listen()
async def on_startup():
	"""
	# Used for testing purposes
	# Drop all tables
	await tf.drop_tables()
	# Create all tables
	await tf.initialize_tables()
	# Create an active event in the Test server
	await tf.insert_event(test_server_id)
	"""
	await tf.initialize_tables()

@subcommand(name="initialize", base="owner", description="Initialize all of the tables the bot requires.")
@check(is_owner())
@check(guild_only())
async def owner_initialize(ctx: SlashContext):
	await ctx.send(await tf.initialize_tables())

@subcommand(name="drop", base="owner", description="Drop all of the tables the bot requires.")
@check(is_owner())
@check(guild_only())
async def owner_drop(ctx: SlashContext):
	await ctx.send(await tf.drop_tables())

@subcommand(name="team", base="create", description="Create a team")
@slash_option(name="member1", description="The user to assign to the new team", required=False, opt_type=OptionType.USER)
@slash_option(name="member2", description="The user to assign to the new team", required=False, opt_type=OptionType.USER)
@slash_option(name="member3", description="The user to assign to the new team", required=False, opt_type=OptionType.USER)
@check(guild_only())
async def create_team(ctx: SlashContext, member1: interactions.Member, member2:interactions.Member, member3:interactions.Member):
	# Get the current event number
	event_number = await tf.get_current_event_id(ctx.guild.id)

	'''
	Used for testing
	Ensures Event Number is Defined
	if not event_number:
		event_number = 1
	'''

	if event_number:

		""" Create Team """

		# Get the next available team number
		team_number = await tf.get_next_team_id_by_event_id(event_number)

		# Generate a new role using the team number
		role = await ctx.guild.create_role(name=f"tower_{team_number}")
		# Insert Role
		await tf.insert_role(event_number, role.id, role.name)

		# Generate a new category channel
		category = await ctx.guild.create_category(name=f"tower_team_{team_number}")
		# Insert Channel
		await tf.insert_channel(event_number, category.id, "Category")

		# Set Category Permissions
		await category.set_permission(target=role, view_channel=True, read_message_history=True, send_messages=True, connect=True, speak=True, use_application_commands=True)
		await category.set_permission(target=ctx.guild.default_role, view_channel=False, read_message_history=False, connect=False, speak=False, use_application_commands=False)

		# Create Text Channel
		channel = await ctx.guild.create_text_channel(name=f"text_{role.name}", category=category)
		# Insert Channel
		await tf.insert_channel(event_number, channel.id, "Text")

		# Create Voice Channel
		channel = await ctx.guild.create_voice_channel(name=f"voice_{role.name}", category=category)
		# Insert Channel
		await tf.insert_channel(event_number, channel.id, "Voice")

		# Insert Team
		await tf.insert_team(event_number, team_number, category.id, role.id)

		""" Begin Adding Team Members """

		output = []

		# If member is defined, add the role to the specified member.
		if member1:
			if await member1.add_role(role) and await tf.insert_team_member(event_number, team_number, member1.id):
				output.append(f"Member: {member1.username} given team role {role.name}.")
			else:
				output.append(f"Unable to give member: {member1.username} the team role: {role.name}.")
		# If member is defined, add the role to the specified member.
		if member2:
			if await member2.add_role(role) and await tf.insert_team_member(event_number, team_number, member2.id):
				output.append(f"Member: {member2.username} given team role: {role.name}.")
			else:
				output.append(f"Unable to give member: {member2.username} the team role: {role.name}.")
		# If member is defined, add the role to the specified member.
		if member3:
			if await member3.add_role(role) and await tf.insert_team_member(event_number, team_number, member3.id):
				output.append(f"Member: {member3.username} given team role {role.name}.")
			else:
				output.append(f"Unable to give member: {member3.username} the team role: {role.name}.")
		await ctx.send("\n".join(output))

	else:
		await ctx.send("Event has not been created yet. Create one with /create event")

@subcommand(name="admin_role", base="create", description="Create an admin role")
@slash_option(name="member1", description="The user to give the admin role", required=False, opt_type=OptionType.USER)
@slash_option(name="member2", description="The user to give the admin role", required=False, opt_type=OptionType.USER)
@slash_option(name="member3", description="The user to give the admin role", required=False, opt_type=OptionType.USER)
@check(guild_only())
async def create_admin_role(ctx: SlashContext, member1: interactions.Member, member2: interactions.Member, member3: interactions.Member):
	# Get the current event number
	event_number = await tf.get_current_event_id(ctx.guild.id)

	'''
	Used for testing
	Ensures Event Number is Defined
	if not event_number:
		event_number = 1
	'''

	if event_number:
		# Ensure there is not already an admin role for the event.
		role = await tf.get_admin_role_for_event(event_number)
		if not role:
			output = []

			# Create the Admin Role for this Event
			# noinspection PyTypeChecker
			role = await ctx.guild.create_role(name=f"tower_admin_{event_number}", permissions=8)
			# Insert Role
			await tf.insert_role(event_number, role.id, role.name)

			# If member is defined, add the role to the specified member.
			if member1:
				if await member1.add_role(role):
					output.append(f"Member: {member1.username} given admin role {role.name}.")
				else:
					output.append(f"Unable to give member: {member1.username} the admin role: {role.name}.")
			# If member is defined, add the role to the specified member.
			if member2:
				if await member2.add_role(role):
					output.append(f"Member: {member2.username} given admin role: {role.name}.")
				else:
					output.append(f"Unable to give member: {member2.username} the admin role: {role.name}.")
			# If member is defined, add the role to the specified member.
			if member3:
				if await member3.add_role(role):
					output.append(f"Member: {member3.username} given Admin Role {role.name}.")
				else:
					output.append(f"Unable to give member: {member3.username} the admin role: {role.name}.")

			# Create Admin Category
			category = await ctx.guild.create_category(name=f"tower_admin_{event_number}")
			# Insert Channel
			await tf.insert_channel(event_number, category.id, "Category")

			# Set Category Permissions
			await category.set_permission(target=role, view_channel=True, read_message_history=True, send_messages=True, connect=True, speak=True, use_application_commands=True)
			await category.set_permission(target=ctx.guild.default_role, view_channel=False, read_message_history=False, connect=False, speak=False, use_application_commands=False)

			# Create BotCommand Channel
			channel = await ctx.guild.create_text_channel(name=f"botcommands_{role.name}", category=category)
			# Insert Channel
			await tf.insert_channel(event_number, channel.id, "Text")

			# Create Text Channel
			channel = await ctx.guild.create_text_channel(f"text_{role.name}", category=category)
			# Insert Channel
			await tf.insert_channel(event_number, channel.id, "Text")

			# Create Voice Channel
			channel = await ctx.guild.create_voice_channel(f"voice_{role.name}", category=category)
			# Insert Channel
			await tf.insert_channel(event_number, channel.id, "Voice")

			await ctx.send(f"Admin channels created.\n{"\n".join(output)}")
		else:
			await ctx.send("Admin role already exists, try using the /set admin to assign the role to members.")
	else:
		await ctx.send("Event has not been created yet. Create one with /create event")

@subcommand(name="event", base="create", description="Create an event for this server")
@check(guild_only())
async def create_event(ctx: SlashContext):
	result = await tf.insert_event(ctx.guild.id)
	if result:
		await ctx.send(f"Created Event {result}")
	else:
		await ctx.send("Could Not Create Event.")

@subcommand(name="current_event_id", base="get", description="Returns the current event id")
@check(guild_only())
async def get_current_event_id(ctx: SlashContext):
	result = await tf.get_current_event_id(ctx.guild.id)
	if result:
		await ctx.send(result)
	else:
		await ctx.send("No Current Event ID.")

@subcommand(name="next_team_id", base="get", description="Returns the next team id that will be created")
@check(guild_only())
async def get_next_team_id(ctx: SlashContext):
	# Lookup the current Event ID
	event_id = await tf.get_current_event_id(ctx.guild.id)
	if event_id:
		# Use the current Event ID to find the next Team ID
		await ctx.send(await tf.get_next_team_id_by_event_id(event_id))
	else:
		await ctx.send("No events have been created yet. Create one with /create event")

@subcommand(name="teams", base="get", description="Returns the teams in the current event")
@check(guild_only())
async def get_teams(ctx: SlashContext):
	event_number = await tf.get_current_event_id(ctx.guild.id)
	if event_number:
		result = await tf.get_teams_query(event_number)
		output = result.join("\n")
		await ctx.send(output)
	else:
		await ctx.send("Event has not been created yet. Create one with /create event")

@subcommand(name="admin", base="set", description="Assigns the admin role to the member")
@slash_option(name="member1", description="The user to give the admin role", required=False, opt_type=OptionType.USER)
@slash_option(name="member2", description="The user to give the admin role", required=False, opt_type=OptionType.USER)
@slash_option(name="member3", description="The user to give the admin role", required=False, opt_type=OptionType.USER)
@check(guild_only())
async def set_admin(ctx: SlashContext, member1:interactions.Member, member2:interactions.Member, member3:interactions.Member ):
	# Get the current event number
	event_number = await tf.get_current_event_id(ctx.guild.id)
	if event_number and (member1 is not None or member2 is not None or member3 is not None):
		role = interactions.utils.get(ctx.guild.roles, name=f"tower_admin_{event_number}")
		if role is not None:
			output = []

			# If member is defined, add the role to the specified member.
			if member1:
				if await member1.add_role(role):
					output.append(f"Member: {member1.username} given admin role {role.name}.")
				else:
					output.append(f"Unable to give member: {member1.username} the admin role: {role.name}.")
			# If member is defined, add the role to the specified member.
			if member2:
				if await member2.add_role(role):
					output.append(f"Member: {member2.username} given admin role: {role.name}.")
				else:
					output.append(f"Unable to give member: {member2.username} the admin role: {role.name}.")
			# If member is defined, add the role to the specified member.
			if member3:
				if await member3.add_role(role):
					output.append(f"Member: {member3.username} given Admin Role {role.name}.")
				else:
					output.append(f"Unable to give member: {member3.username} the admin role: {role.name}.")
			await ctx.send("\n".join(output))
		else:
			await ctx.send("No Current Admin Role is created. Try using /create admin")
	else:
		await ctx.send("Event has not been created yet. Create one with /create event")

@subcommand(name="team", base="set", description="Returns the teams in the current event")
@slash_option(name="member", description="The user to give the admin role", required=True, opt_type=OptionType.USER)
@slash_option(name="team_id", description="The team to assign the user to", required=True, opt_type=OptionType.INTEGER)
@check(guild_only())
async def set_team(ctx: SlashContext, member:interactions.Member, team_id:int):
	# Get the current event number
	event_number = await tf.get_current_event_id(ctx.guild.id)
	if event_number:
		team = interactions.utils.get(ctx.guild.roles, name=f"tower_team_{team_id}")
		if team:
			if await member.add_role(team):
				# Insert Team Member
				if await tf.insert_team_member(event_number, team_id, member.id):
					await ctx.send(f"Added member: {member.username} to team number {team_id}")
				else:
					await ctx.send(f"Added member: {member.username} to team number {team_id}, but unable to append to tables.")
			else:
				await ctx.send(f"Unable to give member: {member.username} the team role.")
		else:
			await ctx.send("Could not find that Team Number in this server.")
	else:
		await ctx.send("Event has not been created yet. Create one with /create event")


bot.start(token)
