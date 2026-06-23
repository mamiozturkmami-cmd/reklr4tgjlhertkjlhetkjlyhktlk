import discord
from discord.ext import commands
from discord import app_commands
import io
import os
import logging
import datetime
import asyncio
import requests  
import base64  
from typing import Optional, List, Dict, Any, Union

# ========================================================================
# 1. ENTERPRISE LEVEL CONFIGURATION AND SETTINGS (Railway/VPS Ready)
# ========================================================================
TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")
PASTEBIN_API_KEY: str = os.getenv("PASTEBIN_API_KEY", "SNxRUbS82pBG5qmSW6AeCkmG7nhJhFB1")
PASTEBIN_URL: str = "https://pastebin.com/api/api_post.php"

# Static Global System Configurations
SYSTEM_VERSION: str = "4.5.0-PRO"
INFRASTRUCTURE_NAME: str = "Sleeping Bot Services"
MAX_BULK_ATTACHMENTS: int = 10

# ========================================================================
# 2. ADVANCED LOGGING AND AUDIT SYSTEM IMPLEMENTATION
# ========================================================================
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

# File Handler for permanent server logs
file_handler = logging.FileHandler(filename='discord_bot.log', encoding='utf-8', mode='w')
file_formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Console Handler for real-time diagnostics monitoring
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# ========================================================================
# 3. CORE EMBED DESIGN UTILITY FACTORY
# ========================================================================
class EnterpriseEmbedFactory:
    """
    High-performance embed generator ensuring uniform professional themes
    across all functional components of the client architecture.
    """
    @staticmethod
    def build(
        title: str, 
        description: str, 
        color: discord.Color = discord.Color.blue(),
        ctx_bot: Optional[commands.Bot] = None
    ) -> discord.Embed:
        """Constructs a standardized secure enterprise operational embed framework."""
        embed = discord.Embed(
            title=title, 
            description=description, 
            color=color, 
            timestamp=discord.utils.utcnow()
        )
        
        footer_icon = None
        if ctx_bot and ctx_bot.user and ctx_bot.user.display_avatar:
            footer_icon = ctx_bot.user.display_avatar.url
            
        embed.set_footer(
            text=f"{INFRASTRUCTURE_NAME} | Secure Distribution Pipeline v{SYSTEM_VERSION}", 
            icon_url=footer_icon
        )
        return embed

# ========================================================================
# 4. BOT CLIENT ARCHITECTURE AND INTERACTION ENGINE
# ========================================================================
class ProDiscordBot(commands.Bot):
    """
    Main advanced framework representing the asynchronous Discord Application Gateway
    with automated tree synchronization algorithms.
    """
    def __init__(self) -> None:
        # Initializing intensive privileged gateway intents
        intents: discord.Intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.invites = True  
        intents.guilds = True
        
        super().__init__(
            command_prefix="!", 
            intents=intents,
            help_command=None
        )
        # Safe memory cache allocations for operations
        self.welcome_channels: Dict[int, int] = {}  
        self.invites: Dict[int, List[discord.Invite]] = {}           

    async def setup_hook(self) -> None:
        """
        Asynchronous gateway execution hook designed to register persistent views 
        before the network connection routine fully locks.
        """
        logger.info("Executing operational boot logic... Initializing system views.")
        try:
            self.add_view(VerifyBoosterView())
            logger.info("Persistent System View successfully bound: VerifyBoosterView")
            self.add_view(TicketSetupView())
            logger.info("Persistent System View successfully bound: TicketSetupView")
            self.add_view(TicketActionView())
            logger.info("Persistent System View successfully bound: TicketActionView")
        except Exception as view_error:
            logger.critical(f"Fatal vulnerability discovered during persistent view assembly: {view_error}")

    async def on_ready(self) -> None:
        """
        Event listener fired immediately when the client gateway finishes synchronization
        and achieves fully authorized operational status.
        """
        logger.info("=" * 60)
        logger.info(f"AUTHORIZED SYSTEM CONNECTION ACTIVE")
        logger.info(f"Target Agent Identity: {self.user} (Internal Identifier: {self.user.id})")
        logger.info(f"Framework Engineering Level: {SYSTEM_VERSION}")
        logger.info("=" * 60)
        
        # Deploying global slash command architecture parameters across the Discord Tree API
        try:
            logger.info("Initiating global synchronization sequence on application tree context...")
            synced_commands = await self.tree.sync()
            logger.info(f"Success! Registered `{len(synced_commands)}` global slash interactions into the gateway.")
            for cmd in synced_commands:
                logger.info(f"Successfully Synced Node Command: /{cmd.name}")
        except discord.Forbidden:
            logger.critical("[SYNC-FAILURE] Bot application lacks the critical 'applications.commands' scope in invite permissions!")
        except Exception as sync_exception:
            logger.error(f"[SYNC-ERROR] Unexpected behavior during context tree replication: {sync_exception}")
        
        # Populate operational cache indices with guild invitation manifests
        logger.info("Rebuilding invitation manifest cache registries for active guilds...")
        for guild in self.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
                logger.info(f"Cached {len(self.invites[guild.id])} validation pathways for Guild ID: {guild.id}")
            except discord.Forbidden:
                self.invites[guild.id] = []
                logger.warning(f"Lacking invite tracking permissions for Guild ID: {guild.id}")
            except Exception as e:
                logger.error(f"Failed to fetch invite manifest for guild mapping loop: {e}")
        
        # Establish dynamic rich presence matrix data configuration
        system_activity = discord.Activity(
            type=discord.ActivityType.watching, 
            name="the Server and Commands | v" + SYSTEM_VERSION
        )
        await self.change_presence(status=discord.Status.online, activity=system_activity)
        logger.info("System operational visibility flags successfully pushed to production.")

    async def on_invite_create(self, invite: discord.Invite) -> None:
        """Tracks the creation of network entry pathways to ensure high precision invite tracking metrics."""
        if invite.guild.id not in self.invites:
            self.invites[invite.guild.id] = []
        self.invites[invite.guild.id].append(invite)
        logger.info(f"[INVITE-LOG] New network invitation vector generated: Code {invite.code} on Guild {invite.guild.id}")

    async def on_invite_delete(self, invite: discord.Invite) -> None:
        """Maintains local ledger sanity by purging expired or destroyed network access records."""
        if invite.guild.id in self.invites:
            self.invites[invite.guild.id] = [i for i in self.invites[invite.guild.id] if i.code != invite.code]
            logger.info(f"[INVITE-LOG] Invitation vector removed from memory structures: Code {invite.code}")

    async def on_member_join(self, member: discord.Member) -> None:
        """
        Triggers automatically when an external entity authenticates into a synchronized guild cluster.
        Utilizes algorithmic cache differential auditing to identify the inviting operator.
        """
        welcome_channel_id: Optional[int] = self.welcome_channels.get(member.guild.id)
        if not welcome_channel_id:
            return
            
        channel = member.guild.get_channel(welcome_channel_id)
        if not channel:
            return
            
        inviter_str: str = "Unknown/Direct Access"
        try:
            invites_before: List[discord.Invite] = self.invites.get(member.guild.id, [])
            invites_after: List[discord.Invite] = await member.guild.invites()
            self.invites[member.guild.id] = invites_after
            
            for invite_b in invites_before:
                for invite_a in invites_after:
                    if invite_b.code == invite_a.code and invite_a.uses > invite_b.uses:
                        if invite_a.inviter:
                            inviter_str = invite_a.inviter.mention
                        break
        except Exception as entry_parse_error:
            logger.error(f"[TRACK-CRITICAL] Automated entry validation algorithm crashed: {entry_parse_error}")
            
        welcome_msg: str = f"Hey {member.mention}, welcome to **{member.guild.name}**! 🎉 You were invited to our community by {inviter_str}."
        try:
            await channel.send(welcome_msg)
            logger.info(f"[WELCOME-DISPATCH] Success greeting routed for user {member.id}")
        except Exception as dispatch_failure:
            logger.error(f"Failed to submit welcome message payload allocation: {dispatch_failure}")

# Instantiate the active framework allocation unit
bot = ProDiscordBot()

# ========================================================================
# 5. PERSISTENT SYSTEM COMPONENTS AND HELPER VIEWS
# ========================================================================
class PasteLinkView(discord.ui.View):
    """Generates explicit UI components tracking remote text storage assets."""
    def __init__(self, url: str) -> None:
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="🌐 Open Link (Proxy)", url=url, style=discord.ButtonStyle.link))

class VerifyBoosterView(discord.ui.View):
    """Persistent framework button view dedicated to validating cross-server premium nitro boost telemetry data."""
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Verify Booster Status", style=discord.ButtonStyle.success, custom_id="verify_booster_button_pro")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        # System architecture hardcoded criteria matrices
        MAIN_GUILD_ID: int = 1473684484976148594
        MAIN_BOOSTER_ROLE_ID: int = 1517453584541679627
        TARGET_BOOSTER_ROLE_ID: int = 1518972492004331590
        
        await interaction.response.defer(ephemeral=True)
        
        main_guild: Optional[discord.Guild] = interaction.client.get_guild(MAIN_GUILD_ID)
        if not main_guild:
            await interaction.followup.send("❌ The main server operations core could not be reached or resolved.", ephemeral=True)
            return

        member_in_main: Optional[discord.Member] = main_guild.get_member(interaction.user.id)
        if not member_in_main:
            try:
                member_in_main = await main_guild.fetch_member(interaction.user.id)
            except Exception:
                await interaction.followup.send("❌ **Verification Failed!** You must be an authenticated member of our Main Server to query premium telemetry.", ephemeral=True)
                return

        has_booster: bool = any(role.id == MAIN_BOOSTER_ROLE_ID for role in member_in_main.roles)
        if not has_booster:
            await interaction.followup.send("❌ **Verification Failed!** You do not actively possess the Server Booster designation role in the primary cluster.", ephemeral=True)
            return

        target_guild: discord.Guild = interaction.guild
        target_role: Optional[discord.Role] = target_guild.get_role(TARGET_BOOSTER_ROLE_ID)
        if not target_role:
            await interaction.followup.send("❌ **System Error:** Sync designation role structure does not exist in this environment topology.", ephemeral=True)
            return

        if target_role in interaction.user.roles:
            await interaction.followup.send("ℹ️ Network Sync Engine Reports: You have already been successfully verified and provisioned!", ephemeral=True)
            return

        try:
            await interaction.user.add_roles(target_role)
            await interaction.followup.send("✅ **Verification Successful!** Main Server Premium Boost telemetry status synchronized. Role granted.", ephemeral=True)
            logger.info(f"[PREMIUM-SYNC] Synchronized booster role assignment for user: {interaction.user.id}")
        except Exception as role_err:
            await interaction.followup.send(f"❌ Critical error during role payload deployment execution: {role_err}", ephemeral=True)

# ========================================================================
# 6. ADVANCED COGNITIVE TICKETING MANAGEMENT CORE ENGINE
# ========================================================================
TICKET_LOG_CHANNEL_ID: int = 1518977494068498653
TICKET_STAFF_ROLE_ID: int = 1473685173655830677

class TicketDropdown(discord.ui.Select):
    """
    Cognitive processing multi-choice drop menu designed to route private 
    support workspace containers into specified network structural departments.
    """
    def __init__(self) -> None:
        options: List[discord.SelectOption] = [
            discord.SelectOption(label="Support", description="If you have any issues.", emoji="🛠️", value="Support Tickets"),
            discord.SelectOption(label="Partnership", description="If you wanna do partnership/ads for ads.", emoji="🤝", value="Partnership Tickets"),
            discord.SelectOption(label="Invite Rewards", description="If you invited people and waiting your invite rewards.", emoji="💳", value="Reward Tickets"),
            discord.SelectOption(label="Report Clowns", description="Report scammers.", emoji="🚫", value="Report Tickets")
        ]
        super().__init__(
            placeholder="Select a secure inquiry management category...", 
            min_values=1, 
            max_values=1, 
            options=options, 
            custom_id="ticket_routing_dropdown_pro"
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        """Asynchronous execution mapping sequence creating secure dedicated workspaces on interaction demand."""
        await interaction.response.defer(ephemeral=True)
        guild: discord.Guild = interaction.guild
        member: discord.User = interaction.user
        category_name: str = self.values[0]

        # Anti-Spam protection: audit active workspaces to locate pre-existing channel allocations
        sanitized_username: str = member.name.lower().replace(" ", "-")
        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{sanitized_username}")
        if existing_channel:
            await interaction.followup.send(f"❌ **Blocked:** High density pipeline error. You already have an active workspace initialized: {existing_channel.mention}", ephemeral=True)
            return

        # Target category allocation routing algorithm
        target_category: Optional[discord.CategoryChannel] = discord.utils.get(guild.categories, name=category_name)
        if not target_category:
            try:
                target_category = await guild.create_category(name=category_name)
                logger.info(f"[STRUCTURE-ENGINE] Created missing category array placeholder: {category_name}")
            except discord.Forbidden:
                await interaction.followup.send("❌ High priority permissions fault: Bot application lacks 'Manage Channels' flag configuration.", ephemeral=True)
                return

        staff_role: Optional[discord.Role] = guild.get_role(TICKET_STAFF_ROLE_ID)
        
        # Build multi-layered military grade security access control permission overwrite configurations
        permissions_matrix: Dict[Union[discord.Role, discord.Member], discord.PermissionOverwrite] = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True, view_channel=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True, manage_channels=True, view_channel=True)
        }
        
        if staff_role:
            permissions_matrix[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True, view_channel=True, read_message_history=True)

        try:
            ticket_channel = await guild.create_text_channel(
                name=f"ticket-{member.name}",
                category=target_category,
                overwrites=permissions_matrix,
                topic=f"Owner: {member.id} | Department: {category_name} | Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )

            welcome_embed = discord.Embed(
                title=f"🎫 Secure Workspace Initialized: {category_name}",
                description=(
                    f"Hello {member.mention}, your private isolated network channel has been provisioned.\n\n"
                    f"**Assigned Sector Department:** `{category_name}`\n"
                    "Please state the comprehensive variables of your issue below. Management operators will evaluate your dataset shortly.\n\n"
                    "**Workspace Control Systems Triggers:**\n"
                    "🔒 **Close:** Revokes access rights from user.\n"
                    "📝 **Transcript:** Compiles complete communication logging historical buffers.\n"
                    "🗑️ **Delete:** Instantly terminates current operational workspace."
                ),
                color=discord.Color.brand_green(),
                timestamp=discord.utils.utcnow()
            )
            welcome_embed.set_footer(text="Automated Workspace Routing Systems Infrastructure", icon_url=interaction.client.user.display_avatar.url)
            
            staff_ping: str = f"{member.mention} | {staff_role.mention}" if staff_role else member.mention
            await ticket_channel.send(content=staff_ping, embed=welcome_embed, view=TicketActionView())
            await interaction.followup.send(f"✅ Your secure {category_name} workspace environment is compiled: {ticket_channel.mention}", ephemeral=True)
            logger.info(f"[TICKET-CREATE] Member {member} initialized infrastructure workspace sequence on channel {ticket_channel.id}")

        except Exception as build_err:
            logger.error(f"Critical error failing workspace initialization routines: {build_err}")
            await interaction.followup.send(f"❌ Core kernel processing architecture failed to compile text node channel: {build_err}", ephemeral=True)

class TicketSetupView(discord.ui.View):
    """Persistent component structural framework that houses administrative dropdown selectors."""
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())

class TicketActionView(discord.ui.View):
    """The localized operational command control console loaded inside active ticket environments."""
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close Workspace", style=discord.ButtonStyle.secondary, custom_id="close_ticket_button_pro")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """Evicts user access allocations while retaining records for audit procedures."""
        await interaction.response.defer()
        channel: discord.TextChannel = interaction.channel
        
        channel_topic: str = channel.topic or ""
        extracted_member_id: Optional[int] = None
        if "Owner:" in channel_topic:
            try:
                extracted_member_id = int(channel_topic.split("|")[0].split(":")[1].strip())
            except Exception:
                logger.warning("Failed parsing member identity strings out of ticket topic string formats.")

        if extracted_member_id:
            resolved_member = interaction.guild.get_member(extracted_member_id)
            if resolved_member:
                await channel.set_permissions(resolved_member, overwrite=None)
                logger.info(f"[TICKET-CLOSE] Evicted permissions visibility from owner {resolved_member.id} in {channel.id}")
        
        await channel.send("🔒 **Ticket Isolation Sequence Complete.** Channel permissions locked out. Authorized staff can now generate transcripts or execute deletion routines.")

    @discord.ui.button(label="📝 Export Transcript", style=discord.ButtonStyle.primary, custom_id="transcript_ticket_button_pro")
    async def transcript_ticket(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """Dumps internal text history arrays directly into secure administrative central logging rooms."""
        await interaction.response.defer(ephemeral=True)
        channel: discord.TextChannel = interaction.channel
        master_log_channel = interaction.client.get_channel(TICKET_LOG_CHANNEL_ID)

        if not master_log_channel:
            await interaction.followup.send("❌ Master administration data logs drop endpoint channel missing or inaccessible.", ephemeral=True)
            return

        await interaction.followup.send("📝 Compiling complete text historical data parameters. Export routine parsing initialized...", ephemeral=True)

        history_buffer: str = f"--- SECURE LOG TRANSACTION REPORT MANIFEST: {channel.name} ---\n"
        history_buffer += f"Export Event Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        history_buffer += f"Executing Agent Signature: {interaction.user} (ID: {interaction.user.id})\n"
        history_buffer += "========================================================================\n\n"

        async for historical_message in channel.history(limit=None, oldest_first=True):
            timestamp_prefix: str = historical_message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            history_buffer += f"[{timestamp_prefix}] {historical_message.author} ({historical_message.author.id}): {historical_message.content}\n"
            if historical_message.attachments:
                for attachment_node in historical_message.attachments:
                    history_buffer += f" > [Media Asset Trapped]: {attachment_node.url}\n"

        binary_file_payload = io.BytesIO(history_buffer.encode("utf-8"))
        exportable_file = discord.File(fp=binary_file_payload, filename=f"transcript-manifest-{channel.name}.txt")

        reporting_embed = discord.Embed(
            title="📝 Centralized Ticket Audit Manifest Exported",
            description=f"**Target Workspace Identifier Tag:** `{channel.name}`\n**Auditing Officer Profile:** {interaction.user.mention}\n**Compilation State:** Complete secure file matrix synchronization successful.",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        reporting_embed.set_footer(text="Internal Compliance Records System Log Engine")
        
        await master_log_channel.send(embed=reporting_embed, file=exportable_file)
        await interaction.followup.send("✅ Document data archive file package exported to internal central logging repository!", ephemeral=True)

    @discord.ui.button(label="🗑️ Delete Workspace", style=discord.ButtonStyle.danger, custom_id="delete_ticket_button_pro")
    async def delete_ticket(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """Permanently obliterates the active channel workspace context."""
        logger.info(f"[TICKET-DESTRUCTION] Channel deletion routine invoked on target node: {interaction.channel.id}")
        await interaction.response.send_message("🗑️ High level infrastructure deletion script initialized. Channel context self destruct sequence active. Purging workspace in 5 seconds...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

# ========================================================================
# 7. EXPLICIT GLOBAL ROUTING ERROR INTERCEPTION SYSTEMS
# ========================================================================
@bot.tree.error
async def on_app_command_error_handler(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
    """Intercepts errors occurring during interaction pipelines, rendering meaningful security messages."""
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"⏳ Rate limit triggered! Please slow down operational demand. Re-evaluate interaction in `{error.retry_after:.2f}` seconds.", ephemeral=True)
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Security Fault: You do not possess the necessary application administrative privileges to issue this pipeline request.", ephemeral=True)
    else:
        logger.error(f"[COMMAND-CORE-ERROR] Unhandled exception occurred inside execution tree: {error}")
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(f"❌ Internal system core execution fault mapped: `{error}`", ephemeral=True)
        except Exception:
            pass

# ========================================================================
# 8. COMPREHENSIVE PRODUCTION SLASH COMMAND APPLICATION ENVIRONMENT
# ========================================================================

# Global reusable selection structures
CHOICES_PING_MATRIX = [
    app_commands.Choice(name="Yes, mention @everyone", value="yes"),
    app_commands.Choice(name="No, do not mention", value="no")
]

CHOICES_SENDER_MATRIX = [
    app_commands.Choice(name="Yes", value="yes"), 
    app_commands.Choice(name="No", value="no")
]

CHOICES_PASTEBIN_EXPIRATION = [
    app_commands.Choice(name="10 Minutes", value="10M"),
    app_commands.Choice(name="1 Hour", value="1H"),
    app_commands.Choice(name="1 Day", value="1D"),
    app_commands.Choice(name="1 Week", value="1W"),
    app_commands.Choice(name="1 Month", value="1M"),
    app_commands.Choice(name="1 Year", value="1Y"),
    app_commands.Choice(name="Never", value="N")
]

# ------------------------------------------------------------------------
# COMMAND 1: /send (Target Message Forwarding Matrix Layout)
# ------------------------------------------------------------------------
@bot.tree.command(name="send", description="Sends the desired text string straight to the designated target channel infrastructure node.")
@app_commands.choices(show_sender=CHOICES_SENDER_MATRIX, ping_everyone=CHOICES_PING_MATRIX)
@app_commands.describe(channel="Target channel to distribute text payload to", message="String parameters representing text block payload", picture="Optional attachment asset", show_sender="Toggle user stamp visibility", ping_everyone="Toggle server wide notifications")
async def send_cmd(
    interaction: discord.Interaction, 
    channel: discord.TextChannel, 
    message: str, 
    picture: Optional[discord.Attachment] = None, 
    show_sender: str = "no", 
    ping_everyone: str = "no"
) -> None:
    await interaction.response.defer(ephemeral=True)
    if not channel: 
        return
        
    content_pieces: List[str] = [f"{message}\n\n*👤 Sender Cryptographic Signature: {interaction.user.mention}*" if show_sender == "yes" else message]
    finalized_payload_content: str = ("@everyone\n" if ping_everyone == "yes" else "") + "\n".join(content_pieces)
    
    files_to_send: List[discord.File] = []
    if picture:
        files_to_send.append(await picture.to_file())
        
    try:
        if files_to_send:
            await channel.send(content=finalized_payload_content, files=files_to_send)
        else:
            await channel.send(content=finalized_payload_content)
        await interaction.followup.send(embed=EnterpriseEmbedFactory.build("✅ Payload Delivered", f"Text block successful packet transmission routed into channel {channel.mention}.", discord.Color.green(), bot))
    except Exception as e:
        await interaction.followup.send(f"❌ Core distribution node failed processing request: {e}")

# ------------------------------------------------------------------------
# COMMAND 2: /txt (Asynchronous Local File Parameter Assembler)
# ------------------------------------------------------------------------
@bot.tree.command(name="txt", description="Converts input text parameters directly into a downloadable flat text format .txt document asset.")
@app_commands.choices(ping_everyone=CHOICES_PING_MATRIX)
@app_commands.describe(file_name="Target title designation for output file asset", content="Complete body values of text string data", message="Additional text context to output with the embed frame", picture="Optional static image file attachment link", ping_everyone="Toggle priority notifications alert")
async def txt_cmd(
    interaction: discord.Interaction, 
    file_name: str, 
    content: str, 
    message: Optional[str] = None, 
    picture: Optional[discord.Attachment] = None, 
    ping_everyone: str = "no"
) -> None:
    await interaction.response.defer(ephemeral=True)
    sanitized_filename: str = file_name.replace(" ", "_")
    if not sanitized_filename.endswith(".txt"):
        sanitized_filename += ".txt"
        
    raw_document_bytes = io.BytesIO(content.encode("utf-8"))
    response_embed = EnterpriseEmbedFactory.build("📄 Document Pipeline Compilation Success", f"File object artifact labeled: **`{sanitized_filename}`** structured completely.", discord.Color.gold(), bot)
    
    if message: 
        response_embed.add_field(name="💬 Operational Context Notes", value=message, inline=False)
    if picture: 
        response_embed.set_image(url=picture.url)
        
    try: 
        await interaction.followup.send(
            content="@everyone" if ping_everyone == "yes" else None, 
            embed=response_embed, 
            file=discord.File(fp=raw_document_bytes, filename=sanitized_filename)
        )
    except Exception as e: 
        await interaction.followup.send(f"❌ Critical transmission collapse on binary delivery stream: {e}")

# ------------------------------------------------------------------------
# COMMAND 3: /sendtxt (Asynchronous Channel File Distribution Routing)
# ------------------------------------------------------------------------
@bot.tree.command(name="sendtxt", description="Transforms raw string characters into a physical file layout and pushes it to an absolute target channel destination.")
@app_commands.choices(show_sender=CHOICES_SENDER_MATRIX, ping_everyone=CHOICES_PING_MATRIX)
@app_commands.describe(channel="Target channel vector allocation space", file_name="Designated metadata file title assignment name", content="String parameters to parse into file block array formats", message="Secondary informational notes context text field value", picture="Optional layout tracking photo asset", show_sender="Render profile identification parameters", ping_everyone="Toggle server notification ping triggers")
async def sendtxt_cmd(
    interaction: discord.Interaction, 
    channel: discord.TextChannel, 
    file_name: str, 
    content: str, 
    message: Optional[str] = None, 
    picture: Optional[discord.Attachment] = None, 
    show_sender: str = "no", 
    ping_everyone: str = "no"
) -> None:
    await interaction.response.defer(ephemeral=True)
    sanitized_filename: str = file_name.replace(" ", "_")
    if not sanitized_filename.endswith(".txt"):
        sanitized_filename += ".txt"
        
    tracking_embed = discord.Embed(title="📁 Transmitted File Document Pipeline Pushed", color=discord.Color.dark_theme(), timestamp=discord.utils.utcnow())
    if show_sender == "yes": 
        tracking_embed.add_field(name="Origin Operator Profile Signature", value=interaction.user.mention, inline=False)
    tracking_embed.add_field(name="System Metadata Matrix Label", value=f"`{sanitized_filename}`", inline=False)
    
    if message: 
        tracking_embed.add_field(name="💬 Operator Log Notes Context", value=message, inline=False)
    if picture:
        tracking_embed.set_image(url=picture.url)
        
    raw_text_data_stream = io.BytesIO(content.encode("utf-8"))
    try:
        await channel.send(
            content="@everyone" if ping_everyone == "yes" else None, 
            embed=tracking_embed, 
            file=discord.File(fp=raw_text_data_stream, filename=sanitized_filename)
        )
        await interaction.followup.send(f"✅ Text conversion distribution completed onto node: {channel.mention}")
    except Exception as e: 
        await interaction.followup.send(f"❌ Security or processing failure during channel deployment cycle: {e}")

# ------------------------------------------------------------------------
# COMMAND 4: /modifytxt (Asynchronous Linear Text Stream Compactor)
# ------------------------------------------------------------------------
@bot.tree.command(name="modifytxt", description="Flattens all vertical newline string parameters into a uniform horizontal compressed character layout block.")
@app_commands.choices(show_sender=CHOICES_SENDER_MATRIX, ping_everyone=CHOICES_PING_MATRIX)
@app_commands.describe(channel="Destination text platform channel location mapping", file_name="Output string asset file validation title", content="Highly structured text values broken down by line arrays", message="Additional data notes parameter context block strings", picture="Optional graphic presentation asset", show_sender="Render user ID attributes", ping_everyone="Trigger system priority alert pings")
async def modifytxt_cmd(
    interaction: discord.Interaction, 
    channel: discord.TextChannel, 
    file_name: str, 
    content: str, 
    message: Optional[str] = None, 
    picture: Optional[discord.Attachment] = None, 
    show_sender: str = "no", 
    ping_everyone: str = "no"
) -> None:
    await interaction.response.defer(ephemeral=True)
    sanitized_filename: str = file_name.replace(" ", "_")
    if not sanitized_filename.endswith(".txt"):
        sanitized_filename += ".txt"
        
    flattened_content: str = " ".join([line.strip() for line in content.splitlines() if line.strip()])
    document_stream_buffer = io.BytesIO(flattened_content.encode("utf-8"))
    
    reporting_embed = discord.Embed(title="📁 Flattened Horizontally Modified Document Transported", color=discord.Color.orange(), timestamp=discord.utils.utcnow())
    if message: 
        reporting_embed.add_field(name="💬 Data Structural Changes Memo", value=message, inline=False)
    if show_sender == "yes":
        reporting_embed.add_field(name="Authorized Compiler Profile Token", value=interaction.user.mention, inline=False)
    if picture:
        reporting_embed.set_image(url=picture.url)
        
    try:
        await channel.send(
            content="@everyone" if ping_everyone == "yes" else None, 
            embed=reporting_embed, 
            file=discord.File(fp=document_stream_buffer, filename=sanitized_filename)
        )
        await interaction.followup.send(f"✅ Modified text asset data streams deployed completely to {channel.mention}.")
    except Exception as e: 
        await interaction.followup.send(f"❌ Processing failure inside linear compression arrays: {e}")

# ------------------------------------------------------------------------
# COMMAND 5: /sendmytxt (Asynchronous Local File Interceptor and Router)
# ------------------------------------------------------------------------
@bot.tree.command(name="sendmytxt", description="Reads an uploaded local text document from your client, clones it, and routes it to target nodes.")
@app_commands.choices(ping_everyone=CHOICES_PING_MATRIX)
@app_commands.describe(channel="Target channel vector framework space", file="Local attachment file asset to process", message="Optional annotation documentation script information", picture="Optional design frame graphical image asset", ping_everyone="Toggle mention pings alert matrices")
async def sendmytxt_cmd(
    interaction: discord.Interaction, 
    channel: discord.TextChannel, 
    file: discord.Attachment, 
    message: Optional[str] = None, 
    picture: Optional[discord.Attachment] = None, 
    ping_everyone: str = "no"
) -> None:
    await interaction.response.defer(ephemeral=True)
    if not file.filename.lower().endswith('.txt'):
        await interaction.followup.send("❌ Data Validation Error: Input target attachment structural orientation must explicitly be `.txt` file format.")
        return
        
    try:
        retrieved_file_byte_array = io.BytesIO(await file.read())
        forwarding_embed = discord.Embed(title="📥 Local File Asset Intercepted & Forwarded Successfully", color=discord.Color.purple(), timestamp=discord.utils.utcnow())
        
        if message: 
            forwarding_embed.add_field(name="💬 Operational Payload Manifest Notes", value=message, inline=False)
        if picture:
            forwarding_embed.set_image(url=picture.url)
            
        await channel.send(
            content="@everyone" if ping_everyone == "yes" else None, 
            embed=forwarding_embed, 
            file=discord.File(fp=retrieved_file_byte_array, filename=file.filename)
        )
        await interaction.followup.send(f"✅ Text package clone routine deployed target sequence execution on channel: {channel.mention}")
    except Exception as e: 
        await interaction.followup.send(f"❌ Buffer extraction algorithm failed reading source dataset attachment object: {e}")

# ------------------------------------------------------------------------
# COMMAND 6: /sendmyfile (Asynchronous Universal File Processing Core Vector)
# ------------------------------------------------------------------------
@bot.tree.command(name="sendmyfile", description="Accepts and routes any generic binary file format layout across network channels cleanly.")
@app_commands.choices(ping_everyone=CHOICES_PING_MATRIX)
@app_commands.describe(channel="Destination text platform layout framework location mapping", file="Any complex binary data matrix package file attachment", message="Informational content script notes block", picture="Secondary graphic presentation link template item", ping_everyone="Execute global call notification pings mapping parameters")
async def sendmyfile_cmd(
    interaction: discord.Interaction, 
    channel: discord.TextChannel, 
    file: discord.Attachment, 
    message: Optional[str] = None, 
    picture: Optional[discord.Attachment] = None, 
    ping_everyone: str = "no"
) -> None:
    await interaction.response.defer(ephemeral=True)
    try:
        extracted_binary_buffer = io.BytesIO(await file.read())
        generic_package_embed = discord.Embed(title="📦 High Density Binary Data Package Received", color=discord.Color.teal(), timestamp=discord.utils.utcnow())
        
        if message: 
            generic_package_embed.add_field(name="💬 Data Payload Registry Annotation Log", value=message, inline=False)
        if picture:
            generic_package_embed.set_image(url=picture.url)
            
        await channel.send(
            content="@everyone" if ping_everyone == "yes" else None, 
            embed=generic_package_embed, 
            file=discord.File(fp=extracted_binary_buffer, filename=file.filename)
        )
        await interaction.followup.send(f"✅ Generic file asset payload array deployed successfully into targeted room: {channel.mention}")
    except Exception as e: 
        await interaction.followup.send(f"❌ Binary transport system interface error: {e}")

# ------------------------------------------------------------------------
# COMMAND 7: /paste (Asynchronous Remote Cloud Database Document Syncer)
# ------------------------------------------------------------------------
@bot.tree.command(name="paste", description="Uploads comprehensive raw text data packages directly into secure external web storage (Pastebin).")
@app_commands.choices(expiration=CHOICES_PASTEBIN_EXPIRATION, ping_everyone=CHOICES_PING_MATRIX)
@app_commands.describe(channel="Target channel for link display asset deployment", content="Comprehensive body layout text structures to save remotely", title="Title classification indexing record name", expiration="Data preservation lifespan parameters selection matrix", message="Context documentation notes narrative statement", picture="Optional illustration asset image link")
async def paste_cmd(
    interaction: discord.Interaction, 
    channel: discord.TextChannel, 
    content: str, 
    title: Optional[str] = "Untitled Paste Infrastructure Record", 
    expiration: str = "N", 
    message: Optional[str] = None, 
    picture: Optional[discord.Attachment] = None, 
    ping_everyone: str = "no"
) -> None:
    await interaction.response.defer(ephemeral=True)
    api_request_payload = {
        "api_dev_key": PASTEBIN_API_KEY, 
        "api_option": "paste", 
        "api_paste_code": content, 
        "api_paste_name": title, 
        "api_paste_expire_date": expiration, 
        "api_paste_private": "0"
    }
    try:
        http_response = await asyncio.to_thread(requests.post, PASTEBIN_URL, data=api_request_payload, timeout=12)
        if http_response.status_code == 200 and "pastebin.com" in http_response.text:
            proxy_url: str = http_response.text.strip().replace("pastebin.com", "pastebinp.com")
            
            notification_embed = discord.Embed(
                title="🎉 Cloud Repository Synchronization Successful!", 
                description=f"Raw text parameters parsed and secured onto external servers storage arrays.\n\n**Generated Document Direct Access Link Index:**\n`{proxy_url}`",
                color=discord.Color.blue(), 
                timestamp=discord.utils.utcnow()
            )
            if message:
                notification_embed.add_field(name="💬 Cloud Transaction Documentation Memo", value=message, inline=False)
            if picture:
                notification_embed.set_image(url=picture.url)
                
            await channel.send(content="@everyone" if ping_everyone == "yes" else None, embed=notification_embed, view=PasteLinkView(url=proxy_url))
            await interaction.followup.send(f"✅ Remote URL compiled and distributed onto network platform nodes: {proxy_url}")
        else: 
            await interaction.followup.send(f"❌ External service gateway rejected code block structures: `{http_response.text}`")
    except Exception as e: 
        await interaction.followup.send(f"❌ Asynchronous network socket thread failure on Pastebin integration API: {e}")

# ------------------------------------------------------------------------
# COMMAND 8: /bulk (Asynchronous Multi File Stream Transport Matrix)
# ------------------------------------------------------------------------
@bot.tree.command(name="bulk", description="Bundles and dispatches up to 10 assorted unique binary data attachments simultaneously inside a singular network packet.")
@app_commands.choices(ping_everyone=CHOICES_PING_MATRIX)
async def bulk_cmd(
    interaction: discord.Interaction, 
    channel: discord.TextChannel, 
    file1: discord.Attachment, 
    file2: Optional[discord.Attachment] = None, 
    file3: Optional[discord.Attachment] = None, 
    file4: Optional[discord.Attachment] = None, 
    file5: Optional[discord.Attachment] = None, 
    file6: Optional[discord.Attachment] = None, 
    file7: Optional[discord.Attachment] = None, 
    file8: Optional[discord.Attachment] = None, 
    file9: Optional[discord.Attachment] = None, 
    file10: Optional[discord.Attachment] = None, 
    message: Optional[str] = None, 
    picture: Optional[discord.Attachment] = None, 
    ping_everyone: str = "no"
) -> None:
    await interaction.response.defer(ephemeral=True)
    potential_attachments: List[Optional[discord.Attachment]] = [file1, file2, file3, file4, file5, file6, file7, file8, file9, file10]
    active_valid_attachments: List[discord.Attachment] = [f for f in potential_attachments if f is not None]
    
    try:
        compiled_discord_file_objects_list: List[discord.File] = []
        for target_attachment in active_valid_attachments:
            raw_binary_stream = io.BytesIO(await target_attachment.read())
            compiled_discord_file_objects_list.append(discord.File(fp=raw_binary_stream, filename=target_attachment.filename))
            
        manifest_embed = discord.Embed(title="📦 High Density Bulk Package Matrix Cargo Dispatched", description=f"Successfully extracted, re-arranged and forwarded `{len(compiled_discord_file_objects_list)}` unique split file arrays.", color=discord.Color.dark_teal(), timestamp=discord.utils.utcnow())
        if message:
            manifest_embed.add_field(name="💬 Package Logistics Memo", value=message, inline=False)
        if picture:
            manifest_embed.set_image(url=picture.url)
            
        await channel.send(content="@everyone" if ping_everyone == "yes" else None, embed=manifest_embed, files=compiled_discord_file_objects_list)
        await interaction.followup.send(f"✅ Multiplex system packet delivery successful! Routed `{len(compiled_discord_file_objects_list)}` components data fields onto target channel nodes.")
    except Exception as e: 
        await interaction.followup.send(f"❌ Multiplex stream parsing handler system encountered failure state: {e}")

# ------------------------------------------------------------------------
# COMMAND 9: /bulktxt (Asynchronous Multi Line Text File Transport Matrix)
# ------------------------------------------------------------------------
@bot.tree.command(name="bulktxt", description="Bundles and dispatches up to 10 unique plain text format (.txt) attachments concurrently.")
@app_commands.choices(ping_everyone=CHOICES_PING_MATRIX)
async def bulktxt_cmd(
    interaction: discord.Interaction, 
    channel: discord.TextChannel, 
    file1: discord.Attachment, 
    file2: Optional[discord.Attachment] = None, 
    file3: Optional[discord.Attachment] = None, 
    file4: Optional[discord.Attachment] = None, 
    file5: Optional[discord.Attachment] = None, 
    file6: Optional[discord.Attachment] = None, 
    file7: Optional[discord.Attachment] = None, 
    file8: Optional[discord.Attachment] = None, 
    file9: Optional[discord.Attachment] = None, 
    file10: Optional[discord.Attachment] = None, 
    message: Optional[str] = None, 
    picture: Optional[discord.Attachment] = None, 
    ping_everyone: str = "no"
) -> None:
    await interaction.response.defer(ephemeral=True)
    potential_attachments: List[Optional[discord.Attachment]] = [file1, file2, file3, file4, file5, file6, file7, file8, file9, file10]
    active_valid_attachments: List[discord.Attachment] = [f for f in potential_attachments if f is not None]
    
    for tracking_target in active_valid_attachments:
        if not tracking_target.filename.lower().endswith('.txt'): 
            return await interaction.followup.send(f"❌ Validation Abort: File token naming schema constraint failed! `{tracking_target.filename}` is completely incompatible with basic horizontal text parser expectations. Must be `.txt` format.")
            
    try:
        compiled_text_files_list: List[discord.File] = []
        for target_text_attachment in active_valid_attachments:
            text_data_stream_io = io.BytesIO(await target_text_attachment.read())
            compiled_text_files_list.append(discord.File(fp=text_data_stream_io, filename=target_text_attachment.filename))
            
        bulk_txt_embed = discord.Embed(title="📝 Bulk Plain Text Document Compilation Consignment Delivered", description=f"Validated text parameters parsed across `{len(compiled_text_files_list)}` plain text matrix file components.", color=discord.Color.dark_purple(), timestamp=discord.utils.utcnow())
        if message:
            bulk_txt_embed.add_field(name="💬 Multi-Document Context Log Message", value=message, inline=False)
        if picture:
            bulk_txt_embed.set_image(url=picture.url)
            
        await channel.send(content="@everyone" if ping_everyone == "yes" else None, embed=bulk_txt_embed, files=compiled_text_files_list)
        await interaction.followup.send(f"✅ System automated document array deployment sequence absolute success! Distributed `{len(compiled_text_files_list)}` items onto platform space.")
    except Exception as e: 
        await interaction.followup.send(f"❌ Error during multi-line array stream data distribution processing: {e}")

# ------------------------------------------------------------------------
# COMMAND 10: /botinfo (Asynchronous Telemetry Diagnostics Analytics Reporter)
# ------------------------------------------------------------------------
@bot.tree.command(name="botinfo", description="Reports instant gateway network socket latency metrics and physical server footprint indicators.")
async def botinfo_cmd(interaction: discord.Interaction) -> None:
    latency_reading_ms: int = round(bot.latency * 1000)
    connected_guilds_count: int = len(bot.guilds)
    
    analytics_embed = discord.Embed(title=f"🤖 {INFRASTRUCTURE_NAME} Core Engine Performance Reports", color=discord.Color.brand_green(), timestamp=discord.utils.utcnow())
    analytics_embed.add_field(name="Gateway API Network Latency", value=f"`{latency_reading_ms} ms`", inline=True)
    analytics_embed.add_field(name="Connected Server Nodes Footprint", value=f"`{connected_guilds_count}` servers bound", inline=True)
    analytics_embed.add_field(name="Core Base Core System Compile Version", value=f"`v{SYSTEM_VERSION}`", inline=True)
    analytics_embed.add_field(name="Asynchronous Task Event Queue Loop Status", value="`HEALTHY / OPERATIONAL`", inline=False)
    
    analytics_embed.set_thumbnail(url=bot.user.display_avatar.url if bot.user and bot.user.display_avatar else None)
    await interaction.response.send_message(embed=analytics_embed)

# ------------------------------------------------------------------------
# COMMAND 11: /startwelcome (Asynchronous Registration Gateway Logic Binder)
# ------------------------------------------------------------------------
@bot.tree.command(name="startwelcome", description="Locks introduction welcoming event routines directly into a specified text channel matrix address.")
@app_commands.checks.has_permissions(manage_guild=True)
@app_commands.describe(channel="Target channel space vector to output automated verification user tracking info statements")
async def startwelcome_cmd(interaction: discord.Interaction, channel: discord.TextChannel) -> None:
    await interaction.response.defer(ephemeral=True)
    bot.welcome_channels[interaction.guild.id] = channel.id
    try: 
        bot.invites[interaction.guild.id] = await interaction.guild.invites()
    except Exception as e:
        logger.warning(f"Could not rebuild invite tracker cache arrays during channel linkage command: {e}")
        
    await interaction.followup.send(embed=EnterpriseEmbedFactory.build("✨ Introduction Routing Pathway Activated", f"Successfully linked welcome interface notifications to network node: {channel.mention}.", discord.Color.green(), bot))

# ------------------------------------------------------------------------
# COMMAND 12: /purge (Asynchronous Historical Text Buffer Wiper Utility)
# ------------------------------------------------------------------------
@bot.tree.command(name="purge", description="Removes bulk text message historical tracking data blocks from specified or localized target text channels.")
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.describe(amount="Quantity of data items to remove from stream sequence lines (set 0 for complete absolute annihilation clear)", channel="Optional target channel parameter node (defaults to active location context view block)")
async def purge_cmd(interaction: discord.Interaction, amount: int = 0, channel: Optional[discord.TextChannel] = None) -> None:
    await interaction.response.defer(ephemeral=True)
    resolved_target_channel: Union[discord.TextChannel, discord.Thread, discord.DMChannel] = channel if channel else interaction.channel
    
    if not isinstance(resolved_target_channel, (discord.TextChannel, discord.Thread)):
        await interaction.followup.send("❌ Channel Interface Layout Violation: Target structural format must be clear text container channel node layout configurations.", ephemeral=True)
        return

    try:
        purge_limit_value = None if amount == 0 else amount
        purged_messages_list = await resolved_target_channel.purge(limit=purge_limit_value)
        await interaction.followup.send(embed=EnterpriseEmbedFactory.build("🧹 Environment Cleared Successfully", f"Target segment cleared completely inside {resolved_target_channel.mention}. Cleared item lines: `{len(purged_messages_list)}` logs lines data elements erased.", discord.Color.brand_green(), bot))
        logger.info(f"[ADMIN-PURGE] Operator {interaction.user.id} removed {len(purged_messages_list)} items inside channel environment: {resolved_target_channel.id}")
    except Exception as e: 
        await interaction.followup.send(f"❌ Structural wipe command execution crash log output metrics: {e}")

# ------------------------------------------------------------------------
# COMMAND 13: /purgemessages (0-1000 Specialized Context Target Message Channel Purge)
# ------------------------------------------------------------------------
@bot.tree.command(name="purgemessages", description="Deletes message history inside the current channel only (0 to 1000 limit, where 0 removes everything).")
@app_commands.describe(amount="Number of historic messages to delete from this specific text node channel (0 for absolute clear, max 1000 limit).")
@app_commands.checks.has_permissions(manage_messages=True)
async def purgemessages_cmd(interaction: discord.Interaction, amount: app_commands.Range[int, 0, 1000]) -> None:
    """
    Specialized clear tool checking exact constraints. 
    Specifying 0 executes an un-bounded complete historical wiping trace line on the local text channel node space.
    """
    await interaction.response.defer(ephemeral=True)
    active_local_channel = interaction.channel

    # Check bot permissions inside this channel specifically
    if not active_local_channel.permissions_for(interaction.guild.me).manage_messages:
        await interaction.followup.send("❌ High priority permissions fault: Bot application lacks 'Manage Messages' capability flags within this localized channel scope workspace.", ephemeral=True)
        return

    try:
        # If amount parameter value equals 0, map limit value to None to let it parse everything until channel is entirely clear
        execution_limit = None if amount == 0 else amount
        
        logger.info(f"[BULK-MESSAGE-PURGE] Commencing localized text wipe sequence on node: {active_local_channel.id}. Requested limit payload: {amount}")
        wiped_elements = await active_local_channel.purge(limit=execution_limit)
        
        completion_embed = discord.Embed(
            title="🧹 Local Text Channel Node Purge Complete",
            description=f"Successfully extracted and deleted raw database trace data layers inside this communication space.\n\n"
                        f"**Target Location Node:** {active_local_channel.mention}\n"
                        f"**Purged Message Count:** `{len(wiped_elements)}` total lines removed.",
            color=discord.Color.from_rgb(46, 204, 113),
            timestamp=discord.utils.utcnow()
        )
        completion_embed.set_footer(text="Targeted Channel Operations Maintenance Protocol", icon_url=interaction.client.user.display_avatar.url)
        
        await interaction.followup.send(embed=completion_embed, ephemeral=True)
        logger.info(f"[BULK-MESSAGE-PURGE] Success! Removed {len(wiped_elements)} items. Operator profile trace signature: {interaction.user.id}")
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Critical authorization failure: Lacking message history or deletion control access vectors.", ephemeral=True)
    except Exception as critical_error:
        logger.error(f"Error handling /purgemessages execution routine tasks loops: {critical_error}")
        await interaction.followup.send(f"❌ Local core message cleaner tool encountered unexpected operational crash state parameter error: `{critical_error}`", ephemeral=True)

# ------------------------------------------------------------------------
# COMMAND 14: /encode (Asynchronous Encryption Binary Base64 Transformation Matrix)
# ------------------------------------------------------------------------
@bot.tree.command(name="encode", description="Transforms simple string formats securely into raw base64 cryptographic packages output layout files.")
@app_commands.describe(content="Raw plain text data string to transform via Base64 binary matrices encoding algorithms", file_name="Target filename string for export text asset allocation")
async def encode_cmd(interaction: discord.Interaction, content: str, file_name: Optional[str] = "encoded_output_manifest.txt") -> None:
    await interaction.response.defer(ephemeral=True)
    base64_encoded_string_data: str = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    target_filename_string: str = file_name
    if not target_filename_string.endswith(".txt"): 
        target_filename_string += ".txt"
        
    encoded_file_bytes_stream = io.BytesIO(base64_encoded_string_data.encode("utf-8"))
    try:
        await interaction.followup.send(
            embed=EnterpriseEmbedFactory.build("🔒 Cryptographic Base64 Encoding Cipher Rendered", "Payload structural transformation sequence execution absolute success. Binary file package structured completely below.", discord.Color.blue(), bot), 
            file=discord.File(fp=encoded_file_bytes_stream, filename=target_filename_string)
        )
    except Exception as e: 
        await interaction.followup.send(f"❌ Cryptographic conversion array data streaming layer exception error: {e}")

# ------------------------------------------------------------------------
# COMMAND 15: /sendwebhook (Asynchronous Masking Automated Bot Webhook Distributor)
# ------------------------------------------------------------------------
@bot.tree.command(name="sendwebhook", description="Deploys transient masking webhooks to proxy secure text information blocks anonymously.")
@app_commands.choices(show_sender=CHOICES_SENDER_MATRIX, ping_everyone=CHOICES_PING_MATRIX)
@app_commands.describe(channel="Destination channel location framework mapping addresses", message="String context value representing payload content", webhook_name="Masking title designation for automated pseudo webhook identity status", avatar_url="Image profile picture link URL assignment parameters for masking profile look", show_sender="Toggle profile transparency tags", ping_everyone="Toggle everyone emergency alert calls configuration")
async def sendwebhook_cmd(
    interaction: discord.Interaction, 
    channel: discord.TextChannel, 
    message: str, 
    webhook_name: str, 
    avatar_url: Optional[str] = None, 
    show_sender: str = "no", 
    ping_everyone: str = "no"
) -> None:
    await interaction.response.defer(ephemeral=True)
    if not channel.permissions_for(interaction.guild.me).manage_webhooks: 
        return await interaction.followup.send("❌ Lack Permissions Privilege Fault: App execution identity lacks 'Manage Webhooks' parameter flag settings configurations within target channel architecture.")
        
    compiled_webhook_content_string: str = ("@everyone\n" if ping_everyone == "yes" else "") + (f"{message}\n\n*👤 Anonymous Masking Source Identity Verification: {interaction.user.mention}*" if show_sender == "yes" else message)
    try:
        created_temporary_webhook_object = await channel.create_webhook(name="Proxy Engine Infrastructure Node Channel Webhook Vector")
        await created_temporary_webhook_object.send(content=compiled_webhook_content_string, username=webhook_name, avatar_url=avatar_url)
        await created_temporary_webhook_object.delete()
        await interaction.followup.send(f"✅ Webhook masking data distribution sequence success routed on node: {channel.mention}!")
    except Exception as e: 
        await interaction.followup.send(f"❌ Webhook virtual routing interface execution module error: {e}")

# ------------------------------------------------------------------------
# COMMAND 16: /sendannounce (Asynchronous Premium Server Booster Link Publisher Panel)
# ------------------------------------------------------------------------
@bot.tree.command(name="sendannounce", description="Sends the Premium Nitro Booster synchronization validation dashboard layout panel to setup verification channel locations.")
@app_commands.checks.has_permissions(administrator=True)
async def sendannounce_cmd(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=True)
    VERIFY_CHANNEL_ID: int = 1518971603063410753
    
    resolved_verification_channel_node = interaction.client.get_channel(VERIFY_CHANNEL_ID)
    if not resolved_verification_channel_node:
        try: 
            resolved_verification_channel_node = await interaction.client.fetch_channel(VERIFY_CHANNEL_ID)
        except Exception: 
            return await interaction.followup.send("❌ Channel Resolution Interrupt Error: Verification master target array channel address could not be validated or requested from Discord network systems.", ephemeral=True)

    booster_verification_panel_embed = discord.Embed(
        title="🌟 Premium Nitro Server Booster Verification Services Core",
        description="Thank you for supporting our community expansion! 💖\n\nIf you have actively boosted our **Main Server**, click the **Verify Booster Status** button below to sync your status and instantly unlock your exclusive rewards.",
        color=discord.Color.magenta(),
        timestamp=discord.utils.utcnow()
    )
    booster_verification_panel_embed.set_footer(text="Global Premium Booster Synchronization Network Engine Cluster Services", icon_url=interaction.client.user.display_avatar.url)
    try:
        await resolved_verification_channel_node.send(embed=booster_verification_panel_embed, view=VerifyBoosterView())
        await interaction.followup.send("✅ Operational booster validation verification console panel successfully deployed into production.", ephemeral=True)
    except Exception as e: 
        await interaction.followup.send(f"❌ Deployment failure log metrics dashboard crash: {e}", ephemeral=True)

# ------------------------------------------------------------------------
# COMMAND 17: /ticketsetup (Asynchronous Multi Category Ticket Board Deployer)
# ------------------------------------------------------------------------
@bot.tree.command(name="ticketsetup", description="Deploys the persistent cognitive smart category customer ticketing support dispatch services dashboard block layout board to a target channel address.")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(channel="Target channel node context address to render multi category drop view support ticket setup block layout frame panel board item inside")
async def ticketsetup_cmd(interaction: discord.Interaction, channel: discord.TextChannel) -> None:
    await interaction.response.defer(ephemeral=True)
    ticketing_dashboard_embed = discord.Embed(
        title="📩 Support Dispatch Services Panel Core",
        description=(
            "If you are encountering network configuration issues, need account sync adjustments, "
            "or wish to file behavioral compliance claims/reports, select an appropriate routing category from the dropdown menu below.\n\n"
            "**Operational Rules Regulation Ledger:**\n"
            "• Flooding workspace initialization engines or launching spam inquiries leads to systematic firewall communication penalties.\n"
            "• Created private channel workspaces are strictly isolated and only accessible to you and network operations team leads.\n"
            "• Closed support sessions will be entirely transcribed, logged, and archived upon completion for security compliance audits."
        ),
        color=discord.Color.dark_blue(),
        timestamp=discord.utils.utcnow()
    )
    ticketing_dashboard_embed.set_footer(text="Official Advanced Cognitive Multi-Category Ticket System Infrastructure Base Services", icon_url=interaction.client.user.display_avatar.url)
    try:
        await channel.send(embed=ticketing_dashboard_embed, view=TicketSetupView())
        await interaction.followup.send(f"✅ Smart Ticketing cognitive workspace routing hub node successfully deployed and initialized on text channel: {channel.mention}.", ephemeral=True)
    except Exception as e: 
        await interaction.followup.send(f"❌ Core processing interruption crash during dashboard render layout assembly: {e}", ephemeral=True)

# ------------------------------------------------------------------------
# COMMAND 18: /purgetickets (Mass Isolation Ticket Channel Wipe Core Action Engine Node)
# ------------------------------------------------------------------------
@bot.tree.command(name="purgetickets", description="Mass terminates and completely deletes all active support ticket channel workspaces globally inside the active guild layout structure.")
@app_commands.checks.has_permissions(administrator=True)
async def purgetickets_cmd(interaction: discord.Interaction) -> None:
    """Iterates through active text channels array collections inside the guild tracking down ticket string naming prefixes for absolute clean wipe routine deletion scripts."""
    await interaction.response.defer(ephemeral=True)
    wiped_channels_counter: int = 0
    
    logger.info(f"[MASS-TICKET-WIPE] Operator {interaction.user.id} triggered absolute workspace clean wipe deletion script algorithms.")
    for ongoing_channel in interaction.guild.text_channels:
        if ongoing_channel.name.startswith("ticket-"):
            try:
                await ongoing_channel.delete()
                wiped_channels_counter += 1
                logger.info(f"[MASS-TICKET-WIPE] Erased active workspace text channel container node: {ongoing_channel.id}")
            except discord.Forbidden:
                logger.warning(f"[MASS-TICKET-WIPE] Perms error failed deletion on channel index: {ongoing_channel.name} ({ongoing_channel.id})")
            except Exception as channel_deletion_error:
                logger.error(f"[MASS-TICKET-WIPE] Unexpected behavior failure destroying channel {ongoing_channel.name}: {channel_deletion_error}")
                
    await interaction.followup.send(f"✅ Mass support tickets purge protocol absolute complete initialization success. Successfully targeted, closed, logged and permanently terminated `{wiped_channels_counter}` active open workspace isolation channels.", ephemeral=True)
    logger.info(f"[PURGE-TICKETS] Global sweep routine operations finished. Removed total count metrics: {wiped_channels_counter} support channel assets.")

# ========================================================================
# 9. ADVANCED COMPILATION AND SYSTEM EXECUTION LIFECYCLE INITIALIZER ENTRY POINT
# ========================================================================
if __name__ == "__main__":
    logger.info("Initializing system deployment environment configuration analysis checking pipelines parameters...")
    if not TOKEN:
        logger.critical("CRITICAL ENVIRONMENT ENGINE CONFIGURATION ERROR: The 'DISCORD_TOKEN' environment key array token parameter is completely undefined within system setup panels (e.g. Railway Config Variables)!")
    else:
        try:
            logger.info("Passing runtime parameters token configurations straight into target Discord Client Gateway Thread. Booting Application Engine Core...")
            bot.run(TOKEN)
        except Exception as bootstrap_fatal_error:
            logger.critical(f"UNEXPECTED INTERRUPT SYSTEM CRASH: Core framework interface failure initialization layer aborted bootstrap sequence operations loops: {bootstrap_fatal_error}")
