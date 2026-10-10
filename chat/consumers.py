import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from .models import Conversation, Message


class GroupChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_id = str(self.scope["url_route"]["kwargs"]["room_id"])
        self.group_name = f"group_{self.room_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "user.join_chat",
                "username": self.user.username
            }
        )

    async def disconnect(self, code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "user.left_chat",
                    "username": self.user.username
                }
            )
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except (json.JSONDecodeError, TypeError):
            return

        action = data.get("action")

        # Deleted Chat
        if action == "delete":
            message_id = data.get("message_id")
            if not message_id:
                return

            deleted = await self.delete_message(self.user, message_id)

            if deleted:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "message.deleted",
                        "message_id": str(message_id),
                    }
                )
            return

        # Edit Chat
        if action == "edit":
            message_id = data.get("message_id")
            new_text = data.get("new_text")
            edited = await self.edit_message(self.user, message_id, new_text)

            if edited:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type":"message.edited",
                        "message_id":message_id,
                        "new_text":new_text
                    }
                )
            return

        message = data.get("message", "").strip()
        if not message:
            return

        # Save Chat to DB
        saved_message = await self.save_message(self.user, self.room_id, message)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "username": self.user.username,
                "message": saved_message.content,
                "created_at": saved_message.created.isoformat(),
                "user_id": str(self.user.id),
                "message_id": str(saved_message.id),  
            }
        )

    # ======================== send methods ===========================
    async def user_join_chat(self, event):
        await self.send(text_data=json.dumps({
            "reason": "user_join",
            "username": event["username"]
        }))

    async def user_left_chat(self, event):
        await self.send(text_data=json.dumps({
            "reason": "user_left",
            "username": event["username"]
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "username": event["username"],
            "message": event["message"],
            "created_at": event["created_at"],
            "user_id": event["user_id"],
            "message_id": event.get("message_id"), 
        }))

    async def message_deleted(self, event):
        await self.send(text_data=json.dumps({
            "reason": "message_deleted",
            "message_id": event["message_id"],
        }))

    async def message_edited(self, event):
        await self.send(
            text_data=json.dumps({
                "message_id":event["message_id"],
                "new_text":event["new_text"],
                "reason":"message_edited"
            })
        )

    # ======================== DB Helper method ===========================
    @database_sync_to_async
    def edit_message(self, user, message_id, new_text): 
        try:
            message = Message.objects.get(
                id=message_id,
                user=user,
            )
            message.content = new_text
            message.save()
            return True
        except Message.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, user, conversation_id, content):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        return Message.objects.create(
            user=user,
            conversation=conversation,
            content=content
        )

    @database_sync_to_async
    def delete_message(self, user, message_id):  
        try:
            message = get_object_or_404(Message, user = user, id = message_id)
            message.delete()
            return True
        except Message.DoesNotExist:
            return False


class PrivatChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.group_name = f"conversation_{self.conversation_id}"

        conversation = await self.get_conversation(self.conversation_id)
        if not conversation:
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        

    async def disconnect(self, code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            

    async def receive(self, text_data = None, bytes_data = None):
        try:
            data = json.loads(text_data)
        except (json.JSONDecodeError, TypeError):
            return 

        action = data.get("action")

        # Deleted chat
        if action == "delete":
            message_id = data.get("message_id")
            deleted = await self.delete_chat(self.user, self.conversation_id, message_id)

            if deleted:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type":"chat.deleted",
                        "message_id":message_id
                    }
                )
            return

        #  Edit chat
        if action == "edit":
            message_id = data.get("message_id")
            new_text = data.get("new_text")
            edited = await self.edit_chat(self.user, self.conversation_id, message_id, new_text)

            if edited:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type":"chat.edited",
                        "message_id":message_id,
                        "new_text":new_text,
                    }
                )
            return

        # Save chat to DB
        message = data.get("message", "").strip()
        if not message:
            return

        saved_message = await self.save_message(self.user, self.conversation_id, message)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type":"chat.message",
                "username":saved_message.user.username,
                "user_id":str(saved_message.user.id),
                "message":saved_message.content,
                "message_id":str(saved_message.id),
                "created_at": saved_message.created.isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps({
                "reason":"chat_message",
                "username":event["username"],
                "user_id":event["user_id"],
                "message":event["message"],
                "message_id":event["message_id"],
                "created_at":event["created_at"],
            })
        )

    async def chat_deleted(self, event):
        await self.send(
            text_data=json.dumps({
                "reason":"chat_deleted",
                "message_id":event["message_id"]
            })
        )

    async def chat_edited(self, event):
            await self.send(
                text_data=json.dumps({
                    "reason":"chat_edited",
                    "message_id":event["message_id"],
                    "new_text":event["new_text"],
                })
            )

    @database_sync_to_async
    def get_conversation(self, conversation_id):
        return Conversation.objects.filter(type="privat", conversations__user = self.user, id = conversation_id).exists()

    @database_sync_to_async
    def save_message(self, user, conversation_id, content):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        return Message.objects.create(
            user = user, 
            conversation = conversation,
            content = content
        )

    @database_sync_to_async
    def delete_chat(self, user, conversation_id, message_id):
        try:
            conversation = get_object_or_404(Conversation, id = conversation_id)
            message = Message.objects.get(
                user=user,
                conversation=conversation,
                id=message_id
            )

            if message:
                message.delete()
                return True
            
        except Message.DoesNotExist:
            return False

    @database_sync_to_async
    def edit_chat(self, user, conversation_id, message_id, new_text):
        try:
            conversation = get_object_or_404(Conversation, id = conversation_id)
            message = Message.objects.get(
                user=user,
                conversation=conversation,
                id=message_id
            )

            if message:
                message.content = new_text
                message.save()
                return True
        except Message.DoesNotExist:
            return False
        
                
        