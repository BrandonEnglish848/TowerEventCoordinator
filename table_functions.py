import mysql.connector
from queries import *
from config import *

mydb = mysql.connector.connect(**mysql_config)

async def drop_tables():
	mycursor = mydb.cursor()
	for i in drop_tables_queries:
		mycursor.execute(i)
	else:
		mycursor.close()
		print("All Tables Dropped.")
		return "All Tables Dropped."

async def initialize_tables():
	await drop_tables()
	mycursor = mydb.cursor()
	for i in initialization_queries:
		mycursor.execute(i)
	else:
		# This will automatically create an active event in the Test server
		await insert_event(test_server_id)

		mycursor.close()
		print("All Tables Checked.")
		return "All Tables Checked."

async def insert_event(guild_number: int):
	mycursor = mydb.cursor()
	event_number = await get_next_event_id()
	mycursor.execute(
		operation=insert_event_query,
		params={'EventID': event_number,'GuildID': guild_number}
	)
	mydb.commit()
	mycursor.close()

async def get_next_event_id():
	mycursor = mydb.cursor()
	mycursor.execute(
		operation=get_next_event_id_query
	)
	myresult = mycursor.fetchone()
	mycursor.close()

	if myresult and myresult[0]:
		return myresult[0] + 1
	else:
		return 1

async def get_next_team_id_by_event_id(event_number: int):
	mycursor = mydb.cursor()
	mycursor.execute(
		operation=get_next_team_id_query,
		params={'EventID': event_number}
	)
	myresult = mycursor.fetchone()
	mycursor.close()

	if myresult and myresult[0]:
		return myresult[0] + 1
	else:
		return 1

async def get_current_event_id(guild_number: int):
	mycursor = mydb.cursor()
	mycursor.execute(
		operation=get_current_event_id_query,
		params={'GuildID': guild_number}
	)
	myresult = mycursor.fetchone()
	mycursor.close()

	if myresult and myresult[0]:
		return myresult[0]
	else:
		return False

async def get_teams(event_number: int):
	mycursor = mydb.cursor()
	mycursor.execute(
		operation=get_teams_query,
		params={'EventID': event_number}
	)
	results = mycursor.fetchall()
	mycursor.close()

	return results

async def get_admin_role_for_event(event_number: int):
	mycursor = mydb.cursor()
	mycursor.execute(
		operation=get_admin_role_query,
		params={
			'EventID': event_number,
			'RoleName': f"admin_{event_number}"
		}
	)
	results = mycursor.fetchone()
	mycursor.close()

	return results

async def insert_team(event_number: int, team_number: int, channel_number: int, channel_type):
	mycursor = mydb.cursor()
	mycursor.execute(
		operation=insert_team_query,
		params={
			'EventID': event_number,
			'TeamID': team_number,
			'ChannelID': channel_number,
			'ChannelType': channel_type
		}
	)
	mydb.commit()
	mycursor.close()

async def insert_team_member(event_number: int, team_number: int, member_number: int):
	mycursor = mydb.cursor()
	mycursor.execute(
		operation=insert_team_member_query,
		params={
			'EventID': event_number,
			'TeamID': team_number,
			'MemberID': member_number
		}
	)
	mydb.commit()
	mycursor.close()

async def insert_channel(event_number: int, channel_number: int, channel_type):
	mycursor = mydb.cursor()
	mycursor.execute(
		operation=insert_channel_query,
		params={
			'EventID': event_number,
			'ChannelID': channel_number,
			'ChannelType': channel_type
		}
	)
	mydb.commit()
	mycursor.close()

async def insert_role(event_number: int, role_number: int, role_name: str):
	mycursor = mydb.cursor()
	mycursor.execute(
		operation=insert_role_query,
		params={
			'EventID': event_number,
			'RoleID': role_number,
			'RoleName': role_name
		}
	)
	mydb.commit()
	mycursor.close()