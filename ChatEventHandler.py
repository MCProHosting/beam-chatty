"""Handles and formats chat events."""
import requests


class Handler():
    """Handle chat events."""

    def __init__(self, config, chat):
        self.config = config
        self.event_types = {
            "reply": self.type_reply, "event": self.type_event,
            "method": self.type_method, "system": self.type_system}
        self.poll_switch = True
        self.chat = chat

    def formatting(self, data):
        """Check the event type and call the function relating to that type."""
        func = self.event_types[data["type"]]
        func(data)
        if self.config.CHATDEBUG:
            print(data)

    def type_reply(self, data):
        """Handle the Reply type data."""
        if "data" in data:
            if "authenticated" in data["data"]:
                if data["data"]["authenticated"]:
                    print("Authenticated with the server")
                else:
                    print("Authenticated Failed, Chat log restricted")
            else:
                print(f"Server Reply: {str(data)}")
        else:
            print(f"Server Reply: {str(data['error'])}")

    def type_event(self, data):
        """Handle the reply chat event types."""
        s = requests.Session()
        s.headers.update({"Client-ID": self.config.CLIENTID})
        event_string = {
            "WelcomeEvent": "Connected to the channel chat...",
            "UserJoin": "{} has joined the channel.",
            "UserLeave": "{} has left the channel.",
            "ChatMessage": "{user}: {msg}",
            "whisper": "{user} → {target} : {msg}",
            "me": "{user} {msg}",
            "PollStart": "{} has started a poll.",
            "PollEnd": "The poll started by {} has ended.",
            "ClearMessages": "{} has cleared chat.",
            "PurgeMessage": "{modname} has purged {username}'s messages.",
            "SkillAttribution": "{user} used the {skill} skill for {sparks}.",
            "DeleteMessage": "{Mod} deleted a message."}

        if data["event"] == "WelcomeEvent":
            print(event_string[data["event"]])

        elif data["event"] == "UserJoin" or data["event"] == "UserLeave":
            if data["data"]["username"] is not None:
                print(event_string[data["event"]].format(
                    data["data"]["username"]))

        elif data["event"] == "PurgeMessage":
            users_response = s.get("https://mixer.com/api/v1/users/{}".format(
                data["data"]["user_id"])).json()["username"]
            USERNAME = users_response
            if "moderator" in data["data"]:
                mod = data["data"]["moderator"]["user_name"]
                print(f"{mod} has purged {USERNAME}'s messages.")
            else:
                pass

        elif data["event"] == "DeleteMessage":
            # pass
            print(event_string[data["event"]].format(
                Mod=data["data"]["moderator"]["user_name"]))

        elif data["event"] == "ClearMessages":
            print(event_string[data["event"]].format(
                data["data"]["clearer"]["user_name"]))

        elif data["event"] == "PollStart":
            if self.poll_switch:
                print(event_string[data["event"]].format(
                    data["data"]["author"]["user_name"]))
                self.poll_switch = False

        elif data["event"] == "PollEnd":
            print(event_string[data["event"]].format(
                data["data"]["author"]["user_name"]))
            self.poll_switch = True

        elif data["event"] == "SkillAttribution":
            user = data["data"]["user_name"]
            skill = data["data"]["skill"]["skill_name"]
            sparks = data["data"]["skill"]["cost"]
            print(event_string["SkillAttribution"].format(
                user=user,
                skill=skill,
                sparks=sparks))

        elif data["event"] == "ChatMessage":
            msg = "".join(
                item["text"] for item in data["data"]["message"]["message"])
            if "whisper" in data["data"]["message"]["meta"]:
                print(event_string["whisper"].format(
                    user=data["data"]["user_name"],
                    target=data["data"]["target"],
                    msg=msg))

            elif "me" in data["data"]["message"]["meta"]:
                print(event_string["me"].format(
                    user=data["data"]["user_name"],
                    msg=msg))
            else:
                print(event_string[data["event"]].format(
                    user=data["data"]["user_name"],
                    msg=msg))
                if msg == "!ping":
                    self.chat.message("Its ping pong time")

    def type_method(self, data):
        """Handle the reply chat event types."""
        if self.config.CHATDEBUG:
            if data["method"] == "auth":
                print("Authenticating with the server...")

            elif data["method"] == "msg":
                if self.config.CHATDEBUG:
                    print(f"METHOD MSG: {str(data)}")
            else:
                print(f"METHOD MSG: {str(data)}")

    def type_system(self, data):
        """Handle the reply chat event types."""
        if self.config.CHATDEBUG:
            print(f"SYSTEM MSG: {str(data['data'])}")
