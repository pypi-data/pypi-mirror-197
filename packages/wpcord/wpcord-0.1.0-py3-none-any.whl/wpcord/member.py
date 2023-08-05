class Avatar():
    def __init__(self, user_id, id) -> None:
        self.id = id
        self.url = f"https://cdn.discordapp.com/avatars/{user_id}/{self.id}.png?size=1024"
    def __str__(self) -> str:
        return self.url

class Member():
    def __init__(self, guild, data) -> None:
        self.data: dict = data
        self.guild = guild # Guild

        self.id = data["user"]["id"]
        self.username = data["user"]["username"]
        self.discriminator = data["user"]["discriminator"]
        self.nickname = data["nick"] if data["nick"] else self.username
        self.avatar = Avatar(self.id, data["user"]["avatar"])
        self.server_avatar = Avatar(self.id, data["avatar"]) if data["avatar"] else Avatar(self.id, self.avatar.id)
    
    @property
    def mention(self):
        return f"<@{self.id}>"

    @property
    def tag(self):
        return f"{self.username}#{self.discriminator}"

    def __str__(self) -> str:
        return self.tag
    
    def __repr__(self) -> str:
        return self.__str__() # Just for now