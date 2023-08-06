from .base import AbstractControlInterface
from ..suite import CommandSuite
from ..client import APIEssentials
from .. import ui
import sqlalchemy
import yaml
from discord import ChannelType
import logging
import aiohttp
import time
import sys
from io import StringIO
import re
import asyncio
import os

PREEMPTIVE_REFRESH_THRESHOLD = 10 * 60 # Start refreshing access tokens 10 minutes before expiry
DEFAULT_GUILD_CONFIG = "{}"

yaml_sanitization_p = re.compile(r"[\"\'>:.@!-#^&\(\)\s]")
def sanitize_suite_command_name(name):
	return yaml_sanitization_p.sub('_', name)

logger = logging.getLogger('beymax.control.webui')

def build_default_control_config(suites):
	return {
			'channels': {},
			'suites': {
				sanitize_suite_command_name(suite.name): {
					'enabled': suite.forced,
					'forced': suite.forced,
					'display_name': suite.name,
					'commands': {
						sanitize_suite_command_name(command['command']): {
							'enabled': False,
							'display_name': command['command']
						}
						for command in suite.commands
					},
					'contexts': {
						sanitize_suite_command_name(context['name']): {
							'enabled': False,
							'display_name': context['name']
						}
						for context in suite.context
					}
				}
				for suite in suites
			}
		}

def get_dependency_list(suites):
	return {
		suitename: deplist
		for suitename, deplist in {
			sanitize_suite_command_name(suite.name): [
				sanitize_suite_command_name(req.name)
				for req in suites
				if suite in req.dependencies
			]
			for suite in suites
		}.items()
		if len(deplist)
	}

WebControlEssentials = CommandSuite("WebUI Shard Essentials", force_enable=True)

@WebControlEssentials.table
class GuildInfo(object):
	"""
	Represents a suite being enabled.
	Forced suites are NOT represented in this database
	"""
	__tablename__ = 'webctrl_guild_config'
	guild_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
	config_yaml = sqlalchemy.Column(sqlalchemy.Text)
	icon_url = sqlalchemy.Column(sqlalchemy.Text)
	name = sqlalchemy.Column(sqlalchemy.String)
	shard = sqlalchemy.Column(sqlalchemy.Integer)

@WebControlEssentials.table
class GuildChannel(object):
	"""
	Represents latest guild channels
	"""
	__tablename__ = 'webctrl_guild_channels'
	guild_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
	channel_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
	channel_type = sqlalchemy.Column(sqlalchemy.Enum(ChannelType))
	name = sqlalchemy.Column(sqlalchemy.String)

@WebControlEssentials.table
class AuditLog(object):
	"""
	Used to store config changes. Used only by the remote, declared here only
	so it becomes accessible to /viewdb
	"""
	__tablename__ = 'webctrl_guild_audit'
	guild_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
	user_id = sqlalchemy.Column(sqlalchemy.BigInteger)
	timestamp = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	event = sqlalchemy.Column(sqlalchemy.String)

@WebControlEssentials.subscribe('guild_channel_delete')
async def on_channel_delete(client, event, channel):
	"""
	Remove guild channels from webUI metadata
	"""
	async with client.db.session() as session:
		await session.execute(
			sqlalchemy.delete(WebControlEssentials.schema.GuildChannel).where(
				(WebControlEssentials.schema.GuildChannel.guild_id == channel.guild.id)
				& (WebControlEssentials.schema.GuildChannel.channel_id == channel.id)
			)
		)
		await session.commit()

@WebControlEssentials.subscribe('guild_channel_create')
async def on_channel_create(client, event, channel):
	"""
	Add guild channels from webUI metadata
	"""
	
	try:
		async with client.db.session() as session:
			session.add(WebControlEssentials.schema.GuildChannel(
				guild_id=channel.guild.id,
				channel_id=channel.id, # Guaranteed by implementation of abc.Snowflake
				channel_type=channel.type, # Guaranteed by concrete channel implementations, which all have type attribute
				name=channel.name
			))
			await session.commit()
	except:
		traceID = await client.trace()
		logger.error(
			"Unable to record channel {} in database, possibly a duplicate entry. See trace {} for details".format(channel.id, traceID),
			exc_info=True
		)

@WebControlEssentials.subscribe('guild_channel_update')
async def on_channel_update(client, event, before_channel, after_channel):
	"""
	Update existing channels in database
	"""
	divert = False
	try:
		async with client.db.session() as session:
			record = (await session.execute(
				sqlalchemy.select(WebControlEssentials.schema.GuildChannel).where(
					(WebControlEssentials.schema.GuildChannel.guild_id == before_channel.guild.id)
					& (WebControlEssentials.schema.GuildChannel.channel_id == before_channel.id)
				)
			)).scalars().first()
			if record is None:
				logger.warning("Failed to update GuildChannel: No channel in database (possibly a rapid update after create), diverting to guild_channel_create")
				divert = True
			else:
				record.channel_type = after_channel.type # Guaranteed by concrete channel implementations, which all have type attribute
				record.name = after_channel.name
				await session.commit()
	except:
		traceID = await client.trace()
		logger.error(
			"Unable to update channel {} in database. See trace {} for details".format(before_channel.id, traceID),
			exc_info=True
		)
	if divert:
		return await on_channel_create(client, event, after_channel)

@WebControlEssentials.subscribe('guild_update')
async def update_guild(client, event, before_guild, after_guild):
	"""
	Updates the guild name/icon/other future metadata in the database.
	"""
	try:
		async with client.db.session() as session:
			record = (await session.execute(
				sqlalchemy.select(WebControlEssentials.schema.GuildInfo).where(
					WebControlEssentials.schema.GuildInfo.guild_id == before_guild.id
				)
			)).scalars().first()
			if record is None:
				return logger.warning("Failed to update GuildInfo for guild {}. No record found -- is the guild in the database or not?".format(before_guild.id))
			record.icon_url = after_guild.icon.url if after_guild.icon is not None else None
			record.name = after_guild.name
			record.shard = client.shard_id
			await session.commit()
	except:
		traceID = await client.trace()
		logger.error(
			"Unable to update metadata for guild {} in database. See trace {} for details".format(before_guild.id, traceID),
			exc_info=True
		)

@WebControlEssentials.subscribe('guild_remove')
async def remove_guild_data(client, event, guild):
	try:
		logger.info("Purging guild data for guild {}".format(guild.id))
		async with client.db.session() as session:
			# This loop will also include the webcontrolessentials tables above
			for suite in client.suites.values():
				for attribute in dir(suite.schema):
					tableobj = getattr(suite.schema, attribute)
					if hasattr(tableobj, "_table_guild_scope") and tableobj._table_guild_scope:
						logger.debug("Removing table {} in guild {}".format(
							tableobj._table_original_name,
							guild.id
						))
						await session.execute(
							sqlalchemy.delete(tableobj).where(
								tableobj.guild_id == guild.id
							)
						)
		await session.commit()
	except:
		traceID = await client.trace()
		logger.error("Unable to purge guild data. Must purge manually. Guild: {}, Trace: {}".format(guild.id, traceID))
			


@WebControlEssentials.subscribe('after:schema') # This must complete before we dispatch command-init
async def initialize_channels(client, event, db):
	"""
	Grab initial guild channels list and ensure database is synchronized.
	Also set guild icon url and name.
	"""
	# Create underlying database schema
	await client.db.connection.run_sync(db.base.metadata.create_all)
	await client.db.connection.commit()
	
	async with client.db.session() as session:
		with session.no_autoflush:

			for guild in client.guilds:
				# For each guild
				# First add/update the core GuildInfo object
				record = (await session.execute(
					sqlalchemy.select(WebControlEssentials.schema.GuildInfo).where(
						WebControlEssentials.schema.GuildInfo.guild_id == guild.id
					)
				)).scalars().first()
				if record is None:
					logger.info("Initializing new guild (joined while offline) {}".format(guild.id))
					await client.controller.guild_consent(guild)
					guild_control = build_default_control_config(client.suites.values()) # Use client.suites to include dependencies
					client.controller.guild_ctrl[guild.id] = guild_control
					session.add(WebControlEssentials.schema.GuildInfo(
						guild_id=guild.id,
						config_yaml=yaml.dump(
							{
								'__ctrl__': guild_control
							},
							None
						),
						icon_url=guild.icon.url if guild.icon is not None else None,
						name=guild.name,
						shard=client.shard_id
					))
				else:
					record.icon_url=guild.icon.url if guild.icon is not None else None
					record.name=guild.name
					record.shard=client.shard_id

					guild_config = yaml.load(record.config_yaml, Loader=yaml.SafeLoader)
					if '__ctrl__' in guild_config:
						client.controller.guild_ctrl[guild.id] = guild_config['__ctrl__']
					else:
						guild_control = build_default_control_config(client.suites.values()) # Use client.suites to include dependencies
						client.controller.guild_ctrl[guild.id] = guild_control
						guild_config['__ctrl__'] = guild_control
						record.config_yaml = yaml.dump(guild_config, None)


				
					# Now delete all channel entries, since this is an existing guild
					await session.execute(
						sqlalchemy.delete(WebControlEssentials.schema.GuildChannel).where(
							WebControlEssentials.schema.GuildChannel.guild_id == guild.id
						)
					)
				
				# Now update all channels
				session.add_all([
					WebControlEssentials.schema.GuildChannel(
						guild_id=guild.id,
						channel_id=channel.id,
						channel_type=channel.type,
						name=channel.name
					)
					for channel in guild.channels
				])

				logger.info("Completed guild initialization for {}".format(guild.id))
		
		await session.commit()

@WebControlEssentials.subscribe('ready', once=True)
async def send_client_id(client, event):
	async with client.controller.http_session.post('{}/metadata/client-id'.format(client.controller.url_base), json={'client_id': client.application_id, 'icon_url': client.user.avatar.url}, headers=(await client.controller.get_auth_headers())) as response:
		if response.status != 200:
			logger.warning("Unable to report client-id to remote ({})".format(response.status))
			


class WebUIControlInterface(AbstractControlInterface):
	"""
	Reference implementation of a webui control interface
	"""

	def __init__(self, pairing_token, url_base, suites, url_suffix='api/shard'):
		super().__init__()
		url_base = url_base.rstrip('/')
		self.__fallback_domain = os.path.basename(url_base)
		self.url_base = '{}/{}'.format(url_base, url_suffix)
		self._command_suites = suites + [WebControlEssentials]
		self.http_session = None
		self.__credentials = {
			'pairing': pairing_token,
			'access': None,
			'refresh': None,
			'expires': None
		}
		self.guild_ctrl = {}
		self.primary_guild = None # This is never updated, webui does not support primary_guild mode
		self.heartbeat_fail_count = 0

	
	async def get_auth_headers(self, token_type='access'):
		"""
		Check if access token is about to expire, or has expired.
		Refresh credentials, if necessary, then return access header
		"""
		if token_type == 'access':
			if self.__credentials['expires'] - time.time() <= PREEMPTIVE_REFRESH_THRESHOLD:
				await self.refresh()
			return {'Authorization': 'Bearer {}'.format(self.__credentials['access'])}
		elif token_type == 'refresh':
			return {'Authorization': 'Bearer refresh-{}'.format(self.__credentials['refresh'])}
		elif token_type == 'pairing':
			return {'Authorization': 'Bearer pairing-{}'.format(self.__credentials['pairing'])}
		raise ValueError("Unknown token type {}".format(token_type))

	async def __aenter__(self):
		"""
		ControlInterface should be used as a context manager
		"""
		# NOTE: The aiohttp docs are ambiguous. If (stupidly) these timeouts are cumulative over the life of the session, then don't do timeouts
		self.http_session = aiohttp.ClientSession(read_timeout=10, conn_timeout=10)
		await self.http_session.__aenter__()
		return self

	async def __aexit__(self, exc_inf, tb, stack):
		"""
		Context exit is a no-op on the base class
		"""
		await self.http_session.__aexit__(None, None, None)
		self.http_session = None

	async def check_start_shard(self, ready_token):
		"""
		This method is responsible for checking if the remote is ready for the shard to start.
		ready_token is whatever the return value from self.ready() was, and can be used in any way.
		This method must return (Any), None, (Any) to indicate that the remote IS NOT ready for the shard
		This method must return (int), (str), (dict) to indicate that the remote IS ready for the shard
		"""
		async with self.http_session.get('{}/start'.format(self.url_base), headers=(await self.get_auth_headers())) as response:
			if response.status != 200:
				logger.warning("Shard recieved error stats from remote when attempting to start: {} : {}".format(response.status, await response.text()))
				return None, None, None

			data = await response.json()

		if not data['start_ok']:
			logger.info('Shard is NOT cleared to start')
			return None, None, None
		
		logger.info('Shard cleared to start')
		return data['shard_id'], data['oauth_token'], data['metadata']

	async def heartbeat(self):
		"""
		This method is responsible for pinging the remote and checking for status updates.
		This will be subscribed to the 'heartbeat' event which is sent every 30 seconds
		This method should take care of any actions needed, as the return value is ignored by the client
		"""
		try:
			async with self.http_session.get('{}/heartbeat/{}'.format(self.url_base, self.client.shard_id), headers=(await self.get_auth_headers())) as response:

				if response.status != 200:
					self.heartbeat_fail_count += 1

					if response.status == 401:
						logger.error("Authentication failure during heartbeat. Adding 2 failures to fail count")
						self.heartbeat_fail_count += 1
					else:
						logger.error("Remote heartbeat failed ({}) : {}".format(response.status, await response.text()))
					
					if self.heartbeat_fail_count >= 5:
						await self.client.shutdown(signal="<remote heartbeat fail>") # Triggers controller halt
					return
				
				data = await response.json()
		except:
			logger.error("Encountered an unhandled exception when making heartbeat connection", exc_info=True)
			self.heartbeat_fail_count += 1
			if self.heartbeat_fail_count >= 5:
				await self.client.shutdown(signal="<remote heartbeat fail>") # Triggers controller halt
			return

		
		self.heartbeat_fail_count = 0 # reset fail count after successful heartbeat

		for guild in data['guilds']:
			self.guild_ctrl[guild['id']] = guild['config']
			logger.info("Updated control configuration for guild {}".format(guild['id']))

	async def config_get(self, guild_id, *keys, default=None):
		"""
		This method is responsible for retrieving a value from config
		"""
		if guild_id is None:
			guild_id == '__global__'
		# First: Check if the given key is present in the guild's control cache (high priority updates delivered over heartbeats)
		if guild_id in self.guild_ctrl and keys[0] in self.guild_ctrl[guild_id]:
			config = self.guild_ctrl[guild_id]
			for key in keys:
				if key in config:
					config = config[key]
				else:
					logger.warning("Guild control keypath {} not defined for guild {}".format(
						'.'.join(str(key) for key in keys),
						guild_id
					))
					return default
			return config
		
		# Second, async: Make a request to the upstream for global config with the given default
		request_data = {
			'keys': [*keys],
			'default': default
		}
		async with self.http_session.post('{}/config'.format(self.url_base), json=request_data, headers=(await self.get_auth_headers())) as response:
			
			# Third, if guild id is not global: Attempt to fetch value form db guild config
			if guild_id != '__global__':
				async with self.client.db.session() as db_session:
					guild_data = (await db_session.execute(
						sqlalchemy.select(WebControlEssentials.schema.GuildInfo).where(
							WebControlEssentials.schema.GuildInfo.guild_id == guild_id
						)
					)).scalars().first()
					if guild_data is not None and guild_data.config_yaml is not None:
						guild_conf = yaml.load(StringIO(guild_data.config_yaml), Loader=yaml.SafeLoader)
						found = True
						for key in keys:
							if key in guild_conf:
								guild_conf = guild_conf[key]
							else:
								found = False
								break
						if found:
							return guild_conf

			if response.status != 200:
				logger.warning("Failed to fetch global config from remote (status {}). Using default".format(response.status))
				return default

			# Finally, return our default, which will either be the given default or the global value found
			return (await response.json())['result']


	async def on_guild_join(self, guild):
		"""
		This method allows the controller to respond to guild_join events.
		The controller may take any actions here (such as leaving the guild to enforce primary_server mode)
		"""
		async with self.client.db.session() as session:
			logger.info("Initializing new guild {}".format(guild.id))
			await self.guild_consent(guild)
			guild_control = build_default_control_config(self.client.suites.values()) # Use client.suites to include dependencies
			self.guild_ctrl[guild.id] = guild_control
			session.add(WebControlEssentials.schema.GuildInfo(
				guild_id=guild.id,
				config_yaml=yaml.dump(
					{
						'__ctrl__': guild_control
					},
					None
				),
				icon_url=guild.icon.url if guild.icon is not None else None,
				name=guild.name,
				shard=self.client.shard_id
			))
			await session.commit()
		
		async with self.http_session.post('{}/guild/join'.format(self.url_base), json={'guild_id': guild.id}, headers=(await self.get_auth_headers())) as response:
			if response.status != 200:
				logger.warning("Received error from remote on guild_join {} : {}".format(response.status, await response.text()))

	def suite_enabled_in_guild(self, suite, guild):
		"""
		This should a boolean indicating if the suite is currently enabled in the guild
		This *MUST* return True for suites where CommandSuite.forced == True
		"""
		if guild is None:
			# DM
			return True
		if len(suite.dependents):
			for dependant in suite.dependents:
				if self.suite_enabled_in_guild(dependant, guild):
					return True
		if guild not in self.client.guilds:
			logger.warning("Guild {} not present in client guild cache. Possibly intercepted an event from a different shard".format(guild.id))
			return False
		if guild.id not in self.guild_ctrl or 'suites' not in self.guild_ctrl[guild.id]:
			# We shouldn't be able to get here, if ready/guild_join/heartbeat are doing their jobs of keeping the cache populated
			logger.error("Guild {} not present in control cache!".format(guild.id))
			return False
		suite_name = sanitize_suite_command_name(suite.name)
		if suite_name in self.guild_ctrl[guild.id]['suites'] and 'enabled' in self.guild_ctrl[guild.id]['suites'][suite_name]:
			return self.guild_ctrl[guild.id]['suites'][suite_name]['enabled']
		logger.error("Suite {} missing from {} guild control, defaulting disabled".format(suite_name, guild.id))
		return False

	def command_enabled_in_guild(self, suite, command, guild):
		"""
		This should a boolean indicating if the command is currently enabled in the guild
		"""
		if not self.suite_enabled_in_guild(suite, guild):
			return False
		if guild is None:
			# DM
			return True
		suite_name = sanitize_suite_command_name(suite.name)
		command_name = sanitize_suite_command_name(command)
		if command_name in self.guild_ctrl[guild.id]['suites'][suite_name]['commands'] and 'enabled' in self.guild_ctrl[guild.id]['suites'][suite_name]['commands'][command_name]:
			return self.guild_ctrl[guild.id]['suites'][suite_name]['commands'][command_name]['enabled']
		logger.error("Command {} missing from {} guild control (suite {}), defaulting disabled".format(command_name, guild.id, suite_name))
		return False
	
	def context_enabled_in_guild(self, suite, context, guild):
		"""
		This should a boolean indicating if the context is currently enabled in the guild
		"""
		if not self.suite_enabled_in_guild(suite, guild):
			return False
		if guild is None:
			# DM
			return True
		suite_name = sanitize_suite_command_name(suite.name)
		context_name = sanitize_suite_command_name(context)
		if context_name in self.guild_ctrl[guild.id]['suites'][suite_name]['contexts'] and 'enabled' in self.guild_ctrl[guild.id]['suites'][suite_name]['contexts'][context_name]:
			return self.guild_ctrl[guild.id]['suites'][suite_name]['contexts'][context_name]['enabled']
		logger.error("context {} missing from {} guild control (suite {}), defaulting disabled".format(context_name, guild.id, suite_name))
		return False

	def add_config_command(self, client):
		"""
		This method is responsible for defining the GLOBAL /config command
		for a shard
		"""
		@client.add_command('config', description='(Administrators only) Configure Beymax for this server')
		async def cmd_config(interaction):
			if interaction.guild_id is None:
				return await interaction.response.send_message(
					"This command cannot be used in DMs",
					ephemeral=True
				)
			elif not interaction.user.guild_permissions.administrator:
				return await interaction.response.send_message(
					'This command can only be used by server administrators.'
					' You must have server-wide administrator permissions (channel-specific administrator permissions do not count).',
					ephemeral=True
				)

			async with self.http_session.post('{}/client-login'.format(self.url_base), json={'user_id': interaction.user.id, 'guild_id': interaction.guild_id}, headers=(await self.get_auth_headers())) as response:

				if response.status != 200:
					traceID = await interaction.client.trace()
					logger.error("Failed to get client login link (trace {}) -- {} : {}".format(
						traceID,
						response.status,
						await response.text()
					))
					return await interaction.response.send_message(
						"The controller responded with an unexpected error. If you continue to encounter"
						" this problem, please make a bug report with the following error trace ID: `{}`".format(
							traceID
						),
						ephemeral=True,
					)
				
				data = await response.json()
			
			view = ui.View()

			# Oops! there's no view.add_button, because I'm stupid
			view.add_item(ui.Button('Configure', callback_or_url=data['login_url']))

			return await interaction.response.send_message(
				"Press this button to open Beymax's configuration page in your browser."
				" This link will only be valid for 10 minutes",
				view=view,
				ephemeral=True,
				delete_after=10 * 60 # JWT redirect lifespan
			)

	@property
	def commandSuites(self):
		"""
		Returns a list of CommandSuite instances that the control interface intends to enable
		These suites will be enabled on created clients.
		It does not mean that these suites have been ACTIVATED in any particular guild
		"""
		return self._command_suites

	async def ready(self):
		"""
		This coroutine should take any local actions needed to prepare,
		and then report itself as ready to the remote. If this method returns
		anything (such as a token or other information received from the remote)
		it is passed to .check_start_shard()
		Relevent logging configuration should take place here
		"""
		auth_data = None
		original_creds = self.__credentials['pairing']
		for attempt in range(5):
			async with self.http_session.get('{}/marco'.format(self.url_base)) as response:
				if response.status != 200:
					logger.warning("Unable to reach remote -- shard may have booted early. Retrying ({} more attempts)".format(4 - attempt))
					await asyncio.sleep(10)
					continue

			if original_creds.startswith('docker-discriminator'):
				_, var = original_creds.split(':')
				async with self.http_session.get('{}/discriminator'.format(self.url_base)) as response:
					if response.status == 502 or response.status == 504:
						logger.warning("Unable to reach remote -- shard may have booted early. Retrying ({} more attempts)".format(4 - attempt))
						await asyncio.sleep(10)
						continue

					if response.status != 200:
						logger.critical("Failed to pair with remote. Cannot recover: {}".format(await response.text()))
						sys.exit(1)

					data = await response.json()
					discriminator = 1 + (data['discriminator'] % data['shard_count'])
					logger.info("Fetching discriminated credential {}".format(discriminator))
					self.__credentials['pairing'] = os.environ['{}_{}'.format(var, discriminator)]

			async with self.http_session.get('{}/auth/pairing'.format(self.url_base), headers=(await self.get_auth_headers('pairing'))) as response:

				if response.status != 200:
					logger.error("Failed to pair with remote. Retrying: {}".format(await response.text()))
					await asyncio.sleep(10)
					continue
					
				auth_data = await response.json()
				break
		
		if auth_data is None:
			logger.critical("Failed to pair with remote. Cannot recover")
			sys.exit(1)
		

		self.__credentials['access'] = auth_data['tokens']['access']
		self.__credentials['refresh'] = auth_data['tokens']['refresh']
		self.__credentials['expires'] = int(response.headers['X-Access-Expires-At'])

		logger.info("Successfully paired with remote")

	async def refresh(self):
		"""
		Refreshes the shard's credentials with the remote
		"""
		async with self.http_session.get('{}/auth/refresh'.format(self.url_base), headers=(await self.get_auth_headers('refresh'))) as response:

			if response.status != 200:
				logger.error("Failed to refresh access token. Authentication may fail in the near future: {}".format(await response.text()))
			else:
				data = await response.json()
				self.__credentials['access'] = data['tokens']['access']
				self.__credentials['refresh'] = data['tokens']['refresh']
				self.__credentials['expires'] = int(response.headers['X-Access-Expires-At'])

				logger.info("Successfully obtained new access and refresh tokens")
	
	async def pre_start(self):
		"""
		Lifecycle hook for any activity that should take place after the client
		has been created, and before the client is started
		"""
		# All shards will run this endpoint, which allows shards to be updated on the fly
		# If there is a production code update, restart all shards and the controller should update
		suite_data = {
			'default_config': build_default_control_config(self.client.suites.values()),
			'suite_list': [
				sanitize_suite_command_name(suite.name)
				for suite in self.client.suites.values()
			],
			'dependencies': get_dependency_list(self.client.suites.values()),
			'channel_refs': [
				*(
					{
						channel
						for suite in self.client.suites.values()
						for channel in suite.channels
					} | {'general'}
				)
			]
		}
		async with self.http_session.post('{}/metadata/suites'.format(self.url_base), json=suite_data, headers=(await self.get_auth_headers())) as response:
			if response.status != 200:
				logger.error("Failed to update suite metadata")
				if self.client.shard_id == 0:
					# If we're the first shard, then this metadata MUST be sent
					await asyncio.sleep(5)
					return await self.pre_start() # Retry
				return
			
			logger.info("Successfully sent suite metadata to the controller")
	
	async def guild_consent(self, guild):
		"""
		Called when joining new guilds. Allows administrators to consent
		"""
		async with self.http_session.get('{}/domain'.format(self.url_base), headers=(await self.get_auth_headers())) as response:
			if response.status != 200:
				logger.error("Unable to fetch remote domain info. Using fallbacks. ({}) : {}".format(response.status, (await response.text())))
				domaininfo = {
					'domain': self.__fallback_domain
				}
			
			else:
				domaininfo = await response.json()
			
		await (await self.client.fetch_channel_reference('general', guild.id)).send(
			"Thanks for the invitation! For security reasons, all my commands will start off disabled."
			" Please read the administrator guide (https://{domain}/setup) and end-user license agreement (https://{domain}/eula)."
			" If you disagree with the EULA, kick me now. If you keep me in the server, I'll assume"
			" you agree with the EULA.".format(
				domain=domaininfo['domain']
			)
		)

