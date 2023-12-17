"""
The _Bot class is a descendant of the Bot class from the aiogram library.
"""

"""
Example:

await bot.send_chat_action(chat_id = message.from_user.id, action = types.ChatActions.TYPING, action_message_id = message.message_id)
await asyncio.sleep(20)
await bot.send_message(chat_id = message.from_user.id, action = types.ChatActions.TYPING, action_message_id = message.message_id, text = "Bot typed!")
"""

from aiogram import types, Bot
from aiogram.types import base
import logging
import asyncio

from typing import Optional
from typing import Union

from utils.helper import get_log_with_id
from utils.helper import get_log

class Bot_(Bot):
	"""
	This class extends the functionality of the base class by adding logging and managing chat actions asynchronously.
	The mechanics of the bot status have also been changed (now the status will remain as long as necessary and can be canceled not by any message,
	but by a special message)

	List of chat actions -> (TYPING, UPLOAD_PHOTO, RECORD_VIDEO, UPLOAD_VIDEO, RECORD_AUDIO, UPLOAD_AUDIO, UPLOAD_DOCUMENT, FIND_LOCATION, RECORD_VIDEO_NOTE, UPLOAD_VIDEO_NOTE)

	:ivar logger: An optional logger for logging purposes.
	:type logger: Optional[logging.handlers]
	:ivar actions: Dict for tasks of actions
	:type actions: Dict[Union[base.Integer, base.String], Dict[str, Any]]
	"""

	def __init__(self, logger: Optional[logging.Logger] = None, *args, **kwargs) -> None:
		"""
		Initializes the _Bot class.

		:param logger: An optional logger for logging purposes.
		:type logger: Optional[logging.Logger]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		"""

		super().__init__(*args, **kwargs)
		self.logger = logger
		self.actions = {}

	async def my_chat_action(self, chat_id: Union[base.Integer, base.String]) -> None:
		"""
		Calls the desired chat_action every 5 seconds if needed

		chat_action can be interrupted either by sending a message with specific content,
		or after 5 seconds

		current = self.actions[chat_id]["items"][-1] -> -1 to display the last chat_action,
		if there are several of them and they are of different types.
		You can set 0 and then they will be displayed in order

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]

		:raise asyncio.CancelledError: If task was cancelled
		:raise KeyError: If task info not found
		"""

		try:
			while chat_id in self.actions.keys() and len(self.actions[chat_id]) != 0:
				current = self.actions[chat_id]["items"][-1]
				await super().send_chat_action(chat_id = chat_id, action = current["action"])
				self.logger.debug(get_log_with_id(id = chat_id, s = '=', text = f"Update chat_action with item: {current} and sleep 5 seconds")) if self.logger else None
				await asyncio.sleep(5)
			self.logger.debug(get_log_with_id(id = chat_id, s = '=', text = "End, because the task was completed")) if self.logger else None
		except asyncio.CancelledError:
			self.logger.debug(get_log_with_id(id = chat_id, s = '=', text = "Cancel  task")) if self.logger else None
		except KeyError as e:
			self.logger.warning(get_log_with_id(id = chat_id, s = '-', text = e)) if self.logger else None

	async def add_chat_action_if_need_it(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None) -> None:
		"""
		Called in self.send_chat_action(...)
		Adds (or creates a queue with the key chat_id and adds) to self.actions chat_action and runs
		in the background self.my_chat_action(...) for a specific chat_id

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: Optional[base.String]
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]	
		"""

		if action_message_id:
			async with asyncio.Lock() as lock:
				if chat_id not in self.actions.keys():
					self.actions[chat_id] = {
						"task": None,
						"items": []
					}
					self.actions[chat_id]["items"] = [
						{
							"action_message_id": action_message_id,
							"action": action
						}
					]
					self.actions[chat_id]["task"] = asyncio.create_task(self.my_chat_action(chat_id = chat_id))
				else:
					item = {
						"action_message_id": action_message_id,
						"action": action
					}

					if item in self.actions[chat_id]["items"]:
						self.actions[chat_id]["items"].remove(item)
					self.actions[chat_id]["items"].append(item)

	async def discard_chat_action_if_need_it(self, chat_id: Union[base.Integer, base.String], action: base.String, action_message_id: Optional[int] = None) -> None:
		"""
		Called in all methods that can interrupt the execution of chat_action
		Removes from self.actions chat_action with the desired action_message_id and action,
		if a message is received with appropriate terminating arguments, or
		restarts self.my_chat_action(...) since chat_action may fail
		because of the message sent

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]

		:raise ValueError: If task the task was deleted
		"""

		async with asyncio.Lock() as lock:
			if chat_id in self.actions.keys() and action and action_message_id:
				try:
					self.actions[chat_id]["items"].remove(
						{
							"action_message_id": action_message_id,
							"action": action
						}
					)
				except ValueError as e:
					self.logger.warning(get_log_with_id(id = chat_id, s = '-', text = e)) if self.logger else None

				self.actions[chat_id]["task"].cancel()
				if len(self.actions[chat_id]["items"]) == 0:
					del self.actions[chat_id]
				else:
					self.actions[chat_id]["task"] = asyncio.create_task(self.my_chat_action(chat_id = chat_id))
			else:
				if chat_id in self.actions.keys():
					self.actions[chat_id]["task"].cancel()
					self.actions[chat_id]["task"] = asyncio.create_task(self.my_chat_action(chat_id = chat_id))

	async def send_chat_action(self, chat_id: Union[base.Integer, base.String], action: base.String, action_message_id: Optional[int] = None, *args, **kwargs) -> Optional[base.Boolean]:
		"""
		Sends a chat action and manages background tasks related to chat actions.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: None if action_message_id is provided, otherwise returns a boolean indicating the success of sending the chat action.
		:rtype: Optional[base.Boolean]
		"""

		await self.add_chat_action_if_need_it(chat_id = chat_id, action_message_id = action_message_id, action = action)
		if not action_message_id:
			self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
			return await super().send_chat_action(chat_id = chat_id, action = action, *args, **kwargs)
		return None

	async def send_message(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with text.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_message(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_photo(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with photo.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""
		result = await super().send_photo(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_audio(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with audio.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_audio(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_document(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with document.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_document(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_video(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with video.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_video(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_animation(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with animation.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_animation(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_voice(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with voice.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_voice(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_video_note(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with video note.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_video_note(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_media_group(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with media group.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_media_group(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_location(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with location.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_location(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_venue(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with venue.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_venue(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_contact(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with contact.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_contact(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_poll(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with poll.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_poll(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_dice(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with dice.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_dice(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_sticker(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with sticker.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_sticker(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_invoice(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with invoice.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_invoice(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def send_game(self, chat_id: Union[base.Integer, base.String], action: Optional[base.String] = None, action_message_id: Optional[int] = None, *args, **kwargs) -> types.Message:
		"""
		Sends a message with game.

		:param chat_id: User's chat_id.
		:type chat_id: Union[base.Integer, base.String]
		:param action: Name of action
		:type action: base.String
		:param action_message_id: Action message's id
		:type action_message_id: Optional[int]
		:param \*args: Arguments
		:type \*args: List[Any]
		:param \*\*kwargs: Key arguments
		:type \*\*kwargs: Dict[str, Any]
		:returns: Info about message
		:rtype: types.Message
		"""

		result = await super().send_game(chat_id = chat_id, *args, **kwargs)
		self.logger.debug(get_log_with_id(id = chat_id, s = '+', text = f"With args: chat_id({chat_id}), action({action}), action_message_id({action_message_id}), *args({args}), **kwargs({kwargs})")) if self.logger else None
		await self.discard_chat_action_if_need_it(chat_id = chat_id, action = action, action_message_id = action_message_id)
		return result

	async def close_tasks(self) -> None:
		"""
		Cancels all tasks in self.actions
		"""

		tasks = [self.actions[key]["task"] for key in self.actions.keys() if self.actions[key]["task"]]

		if tasks:
			for task in tasks:
				task.cancel()
			await asyncio.gather(*tasks)

		self.logger.info(get_log(s = '+', text = "Close all tasks")) if self.logger else None






