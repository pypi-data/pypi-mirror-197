"""IndieAuth client."""

import web
from twilio.base.exceptions import TwilioException, TwilioRestException
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant, VideoGrant
from twilio.rest import Client

app = web.application(__name__, prefix="live")
twilio_account_sid = app.cfg.get("TWILIO_ACCOUNT_SID")
twilio_api_key_sid = app.cfg.get("TWILIO_API_KEY_SID")
twilio_api_key_secret = app.cfg.get("TWILIO_API_KEY_SECRET")
try:
    twilio_client = Client(
        twilio_api_key_sid, twilio_api_key_secret, twilio_account_sid
    )
except TwilioException:
    twilio_client = None


def get_chatroom(name):
    """Return a room, creating one if necessary."""
    for conversation in twilio_client.conversations.conversations.stream():
        if conversation.friendly_name == name:
            return conversation
    return twilio_client.conversations.conversations.create(friendly_name=name)


@app.control("")
class Live:
    """"""

    def get(self):
        """"""
        return app.view.index()


@app.control("stream")
class Stream:
    """"""

    def get(self):
        """"""
        return app.view.stream()


@app.control("chat")
class Chat:
    """Chat with guests."""

    def get(self):
        """Return a chat room."""
        # if not web.tx.user.session:
        #     raise web.SeeOther("/sign-in")
        return app.view.chat()

    def post(self):
        """Sign user in to chat."""
        username = web.form("username").username
        conversation = get_chatroom("MyRoom")
        try:
            conversation.participants.create(identity=username)
        except TwilioRestException as exc:
            # do not error if the user is already in the conversation
            if exc.status != 409:
                raise
        token = AccessToken(
            twilio_account_sid,
            twilio_api_key_sid,
            twilio_api_key_secret,
            identity=username,
        )
        token.add_grant(VideoGrant(room="MyRoom"))
        token.add_grant(ChatGrant(service_sid=conversation.chat_service_sid))
        return {"token": token.to_jwt(), "conversation_sid": conversation.sid}
