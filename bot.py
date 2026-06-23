import discord
from discord.ext import commands
from discord import app_commands
import io
import os
import json
import logging
import datetime
import asyncio
import requests  
import base64  
from typing import Optional, List, Dict, Any, Union

# TELETHON KÜTÜPHANESİ ENTEGRASYONU
from telethon import TelegramClient, events

# ========================================================================
# 1. ENTERPRISE LEVEL CONFIGURATION AND SETTINGS (Railway/VPS Ready)
# Developer/Maintainer: @vantrexXxx
# ========================================================================
TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")
PASTEBIN_API_KEY: str = os.getenv("PASTEBIN_API_KEY", "SNxRUbS82pBG5qmSW6AeCkmG7nhJhFB1")
PASTEBIN_URL: str = "https://pastebin.com/api/api_post.php"

# Static Global System Configurations
SYSTEM_VERSION: str = "4.7.1-ENTERPRISE-WELCOMER"
INFRASTRUCTURE_NAME: str = "Sleeping Bot Services by @vantrexXxx"
MAX_BULK_ATTACHMENTS: int = 10

# ------------------------------------------------------------------------
# USERBOT (TELEGRAM) VERİLERİNİN ENTEGRASYONU
# ------------------------------------------------------------------------
TELEGRAM_API_ID: int = 33462430  
TELEGRAM_API_HASH: str = "c55be1d2cb63e058d9c64bae4f0c4ec3"  
TELEGRAM_CHANNEL_USERNAME: str = "reposteddatav2"
DISCORD_REPOST_CHANNEL_ID: int = 1518971603063410753  

# ========================================================================
# 2. ADVANCED LOGGING AND AUDIT SYSTEM IMPLEMENTATION
# ========================================================================
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename='discord_bot.log', encoding='utf-8', mode='w')
file_formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Telethon Client Başlatıcı (Oturum dosyasını yerel dizinde saklar)
tg_client = TelegramClient('telegram_userbot_session', TELEGRAM_API_ID, TELEGRAM_API_HASH)

# ========================================================================
# 3. CORE EMBED DESIGN UTILITY FACTORY
# ========================================================================
class EnterpriseEmbedFactory:
    @staticmethod
    def build(
        title: str, 
        description: str, 
        color: discord.Color = discord.Color.blue(),
        ctx_bot: Optional[commands.Bot] = None
    ) -> discord.Embed:
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
    def __init__(self) -> None:
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
        self.invites: Dict[int, List[discord.Invite]] = {}           

    def load_data(self, filename: str, default: dict) -> dict:
        if not os.path.exists(filename):
            return default
        with open(filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                logger.warning(f"[DATABASE] Local database file {filename} corrupted or empty. Resetting.")
                return default

    def save_data(self, filename: str, data: dict) -> None:
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as database_io_error:
            logger.critical(f"[DATABASE-CRITICAL] Failed to execute flush stream on {filename}: {database_io_error}")

    async def setup_hook(self) -> None:
        logger.info("Executing operational boot logic...")
        try:
            self.add_view(VerifyBoosterView())
            self.add_view(TicketSetupView())
            self.add_view(TicketActionView())
            logger.info("Successfully registered core interactive asynchronous dashboard interfaces.")
        except Exception as view_error:
            logger.critical(f"Fatal vulnerability discovered during persistent view assembly: {view_error}")

    async def on_ready(self) -> None:
        logger.info("=" * 60)
        logger.info(f"AUTHORIZED ENTERPRISE SYSTEM CORE CONNECTION ACTIVE")
        logger.info(f"Target Agent Identity: {self.user} (Internal Identifier: {self.user.id})")
        logger.info(f"Framework Engineering Level: {SYSTEM_VERSION}")
        logger.info("=" * 60)
        
        # --- TELEGRAM DİNLEME ARKA PLAN SERVİSİNİ BAŞLATMA ---
        logger.info("[TELEGRAM] Hesabınız üzerinden UserBot dinleme sistemi ayağa kaldırılıyor...")
        try:
            await tg_client.start()
            logger.info("[TELEGRAM] Giriş doğrulandı ve bağlantı kuruldu. Kanal izleniyor...")
        except Exception as tg_err:
            logger.error(f"[TELEGRAM CRITICAL] Telegram hesabına bağlanırken hata: {tg_err}")
        
        try:
            total = 0
            for guild in self.guilds:
                try:
                    guild_obj = discord.Object(id=guild.id)
                    self.tree.copy_global_to(guild=guild_obj)
                    synced = await self.tree.sync(guild=guild_obj)
                    total += len(synced)
                    logger.info(f"[SYNC] {guild.name} -> {len(synced)} commands synced.")
                except Exception as e:
                    logger.error(f"[SYNC ERROR] {guild.name}: {e}")
            logger.info(f"Total synced commands: {total}")
        except Exception as sync_exception:
            logger.error(f"[SYNC-ERROR] Unexpected behavior during context tree replication: {sync_exception}")
        
        logger.info("[TRACKER-INITIALIZER] Running asynchronous sweep to map guild invite arrays...")
        for guild in self.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
                logger.info(f"[TRACKER-INITIALIZER] Successfully cached `{len(self.invites[guild.id])}` metrics for guild: {guild.name}")
            except discord.Forbidden:
                logger.warning(f"[TRACKER-INITIALIZER] Missing mandatory 'Manage Guild' permissions to monitor data in {guild.name}")
                self.invites[guild.id] = []
        
        system_activity = discord.Activity(type=discord.ActivityType.watching, name="the Server and Commands | v" + SYSTEM_VERSION)
        await self.change_presence(status=discord.Status.online, activity=system_activity)

    async def on_invite_create(self, invite: discord.Invite) -> None:
        if invite.guild.id not in self.invites:
            self.invites[invite.guild.id] = []
        self.invites[invite.guild.id].append(invite)
        logger.info(f"[INVITE-CREATE] Recorded new endpoint vector: code '{invite.code}' inside guild context '{invite.guild.name}'.")

    async def on_invite_delete(self, invite: discord.Invite) -> None:
        if invite.guild.id in self.invites:
            self.invites[invite.guild.id] = [i for i in self.invites[invite.guild.id] if i.code != invite.code]
            logger.info(f"[INVITE-DELETE] Purged trackable telemetry code identifier '{invite.code}' from execution loop.")

    async def on_member_join(self, member: discord.Member) -> None:
        logger.info(f"[MEMBER-JOIN] Intercepted new client gateway validation entry point: user={member.name} id={member.id}")
        
        welcome_settings = self.load_data("welcome_settings.json", {})
        guild_id_str = str(member.guild.id)
        
        if guild_id_str not in welcome_settings:
            return
            
        settings = welcome_settings[guild_id_str]
        channel_id = settings.get("channel_id")
        show_pfp = settings.get("show_pfp", "OFF")
        
        channel = member.guild.get_channel(channel_id)
        if not channel:
            return
            
        inviter_name = "Unknown"
        inviter_id = None
        
        try:
            invites_before = self.invites.get(member.guild.id, [])
            invites_after = await member.guild.invites()
            self.invites[member.guild.id] = invites_after
            
            for invite_b in invites_before:
                for invite_a in invites_after:
                    if invite_b.code == invite_a.code and invite_a.uses > invite_b.uses:
                        if invite_a.inviter:
                            inviter_name = invite_a.inviter.name
                            inviter_id = str(invite_a.inviter.id)
                        break
        except Exception as entry_parse_error:
            logger.error(f"[TRACKER-CRITICAL] Automated entry tracking validation pipeline crashed completely: {entry_parse_error}")

        inviter_stats = self.load_data("inviter_stats.json", {})
        if guild_id_str not in inviter_stats:
            inviter_stats[guild_id_str] = {}
            
        inviter_invites = 0
        if inviter_id:
            inviter_stats[guild_id_str][inviter_id] = inviter_stats[guild_id_str].get(inviter_id, 0) + 1
            self.save_data("inviter_stats.json", inviter_stats)
            inviter_invites = inviter_stats[guild_id_str][inviter_id]

        if inviter_id and inviter_name != "Unknown":
            welcome_msg = f"{member.mention} has joined {member.guild.name},You are the {member.guild.member_count}th member! invited by {inviter_name}, who now has {inviter_invites} invites."
        else:
            welcome_msg = f"{member.mention} has joined {member.guild.name},You are the {member.guild.member_count}th member! invited by Unknown, who now has 0 invites."

        embed = None
        if show_pfp == "ON" and member.display_avatar:
            embed = discord.Embed(color=discord.Color.from_rgb(47, 49, 54))
            embed.set_image(url=member.display_avatar.url)
            
        try:
            if embed:
                await channel.send(content=welcome_msg, embed=embed)
            else:
                await channel.send(content=welcome_msg)
        except Exception as execution_output_fault:
            logger.error(f"[MEMBER-JOIN-FAULT] Unable to dispatch text packet stream through internal gateway: {execution_output_fault}")

bot = ProDiscordBot()

# ------------------------------------------------------------------------
# TELETHON TELEGRAM EVENTS (Yabancı Kanalı Dinleme Mekanizması)
# ------------------------------------------------------------------------
@tg_client.on(events.NewMessage(chats=TELEGRAM_CHANNEL_USERNAME))
async def telegram_message_listener(event):
    logger.info("[TELEGRAM] İzlenen kanalda yeni içerik saptandı.")
    try:
        discord_channel = bot.get_channel(DISCORD_REPOST_CHANNEL_ID)
        if not discord_channel:
            logger.error(f"[TELEGRAM-REPOST] Hedef Discord kanalı eksik veya geçersiz. ID: {DISCORD_REPOST_CHANNEL_ID}")
            return
            
        message_text = event.message.message
        
        # Eğer mesaj içerisinde dosya/fotoğraf/medya varsa
        if event.message.media:
            logger.info("[TELEGRAM] Medya algılandı, RAM üzerine çekiliyor...")
            media_buffer = io.BytesIO()
            await tg_client.download_media(event.message, media_buffer)
            media_buffer.seek(0)
            
            filename = "telegram_file"
            if hasattr(event.message.media, 'document') and event.message.media.document.attributes:
                for attr in event.message.media.document.attributes:
                    if hasattr(attr, 'file_name'):
                        filename = attr.file_name
            else:
                filename = "photo.jpg"
                
            discord_file = discord.File(fp=media_buffer, filename=filename)
            await discord_channel.send(content=message_text if message_text else None, file=discord_file)
            logger.info("[TELEGRAM-REPOST] Medyalı içerik Discord'a başarıyla klonlandı.")
        else:
            # Sadece düz yazı ise
            if message_text:
                await discord_channel.send(content=message_text)
                logger.info("[TELEGRAM-REPOST] Metin içeriği Discord'a başarıyla klonlandı.")
                
    except Exception as repost_err:
        logger.error(f"[TELEGRAM-REPOST ERROR] Mesaj geçiş köprüsünde bir tıkanma oldu: {repost_err}")

# ========================================================================
# 5. PERSISTENT SYSTEM COMPONENTS AND HELPER VIEWS
# ========================================================================
class PasteLinkView(discord.ui.View):
    def __init__(self, url: str) -> None:
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="🌐 Open Link (Proxy External)", url=url, style=discord.ButtonStyle.link))

class VerifyBoosterView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Verify Booster Status", style=discord.ButtonStyle.success, custom_id="verify_booster_button_pro")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        MAIN_GUILD_ID: int = 1473684484976148594
        MAIN_BOOSTER_ROLE_ID: int = 1517453584541679627
        TARGET_BOOSTER_ROLE_ID: int = 1518972492004331590
        
        await interaction.response.defer(ephemeral=True)
        main_guild: Optional[discord.Guild] = interaction.client.get_guild(MAIN_GUILD_ID)
        if not main_guild:
            return await interaction.followup.send("❌ The main server operations core could not be reached or resolved.", ephemeral=True)

        member_in_main = main_guild.get_member(interaction.user.id)
        if not member_in_main:
            try:
                member_in_main = await main_guild.fetch_member(interaction.user.id)
            except Exception:
                return await interaction.followup.send("❌ **Verification Failed!** You must be an authenticated member of our Main Server.", ephemeral=True)

        has_booster: bool = any(role.id == MAIN_BOOSTER_ROLE_ID for role in member_in_main.roles)
        if not has_booster:
            return await interaction.followup.send("❌ **Verification Failed!** You do not actively possess the Server Booster role inside our main operations server.", ephemeral=True)

        target_guild: discord.Guild = interaction.guild
        target_role: Optional[discord.Role] = target_guild.get_role(TARGET_BOOSTER_ROLE_ID)
        if not target_role:
            return await interaction.followup.send("❌ Target deployment synchronization role missing from guild database.", ephemeral=True)

        if target_role in interaction.user.roles:
            return await interaction.followup.send("ℹ️ Telemetry synchronization validated. You already possess the target authorization permissions layer.", ephemeral=True)

        try:
            await interaction.user.add_roles(target_role)
            await interaction.followup.send("✅ **Verification Successful!** Main Server Premium Boost telemetry status synchronized. Role granted.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("❌ Authorization deployment error: Hierarchy priority conflict inside role permission layers.", ephemeral=True)
        except Exception as role_err:
            await interaction.followup.send(f"❌ Error during role payload deployment execution sequence parameter maps: {role_err}", ephemeral=True)

# ========================================================================
# 6. ADVANCED COGNITIVE TICKETING MANAGEMENT CORE ENGINE
# ========================================================================
TICKET_LOG_CHANNEL_ID: int = 1518977494068498653
TICKET_STAFF_ROLE_ID: int = 1473685173655830677

class TicketDropdown(discord.ui.Select):
    def __init__(self) -> None:
        options: List[discord.SelectOption] = [
            discord.SelectOption(label="Support", description="If you have any issues.", emoji="🛠️", value="Support Tickets"),
            discord.SelectOption(label="Partnership", description="If you wanna do partnership/ads for ads.", emoji="🤝", value="Partnership Tickets"),
            discord.SelectOption(label="Invite Rewards", description="If you invited people and waiting your invite rewards.", emoji="💳", value="Reward Tickets"),
            discord.SelectOption(label="Report Clowns", description="Report scammers.", emoji="🚫", value="Report Tickets")
        ]
        super().__init__(placeholder="Select a secure inquiry management category...", min_values=1, max_values=1, options=options, custom_id="ticket_routing_dropdown_pro")

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        guild, member, category_name = interaction.guild, interaction.user, self.values[0]
        sanitized_username = member.name.lower().replace(" ", "-")
        existing_channel = discord.utils.get(guild.text_channels, name=f"ticket-{sanitized_username}")
        if existing_channel:
            return await interaction.followup.send(f"❌ **Blocked:** You already have an active workspace initialized: {existing_channel.mention}", ephemeral=True)

        target_category = discord.utils.get(guild.categories, name=category_name)
        if not target_category:
            try:
                target_category = await guild.create_category(name=category_name)
            except discord.Forbidden:
                return await interaction.followup.send("❌ Infrastructure privilege mismatch. Unable to instantiate structural ticket category containers.", ephemeral=True)

        staff_role = guild.get_role(TICKET_STAFF_ROLE_ID)
        permissions_matrix = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True, view_channel=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True, view_channel=True)
        }
        if staff_role:
            permissions_matrix[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, view_channel=True)

        try:
            ticket_channel = await guild.create_text_channel(
                name=f"ticket-{member.name}", category=target_category, overwrites=permissions_matrix,
                topic=f"Owner: {member.id} | Department: {category_name} | Timestamp: {datetime.datetime.utcnow().isoformat()}"
            )
            welcome_embed = discord.Embed(title=f"🎫 Secure Workspace Initialized: {category_name}", description=f"Hello {member.mention}, please state your specific inquiry or query scope details below.", color=discord.Color.brand_green())
            staff_ping = f"{member.mention} | {staff_role.mention}" if staff_role else member.mention
            await ticket_channel.send(content=staff_ping, embed=welcome_embed, view=TicketActionView())
            await interaction.followup.send(f"✅ Secure workspace compiled and initialized: {ticket_channel.mention}", ephemeral=True)
        except Exception as build_err:
            await interaction.followup.send(f"❌ Failed to compile operational text node channel: {build_err}", ephemeral=True)

class TicketSetupView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())

class TicketActionView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close Workspace", style=discord.ButtonStyle.secondary, custom_id="close_ticket_button_pro")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()
        channel = interaction.channel
        channel_topic = channel.topic or ""
        if "Owner:" in channel_topic:
            try:
                extracted_member_id = int(channel_topic.split("|")[0].split(":")[1].strip())
                resolved_member = interaction.guild.get_member(extracted_member_id)
                if resolved_member: 
                    await channel.set_permissions(resolved_member, overwrite=None)
            except Exception: pass
        await channel.send("🔒 **Ticket Locked.** Authorized operations staff can now generate permanent transcripts or execute final server deletion.")

    @discord.ui.button(label="📝 Export Transcript", style=discord.ButtonStyle.primary, custom_id="transcript_ticket_button_pro")
    async def transcript_ticket(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer(ephemeral=True)
        channel = interaction.channel
        master_log_channel = interaction.client.get_channel(TICKET_LOG_CHANNEL_ID)
        if not master_log_channel:
            return await interaction.followup.send("❌ Error: Target deployment system logging registry node unreachable.", ephemeral=True)

        history_buffer = f"--- SECURE LOG ENCRYPTED STREAM TRANSCRIPT ARCHIVE MAP: {channel.name} ---\n"
        history_buffer += f"Generated At Timestamp: {datetime.datetime.utcnow().isoformat()}\n\n"
        
        async for msg in channel.history(limit=None, oldest_first=True):
            history_buffer += f"[{msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}] ({msg.author.name} - ID:{msg.author.id}):\n\"{msg.content}\"\n"
            if msg.attachments:
                for att in msg.attachments:
                    history_buffer += f" >> Attached Asset URL: {att.url}\n"
            history_buffer += "-" * 40 + "\n"
            
        await master_log_channel.send(file=discord.File(fp=io.BytesIO(history_buffer.encode("utf-8")), filename=f"transcript-secure-archive-{channel.name}.txt"))
        await interaction.followup.send("✅ Document exported and synchronized inside main internal logging vaults.", ephemeral=True)

    @discord.ui.button(label="🗑️ Delete Workspace", style=discord.ButtonStyle.danger, custom_id="delete_ticket_button_pro")
    async def delete_ticket(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.channel.send("🗑️ Purging active technical node workspace environment permanently in 5 seconds...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

# ========================================================================
# 7. EXPLICIT GLOBAL ROUTING ERROR INTERCEPTION SYSTEMS
# ========================================================================
@bot.tree.error
async def on_app_command_error_handler(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"⏳ Rate limit dynamic restriction triggered! Please check retry interval timelines after exact time metric gap: `{error.retry_after:.2f}` seconds.", ephemeral=True)
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ Security Fault: Application administrative workspace matrix privileges missing.", ephemeral=True)

# ========================================================================
# 8. SLASH COMMANDS IMPLEMENTATION SEGMENTS
# ========================================================================
CHOICES_PING_MATRIX = [app_commands.Choice(name="Yes", value="yes"), app_commands.Choice(name="No", value="no")]
CHOICES_SENDER_MATRIX = [app_commands.Choice(name="Yes", value="yes"), app_commands.Choice(name="No", value="no")]

@bot.tree.command(name="send", description="Sends text payload content arrays directly to the designated channel.")
@app_commands.choices(show_sender=CHOICES_SENDER_MATRIX, ping_everyone=CHOICES_PING_MATRIX)
async def send_cmd(interaction: discord.Interaction, channel: discord.TextChannel, message: str, picture: Optional[discord.Attachment]=None, show_sender: str="no", ping_everyone: str="no") -> None:
    await interaction.response.defer(ephemeral=True)
    content = f"{message}\n\n*👤 Sender Identity Telemetry Reference: {interaction.user.mention}*" if show_sender == "yes" else message
    final = ("@everyone\n" if ping_everyone == "yes" else "") + content
    files = [await picture.to_file()] if picture else []
    await channel.send(content=final, files=files)
    await interaction.followup.send("✅ Payload Delivered and Stream Completed Successfully.", ephemeral=True)

@bot.tree.command(name="txt", description="Converts input text parameters directly into physical .txt files.")
@app_commands.choices(ping_everyone=CHOICES_PING_MATRIX)
async def txt_cmd(interaction: discord.Interaction, file_name: str, content: str, ping_everyone: str="no") -> None:
    await interaction.response.defer(ephemeral=True)
    if not file_name.endswith(".txt"): file_name += ".txt"
    await interaction.followup.send(content="@everyone" if ping_everyone=="yes" else None, file=discord.File(fp=io.BytesIO(content.encode("utf-8")), filename=file_name))

@bot.tree.command(name="sendtxt", description="Transforms raw string characters into a physical file and pushes to target channels.")
@app_commands.choices(ping_everyone=CHOICES_PING_MATRIX)
async def sendtxt_cmd(interaction: discord.Interaction, channel: discord.TextChannel, file_name: str, content: str, ping_everyone: str="no") -> None:
    await interaction.response.defer(ephemeral=True)
    if not file_name.endswith(".txt"): file_name += ".txt"
    await channel.send(content="@everyone" if ping_everyone=="yes" else None, file=discord.File(fp=io.BytesIO(content.encode("utf-8")), filename=file_name))
    await interaction.followup.send("✅ Document Pushed and Synced.", ephemeral=True)

@bot.tree.command(name="modifytxt", description="Flattens vertical newline string parameters into a compressed horizontal layout.")
async def modifytxt_cmd(interaction: discord.Interaction, channel: discord.TextChannel, file_name: str, content: str) -> None:
    await interaction.response.defer(ephemeral=True)
    if not file_name.endswith(".txt"): file_name += ".txt"
    flattened = " ".join([l.strip() for l in content.splitlines() if l.strip()])
    await channel.send(file=discord.File(fp=io.BytesIO(flattened.encode("utf-8")), filename=file_name))
    await interaction.followup.send("✅ Horizontally Serialized Modified Document Dispatched.", flattened)

@bot.tree.command(name="sendmytxt", description="Reads an uploaded local text document payload and routes it onto designated pipelines.")
async def sendmytxt_cmd(interaction: discord.Interaction, channel: discord.TextChannel, file: discord.Attachment) -> None:
    await interaction.response.defer(ephemeral=True)
    await channel.send(file=discord.File(fp=io.BytesIO(await file.read()), filename=file.filename))
    await interaction.followup.send("✅ Document Routed with Absolute Payload Integrity Verification.", ephemeral=True)

@bot.tree.command(name="sendannounce", description="Send booster verification panel.")
@app_commands.checks.has_permissions(administrator=True)
async def sendannounce_cmd(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    BOOSTER_GUILD_ID = 1518971603063410750
    VERIFY_CHANNEL_ID = 1518971603063410753

    guild = bot.get_guild(BOOSTER_GUILD_ID)

    if guild is None:
        return await interaction.followup.send("❌ Booster server not found.", ephemeral=True)

    channel = guild.get_channel(VERIFY_CHANNEL_ID)

    if channel is None:
        return await interaction.followup.send("❌ Verify channel not found.", ephemeral=True)

    embed = discord.Embed(
        title="🌟 Server Booster Verification",
        description=(
            "Thank you for supporting our community! ❤️\n\n"
            "If you have boosted our Main Server, click the button below.\n\n"
            "**Verification Rules**\n"
            "• **You must be in our Main Server.**\n"
            "• **You must actively have the Server Booster role.**\n"
            "• **Verification is automatic.**\n\n"
            "***Click the button below to verify.***"
        ),
        color=discord.Color.purple()
    )

    await channel.send(embed=embed, view=VerifyBoosterView())
    await interaction.followup.send("✅ Verification panel sent.", ephemeral=True)

@bot.tree.command(name="sendmyfile", description="Accepts and routes generic binary files or media formats across internal channels.")
async def sendmyfile_cmd(interaction: discord.Interaction, channel: discord.TextChannel, file: discord.Attachment) -> None:
    await interaction.response.defer(ephemeral=True)
    await channel.send(file=discord.File(fp=io.BytesIO(await file.read()), filename=file.filename))
    await interaction.followup.send("✅ Binary Delivered Safely.", ephemeral=True)

@bot.tree.command(name="bulk", description="Bundles and dispatches up to 10 unique binary data attachments into a batch transfer.")
async def bulk_cmd(interaction: discord.Interaction, channel: discord.TextChannel, file1: discord.Attachment, file2: Optional[discord.Attachment]=None) -> None:
    await interaction.response.defer(ephemeral=True)
    atts = [f for f in [file1, file2] if f]
    files = [discord.File(fp=io.BytesIO(await a.read()), filename=a.filename) for a in atts]
    await channel.send(files=files)
    await interaction.followup.send("✅ Bulk Processing System Deployment Successful.", ephemeral=True)

@bot.tree.command(name="botinfo", description="Reports gateway network socket latency metrics and operational footprint parameters.")
async def botinfo_cmd(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"🤖 **Gateway Heartbeat Metric:** `{round(bot.latency * 1000)}ms` | **Active Node Servers Tracker:** `{len(bot.guilds)}` | **System Infrastructure Level:** `v{SYSTEM_VERSION}`")

@bot.tree.command(name="purge", description="Removes bulk text message historical tracking data from active execution channels.")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge_cmd(interaction: discord.Interaction, amount: int = 0) -> None:
    await interaction.response.defer(ephemeral=True)
    purged = await interaction.channel.purge(limit=None if amount == 0 else amount)
    await interaction.followup.send(f"🧹 Purge pipeline processed. Permanently terminated `{len(purged)}` message packet records from history logs.", ephemeral=True)

@bot.tree.command(name="purgemessages", description="Deletes message logs and history inside the current channel frame up to 1000 lines.")
@app_commands.checks.has_permissions(manage_messages=True)
async def purgemessages_cmd(interaction: discord.Interaction, amount: app_commands.Range[int, 0, 1000]) -> None:
    await interaction.response.defer(ephemeral=True)
    purged = await interaction.channel.purge(limit=None if amount == 0 else amount)
    await interaction.followup.send(f"🧹 Data structure cleaning executed successfully. Purged exactly `{len(purged)}` cached historical objects.", ephemeral=True)

@bot.tree.command(name="encode", description="Transforms simple string formats securely into raw base64 data structures as a file.")
async def encode_cmd(interaction: discord.Interaction, content: str) -> None:
    await interaction.response.defer(ephemeral=True)
    b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    await interaction.followup.send(file=discord.File(fp=io.BytesIO(b64.encode("utf-8")), filename="encoded-base64-payload.txt"), ephemeral=True)

@bot.tree.command(name="sendwebhook", description="Deploys transient masking webhooks to route data packets impersonating specific aliases.")
async def sendwebhook_cmd(interaction: discord.Interaction, channel: discord.TextChannel, message: str, webhook_name: str) -> None:
    await interaction.response.defer(ephemeral=True)
    wh = await channel.create_webhook(name="Infrastructure Proxy Engine")
    await wh.send(content=message, username=webhook_name)
    await wh.delete()
    await interaction.followup.send("✅ Transmitted payload virtualization via ephemeral remote webhook node successfully.", ephemeral=True)

@bot.tree.command(name="ticketsetup", description="Deploys the ticketing support dispatch dashboard block down inside specified channels.")
@app_commands.checks.has_permissions(administrator=True)
async def ticketsetup_cmd(interaction: discord.Interaction, channel: discord.TextChannel) -> None:
    await interaction.response.defer(ephemeral=True)
    await channel.send(embed=discord.Embed(title="📩 Operations Support Center Panel", description="Initialize an active workspace routing segment below.", color=discord.Color.dark_blue()), view=TicketSetupView())
    await interaction.followup.send("✅ Ticketing interaction component node successfully deployed inside live production environments.", ephemeral=True)

@bot.tree.command(name="purgetickets", description="Mass terminates active support ticket workspace isolation channels from server structures.")
@app_commands.checks.has_permissions(administrator=True)
async def purgetickets_cmd(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=True)
    count = 0
    for ch in interaction.guild.text_channels:
        if ch.name.startswith("ticket-"):
            await ch.delete()
            count += 1
    await interaction.followup.send(f"✅ Mass support tickets purge protocol absolute complete initialization success. Successfully targeted and permanently terminated `{count}` active open workspace channels.", ephemeral=True)

# ========================================================================
# ADVANCED WELCOMER & INVITE TRACKER MANAGEMENT INTEGRATION PLUGINS
# ========================================================================

@bot.tree.command(name="startwelcome", description="Configures and initializes the advanced greeting welcomer pipeline system.")
@app_commands.checks.has_permissions(manage_guild=True)
@app_commands.choices(profile_photo=[
    app_commands.Choice(name="ON (Show Profile Photo)", value="ON"),
    app_commands.Choice(name="OFF (Text Only)", value="OFF")
])
async def startwelcome_cmd(interaction: discord.Interaction, channel: discord.TextChannel, profile_photo: str = "OFF") -> None:
    await interaction.response.defer(ephemeral=True)
    
    settings = bot.load_data("welcome_settings.json", {})
    settings[str(interaction.guild.id)] = {
        "channel_id": channel.id,
        "show_pfp": profile_photo
    }
    bot.save_data("welcome_settings.json", settings)
    
    try: 
        bot.invites[interaction.guild.id] = await interaction.guild.invites()
    except Exception as invite_cache_rebuild_error: 
        logger.error(f"[WELCOME-CONFIG-ERROR] Failed to securely cache invite links list array details: {invite_cache_rebuild_error}")
        
    await interaction.followup.send(
        embed=EnterpriseEmbedFactory.build(
            "✨ Welcome System Active Routing Node Established", 
            f"The welcoming telemetries have been successfully routed onto target data node: {channel.mention}\n"
            f"Profile Picture Render Configuration Parameter Toggle state resolved to: **{profile_photo}**", 
            discord.Color.green(), 
            bot
        )
    )

@bot.tree.command(name="stopwelcome", description="Terminates, unsubscribes and completely shuts down the active welcomer pipeline.")
@app_commands.checks.has_permissions(manage_guild=True)
async def stopwelcome_cmd(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=True)
    
    settings = bot.load_data("welcome_settings.json", {})
    guild_id_str = str(interaction.guild.id)
    
    if guild_id_str in settings:
        del settings[guild_id_str]
        bot.save_data("welcome_settings.json", settings)
        await interaction.followup.send("🛑 Welcomer greetings data routing pipeline has been completely deactivated and decoupled successfully.", ephemeral=True)
    else:
        await interaction.followup.send("❌ Operational Error: There is no active welcome deployment setup configured inside this guild sector.", ephemeral=True)

@bot.tree.command(name="invite", description="Displays tracked internal invite telemetry statistics counters for targeted members.")
async def invite_cmd(interaction: discord.Interaction, user: Optional[discord.Member] = None) -> None:
    await interaction.response.defer()
    target = user or interaction.user
    
    stats = bot.load_data("inviter_stats.json", {})
    guild_id_str = str(interaction.guild.id)
    user_id_str = str(target.id)
    
    invite_count_metric = stats.get(guild_id_str, {}).get(user_id_str, 0)
    await interaction.followup.send(f"✉️ **{target.name}** has **{invite_count_metric}** invites.")

@bot.tree.command(name="resetinvites", description="Purges, drops and flushes all recorded user invitation statistics within the guild.")
@app_commands.checks.has_permissions(administrator=True)
async def resetinvites_cmd(interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=True)
    
    stats = bot.load_data("inviter_stats.json", {})
    guild_id_str = str(interaction.guild.id)
    
    if guild_id_str in stats:
        stats[guild_id_str] = {}
        bot.save_data("inviter_stats.json", stats)
    
    try:
        bot.invites[interaction.guild.id] = await interaction.guild.invites()
    except Exception as telemetry_sync_err:
        logger.error(f"[DATABASE-WIPE-ERR] Critical sync fault reported while updating background parameters: {telemetry_sync_err}")
        
    await interaction.followup.send("✅ Database Purge Protocol Executed: All recorded user invitation statistics numbers have been wiped back to default zero layers.", ephemeral=True)

# ========================================================================
# 9. SYSTEM EXECUTION LIFECYCLE INITIALIZER ENTRY POINT
# ========================================================================
if __name__ == "__main__":
    logger.info("Initializing system deployment environment configuration analysis checking pipelines parameters...")
    if not TOKEN:
        logger.critical("CRITICAL ENVIRONMENT ENGINE CONFIGURATION ERROR: The 'DISCORD_TOKEN' environment key array token parameter is completely undefined within system setup panels (e.g. Railway Config Variables)!")
    else:
        try:
            bot.run(TOKEN)
        except Exception as bootstrap_fatal_error:
            logger.critical(f"UNEXPECTED INTERRUPT SYSTEM CRASH: Core framework interface failure initialization layer aborted bootstrap sequence operations loops: {bootstrap_fatal_error}")
