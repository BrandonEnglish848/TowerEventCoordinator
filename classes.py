import table_functions as tf

class TowerEvent:
	def __init__(self, event_id, guild_id):
		self.event_id:int = event_id
		self.guild_id:int = guild_id
		self.admin_role:int|None = None
		self.admins:[] = []
		self.teams:[Team] = []
		self.roles = []
		self.channels = []
		self.settings = {}

	async def check_teams(self):
		if await self.setup_blank_teams():
			if await self.setup_team_members():
				if await self.setup_team_role():
					return True
				else:
					return False
			else:
				return False
		else:
			return False

	async def setup_blank_teams(self):
		# Query for all teams associated with this event_id
		teams = await tf.get_teams(self.event_id)
		# If there are results, append a Team object for each result
		if teams:
			for result in teams:
				# Make a new Team object
				current_team = Team(result[0])
				# Store it
				self.teams.append(current_team)
			else:
				return True
		else:
			return False

	async def setup_team_members(self):
		# Get each Team object, and fill in its member data
		for team in self.teams:
			members = await tf.get_team_members(self.event_id, team.team_id)
			if members:
				for member in members:
					self.teams[team].members.append(member[0])
		else:
			return True

	async def setup_team_role(self):
		for team in self.teams:
			role = await tf.get_team_role(self.event_id, team.team_id)
			if role:
				self.teams[team].role = role
		else:
			return True


	# def init_admin(self):

	# def init_roles(self):

class Team:
	def __init__(self, team_id):
		self.team_id:int = team_id
		self.members:[int] = []
		self.role:int|None = None
		self.category:int|None = None