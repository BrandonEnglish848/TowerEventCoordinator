initialization_queries = [
	"CREATE SCHEMA IF NOT EXISTS `Tower` DEFAULT CHARACTER SET utf8mb4;",
	"CREATE TABLE IF NOT EXISTS `Blessings` (`BlessingID` BIGINT NOT NULL, `Title` VARCHAR(255), `Description` VARCHAR(255), PRIMARY KEY (`BlessingID`));",
	"CREATE TABLE IF NOT EXISTS `Events` (`EventID` BIGINT NOT NULL, `GuildID` BIGINT NOT NULL, `Active` BOOLEAN DEFAULT TRUE, PRIMARY KEY (`EventID`, `GuildID`));",
	"CREATE TABLE IF NOT EXISTS `EventSettings` (`EventID` BIGINT NOT NULL, `EnableBlessings` BOOLEAN DEFAULT TRUE, `EntryPricePerPerson` BIGINT DEFAULT 2000000, `TeamSizeMinimum` BIGINT DEFAULT 1, `TeamSizeMaximum` BIGINT DEFAULT 3, `StartDate` DATE, `Status` BIGINT DEFAULT 0, PRIMARY KEY (`EventID`));",
	"CREATE TABLE IF NOT EXISTS `Layouts` (`EventID` BIGINT NOT NULL, `FloorID` BIGINT NOT NULL, `RoomID` BIGINT NOT NULL, PRIMARY KEY (`EventID`, `FloorID`, `RoomID`));",
	"CREATE TABLE IF NOT EXISTS `Roles` (`EventID` BIGINT NOT NULL, `RoleID` BIGINT NOT NULL, `RoleName` VARCHAR(255) NOT NULL, PRIMARY KEY (`EventID`, `RoleID`));",
	"CREATE TABLE IF NOT EXISTS `Rooms` (`RoomID` BIGINT NOT NULL, `RoomTitle` VARCHAR(255), `Description` VARCHAR(255), `BlessingsChallengeDescription` VARCHAR(255), PRIMARY KEY (`RoomID`));",
	"CREATE TABLE IF NOT EXISTS `TeamBlessings` (`EventID` BIGINT NOT NULL, `TeamID` BIGINT NOT NULL, `BlessingID` BIGINT NOT NULL, `BlessingCount` BIGINT DEFAULT 1, PRIMARY KEY (`EventID`, `TeamID`, `BlessingID`));",
	"CREATE TABLE IF NOT EXISTS `TeamChannels` (`EventID` BIGINT NOT NULL, `TeamID` BIGINT NOT NULL, `ChannelID` BIGINT NOT NULL, ChannelType VARCHAR(50), PRIMARY KEY (`EventID`, `TeamID`, `ChannelID`));",
	"CREATE TABLE IF NOT EXISTS `TeamMembers` (`EventID` BIGINT NOT NULL, `TeamID` BIGINT NOT NULL, `MemberID` BIGINT NOT NULL, PRIMARY KEY (`EventID`, `TeamID`, `MemberID`));",
	"CREATE TABLE IF NOT EXISTS `Teams` (`EventID` BIGINT NOT NULL, `TeamID` BIGINT NOT NULL, `CategoryID` BIGINT, `RoleID` BIGINT, `CurrentFloor` BIGINT DEFAULT 0, `VisibleFloor` BIGINT DEFAULT 0, PRIMARY KEY (`EventID`, `TeamID`));",
	"CREATE TABLE IF NOT EXISTS `Transactions` (`TransactionID` BIGINT NOT NULL, `EventID` BIGINT NOT NULL, `Amount` BIGINT, `Username` VARCHAR(255), `MemberID` BIGINT, PRIMARY KEY (`TransactionID`));"
]

drop_tables_queries = [
	"DROP TABLE IF EXISTS `Blessings`;",
	"DROP TABLE IF EXISTS `Events`;",
	"DROP TABLE IF EXISTS `EventSettings`;",
	"DROP TABLE IF EXISTS `Layouts`;",
	"DROP TABLE IF EXISTS `Roles`;",
	"DROP TABLE IF EXISTS `Rooms`;",
	"DROP TABLE IF EXISTS `TeamBlessings`;",
	"DROP TABLE IF EXISTS `TeamChannels`;",
	"DROP TABLE IF EXISTS `TeamMembers`;",
	"DROP TABLE IF EXISTS `Teams`;",
	"DROP TABLE IF EXISTS `Transactions`;"
]

insert_channel_query = "INSERT INTO `Tower`.`TeamChannels` (`EventID`, `TeamID`, `ChannelID`, `ChannelType`) VALUES (%(EventID)s, %(TeamID)s, %(ChannelID)s, %(ChannelType)s);"

insert_team_query = "INSERT INTO `Tower`.`Teams` (`EventID`, `TeamID`, `CategoryID`, `RoleID`) VALUES (%(EventID)s, %(TeamID)s, %(CategoryID)s, %(RoleID)s)"

insert_team_member_query = "INSERT INTO `Tower`.`TeamMembers` (`EventID`, `TeamID`, `MemberID`) VALUES (%(EventID)s, %(TeamID)s, %(MemberID)s);"

insert_role_query = "INSERT INTO `Tower`.`Roles` (`EventID`, `RoleID`, `RoleName`) VALUES (%(EventID)s, %(RoleID)s, %(RoleName)s);"

insert_event_query = "INSERT INTO `Tower`.`Events` (`EventID`, `GuildID`) VALUES (%(EventID)s, %(GuildID)s)"

get_current_event_id_query = "SELECT MAX(`EventID`) FROM `Events` WHERE `GuildID` = %(GuildID)s AND `Active` = 1"

get_next_team_id_query = "SELECT MAX(`TeamID`) FROM `Teams` WHERE `EventID` = %(EventID)s"

get_teams_query = "SELECT `Teams`.`TeamID`, `Teams`.`CategoryID`, `Teams`.`RoleID`, `Teams`.`CurrentFloor`, `Teams`.`VisibleFloor` FROM `Tower`.`Teams` WHERE `Teams`.`EventID` = %(EventID)s;"

get_next_event_id_query = "SELECT MAX(`EventID`) FROM `EVENTS`"