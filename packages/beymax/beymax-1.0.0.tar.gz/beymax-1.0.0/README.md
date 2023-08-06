# Beymax API

A high-level, functional-focused wrapper to [discord.py](https://discordpy.readthedocs.io/en/stable/)

## About

This package started off as a personal discord bot, but as it grew in scope, I found the need to add my own utilities
on top of the wonderful [discord.py](https://discordpy.readthedocs.io/en/stable/) by GitHub user Rapptz.
Beymax aims to reduce the amount of boilerplate needed to create a functioning Discord bot, while also exposing
an API which is familiar to those used to writing event-driven code.

## Differences from discord.py

* Essentially _everything_ runs as an event listener. This includes tasks, commands, and context menus
	* Events now have 3 phases: For an event called `event`, subscribers to `before:event` are run first, then `event`, and finally `after:event`.
	* Events can be cancelled: Any listener to an event can call `event.cancel()` which will prevent any listeners in subsequent phases from being invoked.
	It does abort any listeners which have already ben called, such as other listeners to the current phase
* Client differences:
	* Events can be scheduled in the future with `Client.dispatch_future()`. This adds an entry to the database, so the scheduled event will persist through restarts.
	`.dispatch_future()` guarantees precision within at least 30s of the scheduled time.
	* Key-value storage: Reduces boilerplate for storing/retreiving arbitrary small data points. `Client.set_value()` and `Client.get_value()` can be used to
	store & retreive small strings from the database
	* Database migrations: `Client.migration()` allows schema migrations to be added in code. Migrations are called only the first time the bot starts up after
	a new migration is added.
	* Special message handlers: A small convenience layer over `Client.wait_for()`, `Client.add_special()` allows a coroutine to be invoked any time a message
	is received which meets user-defined criteria
	* Native database integration: Beymax natively supports [SQLAlchemy](https://www.sqlalchemy.org/) for interacting with databases in your bot.
* Cogs -> Suites: discord.py's concept of a `cog` is essentially the same as a Beymax `suite`. Suites group together a set of commands, context menus, event listeners, database tables, etc which logically relate to each other. Suites can define their own interdependencies, ensuring that if a suite is loaded by your bot, all of its dependencies are also loaded.
* UI Differences: discord.py's ui library follows an imperative style, where UI elements are defined in advance via subclassing. Beymax overrides this interface to provide a functionally-oriented style where UI elements are defined dynamically at runtime using function decorators.
* Argument parsing and command definition: Beymax mostly follows discord.py's style of defining command/context arguments via function annotations. Beymax extends this
by allowing all argument metadata to be set in the annotations, including parameter descriptions.

