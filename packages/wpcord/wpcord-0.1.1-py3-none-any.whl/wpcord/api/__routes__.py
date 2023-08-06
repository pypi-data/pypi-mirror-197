from ..enums import WPCordEnum
from ..http import HTTPMethod

class APIRoute:
    def __init__(self, method: HTTPMethod, path: str, **params) -> None:
        if isinstance(method, str):
            method = HTTPMethod.from_value(method.upper())
        self.method: HTTPMethod = method
        self.path = path.format(**params)

class APIRoutes(WPCordEnum):
    @property
    def method(self) -> HTTPMethod:
        return HTTPMethod.from_value(self.value[0])
    
    @property
    def path(self) -> str:
        return self.value[1]

    def __str__(self) -> str:
        return self.path

    def __call__(self, **parameters) -> APIRoute:
        return APIRoute(*self.value, **parameters)

        

    # Application commands
    # --------------------
    get_global_application_command            = "GET",    "/applications/{application_id}/commands"
    create_global_application_command         = "POST",   "/applications/{application_id}/commands"
    delete_global_application_command         = "DELETE", "/applications/{application_id}/commands"
    bulk_overwrite_global_application_command = "PUT",    "/applications/{application_id}/commands"

    get_guild_application_command             = "GET",    "/applications/{application_id}/guilds/{guild_id}/commands"
    create_guild_application_command          = "POST",   "/applications/{application_id}/guilds/{guild_id}/commands"
    delete_guild_application_command          = "DELETE", "/applications/{application_id}/guilds/{guild_id}/commands"
    bulk_overwrite_guild_application_command  = "PUT",    "/applications/{application_id}/guilds/{guild_id}/commands"

    get_guild_application_command_permissions = "GET",    "/applications/{application_id}/guilds/{guild_id}/commands/permissions"
    get_application_command_permissions       = "GET",    "/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions"
    edit_application_command_permissions      = "PUT",    "/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions"

    # Receiving and responding
    # ------------------------
    create_interaction_response               = "POST",   "/interactions/{interaction_id}/{interaction_token}/callback"

    get_original_interaction_response         = "GET",    "/webhooks/{interaction_id}/{interaction_token}/messages/@original"
    edit_original_interaction_response        = "PATCH",  "/webhooks/{interaction_id}/{interaction_token}/messages/@original"
    delete_original_interaction_response      = "DELETE", "/webhooks/{interaction_id}/{interaction_token}/messages/@original"

    # Channel
    # -------
    get_channel                               = "GET",    "/channels/{channel_id}"
    modify_channel                            = "PATCH",  "/channels/{channel_id}"
    # /messages
    create_message                            = "POST",   "/channels/{channel_id}/messages"
    edit_message                              = "PATCH",  "/channels/{channel_id}/messages/{message_id}"
    delete_message                            = "DELETE", "/channels/{channel_id}/messages/{message_id}"

    # Guild
    # -----
    create_guild                              = "POST",   "/guilds"
    get_guild                                 = "GET",    "/guilds/{guild_id}"
    modify_guild                              = "PATCH",  "/guilds/{guild_id}"
    delete_guild                              = "DELETE", "/guilds/{guild_id}"
    # /preview
    get_guild_preview                         = "GET",    "/guilds/{guild_id}/preview"
    # /channels
    get_guild_channels                        = "GET",    "/guilds/{guild_id}/channels"
    create_guild_channels                     = "POST",   "/guilds/{guild_id}/channels"
    modify_guild_channel_positions            = "PATCH",  "/guilds/{guild_id}/channels"
    # /threads
    list_active_guild_threads                 = "GET",    "/guilds/{guild_id}/threads/active"
    # /members
    get_guild_member                          = "GET",    "/guilds/{guild_id}/members/{user_id}"
    search_guild_member                       = "GET",    "/guilds/{guild_id}/members/search"
    add_guild_member                          = "PUT",    "/guilds/{guild_id}/members/{user_id}"
    modify_guild_member                       = "PATCH",  "/guilds/{guild_id}/members/{user_id}"
    modify_current_member                     = "PATCH",  "/guilds/{guild_id}/members/@me"
    modify_current_user_nick                  = "PATCH",  "/guilds/{guild_id}/members/@me/nick"
    add_guild_member_role                     = "PUT",    "/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
    remove_guild_member_role                  = "DELETE", "/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
    remove_guild_member                       = "DELETE", "/guilds/{guild_id}/members/{user_id}"
    # /bans
    get_guild_bans                            = "GET",    "/guilds/{guild_id}/bans"
    get_guild_ban                             = "GET",    "/guilds/{guild_id}/bans/{user_id}"
    create_guild_ban                          = "PUT",    "/guilds/{guild_id}/bans/{user_id}"
    remove_guild_ban                          = "DELETE", "/guilds/{guild_id}/bans/{user_id}"
    # /roles
    get_guild_roles                           = "GET",    "/guilds/{guild_id}/roles"
    create_guild_role                         = "POST",   "/guilds/{guild_id}/roles"
    modify_guild_role_positions               = "PATCH",  "/guilds/{guild_id}/roles"
    modify_guild_role                         = "PATCH",  "/guilds/{guild_id}/roles/{role_id}"
    # /mfa
    modify_guild_mfa_level                    = "POST",   "/guilds/{guild_id}/mfa"
    # /prune
    get_guild_prune_count                     = "GET",    "/guilds/{guild_id}/prune"
    begin_guild_prune                         = "POST",   "/guilds/{guild_id}/prune"
    # /regions
    get_guild_voice_regions                   = "GET",    "/guilds/{guild_id}/regions"
    # /invites
    get_guild_invites                         = "GET",    "/guilds/{guild_id}/invites"
    # /regions
    get_guild_integrations                    = "GET",    "/guilds/{guild_id}/integrations"
    delete_guild_integrations                 = "DELETE", "/guilds/{guild_id}/integrations"
    # /widget
    get_guild_widget_settings                 = "GET",    "/guilds/{guild_id}/widget"
    modify_guild_widget_settings              = "PATCH",  "/guilds/{guild_id}/widget"
    get_guild_widget                          = "GET",    "/guilds/{guild_id}/widget.json"
    get_guild_widget_image                    = "GET",    "/guilds/{guild_id}/widget.png"
    # /vanity-url
    get_guild_vanity_url                      = "GET",    "/guilds/{guild_id}/vanity-url"
    # /welcome-screen
    get_guild_welcome_screen                  = "GET",    "/guilds/{guild_id}/welcome-screen"
    modify_guild_welcome_screen               = "PATCH",  "/guilds/{guild_id}/welcome-screen"
    # /voice-states
    modify_current_user_voice_state           = "PATCH",  "/guilds/{guild_id}/voice-states/@me"
    modify_user_voice_state                   = "PATCH",  "/guilds/{guild_id}/voice-states/{user_id}"
    
    # Stickers
    # --------
    get_guild_stickers                        = "GET",    "/guilds/{guild_id}/stickers"

    # User
    # ----
    get_current_user                          = "GET",    "/users/@me"
    get_user                                  = "GET",    "/users/{user_id}"
    modify_current_user                       = "PATCH",  "/users/@me"
    # /guilds
    get_current_user_guilds                   = "GET",    "/users/@me/guilds"
    get_current_user_guild_member             = "GET",    "/users/@me/guilds/{guild_id}/member"
    leave_guild                               = "DELETE", "/users/@me/guilds/{guild_id}"
    # /channels
    create_dm                                 = "POST",   "/users/@me/channels"
    # /connections
    get_user_connections                      = "GET",    "/users/@me/connections"

    # Gateway
    # -------
    get_gateway                               = "GET",    "/gateway"
    get_gateway_bot                           = "GET",    "/gateway/bot"