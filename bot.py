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
from typing import Optional

# ========================================================================
# 1. SETTINGS AND CONFIGURATION (Railway Compatible)
# ========================================================================
TOKEN = os.getenv("DISCORD_TOKEN")
PASTEBIN_API_KEY = os.getenv("PASTEBIN_API_KEY", "SNxRUbS82pBG5qmSW6AeCkmG7nhJhFB1")
PASTEBIN_URL = "https://pastebin.com/api/api_post.php"

# ========================================================================
# 2. LOGGING SYSTEM
# ========================================================================
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename='discord_bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

# ========================================================================
# 3. BOT CLASS AND CONNECTION INFRASTRUCTURE
# ========================================================================
class ProDiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.invites = True  
        
        super().__init__(
            command_prefix="!", 
            intents=intents,
            help_command=None
        )
        self.welcome_channels = {}  
        self.invites = {}           

    # INDENTATION ERROR FIXED HERE (Hizalama hatası düzeltildi)
    async def setup_hook(self):
        logger.info("Registering persistent views inside the execution hook...")
        self.add_view(VerifyBoosterView())
        self.add_view(TicketSetupView())
        self.add_view(TicketActionView())

    async def on_ready(self):
        logger.info(f"Bot successfully logged in! User: {self.user} (ID: {self.user.id})")
        logger.info("-" * 40)
        
        try:
            logger.info("Force syncing slash commands globally...")
            await self.tree.sync()
            logger.info("All global slash commands synced successfully!")
        except discord.Forbidden:
            logger.critical("Sync failed! Bot lacks 'applications.commands' scope.")
        except Exception as e:
            logger.error(f"Error occurred while registering server applications tree context: {e}")
        
        for guild in self.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except discord.Forbidden:
                self.invites[guild.id] = []
            except Exception as e:
                logger.error(f"Failed to fetch invite manifest for guild {guild.id}: {e}")
        
        activity = discord.Activity(type=discord.ActivityType.watching, name="the Server and Commands")
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_invite_create(self, invite):
        if invite.guild.id not in self.invites:
            self.invites[invite.guild.id] = []
        self.invites[invite.guild.id].append(invite)

    async def on_invite_delete(self, invite):
        if invite.guild.id in self.invites:
            self.invites[invite.guild.id] = [i for i in self.invites[invite.guild.id] if i.code != invite.code]

    async def on_member_join(self, member):
        welcome_channel_id = self.welcome_channels.get(member.guild.id)
        if not welcome_channel_id:
            return
            
        channel = member.guild.get_channel(welcome_channel_id)
        if not channel:
            return
            
        inviter_str = "Unknown/Direct Access"
        try:
            invites_before = self.invites.get(member.guild.id, [])
            invites_after = await member.guild.invites()
            self.invites[member.guild.id] = invites_after
            
            for invite_b in invites_before:
                for invite_a in invites_after:
                    if invite_b.code == invite_a.code and invite_a.uses > invite_b.uses:
                        if invite_a.inviter:
                            inviter_str = invite_a.inviter.mention
                        break
        except Exception as e:
            logger.error(f"[TRACK-CRITICAL] Error parsing execution tracking metadata loops: {e}")
            
        welcome_msg = f"Hey {member.mention}, welcome to **{member.guild.name}**! 🎉 You were invited to our community by {inviter_str}."
        try:
            await channel.send(welcome_msg)
        except Exception as e:
            logger.error(f"Failed to submit welcome message payload: {e}")

bot = ProDiscordBot()

# ========================================================================
# 4. HELPER CLASSES AND FUNCTIONS
# ========================================================================
def create_embed(title: str, description: str, color: discord.Color = discord.Color.blue()) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=color, timestamp=discord.utils.utcnow())
    embed.set_footer(text="Sleeping Bot Infrastructure", icon_url=bot.user.display_avatar.url if bot.user and bot.user.display_avatar else None)
    return embed

class PasteLinkView(discord.ui.View):
    def __init__(self, url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="🌐 Open Link (Proxy)", url=url, style=discord.ButtonStyle.link))

class VerifyBoosterView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Verify Booster Status", style=discord.ButtonStyle.success, custom_id="verify_booster_button")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        MAIN_GUILD_ID = 1473684484976148594
        MAIN_BOOSTER_ROLE_ID = 1517453584541679627
        TARGET_BOOSTER_ROLE_ID = 1518972492004331590
        
        main_guild = interaction.client.get_guild(MAIN_GUILD_ID)
        if not main_guild:
            await interaction.response.send_message("❌ The main server could not be reached.", ephemeral=True)
            return

        member_in_main = main_guild.get_member(interaction.user.id)
        if not member_in_main:
            try:
                member_in_main = await main_guild.fetch_member(interaction.user.id)
            except:
                await interaction.response.send_message("❌ **Verification Failed!** You must be a member of our Main Server.", ephemeral=True)
                return

        has_booster = any(role.id == MAIN_BOOSTER_ROLE_ID for role in member_in_main.roles)
        if not has_booster:
            await interaction.response.send_message("❌ **Verification Failed!** You do not actively possess the Server Booster role.", ephemeral=True)
            return

        target_guild = interaction.guild
        target_role = target_guild.get_role(TARGET_BOOSTER_ROLE_ID)
        if not target_role:
            await interaction.response.send_message("❌ **System Error:** Sync role does not exist here.", ephemeral=True)
            return

        if target_role in interaction.user.roles:
            await interaction.response.send_message("ℹ️ You have already been successfully verified!", ephemeral=True)
            return

        try:
            await interaction.user.add_roles(target_role)
            await interaction.response.send_message("✅ **Verification Successful!** Main Server Boost status synchronized.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error during role execution: {e}", ephemeral=True)

# ========================================================================
# 5. ADVANCED TICKET ENGINE (SMART CATEGORY ROUTING)
# ========================================================================
TICKET_LOG_CHANNEL_ID = 1518977494068498653
TICKET_STAFF_ROLE_ID = 1473685173655830677

class TicketDropdown(discord.ui.Select):
    """Smart routing dropdown menu for advanced ticket categorization"""
    def __init__(self):
        options = [
            discord.SelectOption(label="General Support", description="Standard technical or community assistance.", emoji="🛠️", value="Support Tickets"),
            discord.SelectOption(label="Partnership", description="Business, alliances, and partnership inquiries.", emoji="🤝", value="Partnership Tickets"),
            discord.SelectOption(label="Billing & Operations", description="Payment, account, or premium issues.", emoji="💳", value="Billing Tickets"),
            discord.SelectOption(label="Report Violation", description="File a claim or report a vulnerability.", emoji="🚫", value="Report Tickets")
        ]
        super().__init__(placeholder="Select an inquiry category...", min_values=1, max_values=1, options=options, custom_id="ticket_routing_dropdown")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        member = interaction.user
        category_name = self.values[0]

        # Anti-spam: check if user already has an active ticket
        existing_channel = discord.utils.get(guild.channels, name=f"ticket-{member.name.lower()}")
        if existing_channel:
            await interaction.followup.send(f"❌ **Blocked:** You already have an active open workspace: {existing_channel.mention}", ephemeral=True)
            return

        # SMART CATEGORY ROUTING: Get or create the specific category based on selection
        target_category = discord.utils.get(guild.categories, name=category_name)
        if not target_category:
            try:
                target_category = await guild.create_category(name=category_name)
            except discord.Forbidden:
                await interaction.followup.send("❌ Error: App lacks 'Manage Channels' permission to create routing categories.", ephemeral=True)
                return

        staff_role = guild.get_role(TICKET_STAFF_ROLE_ID)
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True, manage_channels=True)
        }
        
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True)

        try:
            ticket_channel = await guild.create_text_channel(
                name=f"ticket-{member.name}",
                category=target_category,
                overwrites=overwrites,
                topic=f"Owner: {member.id} | Department: {category_name} | Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )

            embed = discord.Embed(
                title=f"🎫 {category_name} Inquiry",
                description=(
                    f"Hello {member.mention}, your secure workspace has been allocated.\n\n"
                    f"**Department:** `{category_name}`\n"
                    "Please provide all necessary details regarding your request below. Our operations team will review your data shortly.\n\n"
                    "**Management Triggers:**\n"
                    "🔒 **Close:** Lock workspace access.\n"
                    "📝 **Transcript:** Archive communication history.\n"
                    "🗑️ **Delete:** Terminate environment."
                ),
                color=discord.Color.brand_green(),
                timestamp=discord.utils.utcnow()
            )
            embed.set_footer(text="Advanced Ticket Infrastructure Blueprint")
            
            await ticket_channel.send(content=f"{member.mention} | {staff_role.mention if staff_role else ''}", embed=embed, view=TicketActionView())
            await interaction.followup.send(f"✅ Your secure {category_name} workspace is ready: {ticket_channel.mention}", ephemeral=True)
            logger.info(f"[TICKET-CREATE] {member} launched {category_name} loop {ticket_channel.id}")

        except Exception as e:
            await interaction.followup.send(f"❌ Core processing failed to initialize channel: {e}", ephemeral=True)

class TicketSetupView(discord.ui.View):
    """The persistent dropdown panel setup layout"""
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())

class TicketActionView(discord.ui.View):
    """Management operations matrix dashboard bound inside active ticket rooms"""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close", style=discord.ButtonStyle.secondary, custom_id="close_ticket_button")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        channel = interaction.channel
        
        topic = channel.topic or ""
        member_id = None
        if "Owner:" in topic:
            try: member_id = int(topic.split("|")[0].split(":")[1].strip())
            except: pass

        if member_id:
            member = interaction.guild.get_member(member_id)
            if member:
                await channel.set_permissions(member, overwrite=None)
        
        await channel.send("🔒 **Ticket Locked.** Creator access permissions evicted. Operators can now dump transcripts or execute deletion routines.")

    @discord.ui.button(label="📝 Transcript", style=discord.ButtonStyle.primary, custom_id="transcript_ticket_button")
    async def transcript_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        channel = interaction.channel
        log_channel = interaction.client.get_channel(TICKET_LOG_CHANNEL_ID)

        if not log_channel:
            await interaction.followup.send("❌ Master logs data drop endpoint missing or inaccessible.", ephemeral=True)
            return

        await interaction.followup.send("📝 Compiling historical text data metrics. Please wait...", ephemeral=True)

        history_text = f"--- HISTORICAL WORKSPACE TRANSACTION TRANSCRIPT: {channel.name} ---\n"
        history_text += f"Dump Instance Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        history_text += f"Executing Agent Profile: {interaction.user} ({interaction.user.id})\n"
        history_text += "----------------------------------------------------------------------\n\n"

        async for msg in channel.history(limit=None, oldest_first=True):
            time_str = msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
            history_text += f"[{time_str}] {msg.author}: {msg.content}\n"
            if msg.attachments:
                for att in msg.attachments:
                    history_text += f" > [Media Ejected]: {att.url}\n"

        file_bytes = io.BytesIO(history_text.encode("utf-8"))
        discord_file = discord.File(fp=file_bytes, filename=f"transcript-{channel.name}.txt")

        embed = discord.Embed(
            title="📝 Ticket Session Archived",
            description=f"**Target Room Tag:** `{channel.name}`\n**Archiving Officer:** {interaction.user.mention}\n**State:** File manifest exported securely.",
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow()
        )
        
        await log_channel.send(embed=embed, file=discord_file)
        await interaction.followup.send("✅ Document archive payload pushed out successfully!", ephemeral=True)

    @discord.ui.button(label="🗑️ Delete", style=discord.ButtonStyle.danger, custom_id="delete_ticket_button")
    async def delete_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🗑️ Channel termination sequence active. Purging workspace in 5 seconds...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

# ========================================================================
# 6. GLOBAL ERROR HANDLER
# ========================================================================
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"⏳ Please slow down! Wait {error.retry_after:.2f} seconds.", ephemeral=True)
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You do not have the required application privileges.", ephemeral=True)
    else:
        logger.error(f"Command error: {error}")

# ========================================================================
# 7. ALL ACTIVE SLASH COMMANDS
# ========================================================================

PING_CHOICES = [
    app_commands.Choice(name="Yes, mention @everyone", value="yes"),
    app_commands.Choice(name="No, do not mention", value="no")
]

EXPIRATION_CHOICES = [
    app_commands.Choice(name="10 Minutes", value="10M"),
    app_commands.Choice(name="1 Hour", value="1H"),
    app_commands.Choice(name="1 Day", value="1D"),
    app_commands.Choice(name="1 Week", value="1W"),
    app_commands.Choice(name="1 Month", value="1M"),
    app_commands.Choice(name="1 Year", value="1Y"),
    app_commands.Choice(name="Never", value="N")
]

@bot.tree.command(name="send", description="Sends the desired text string straight to the designated target channel.")
@app_commands.choices(show_sender=[app_commands.Choice(name="Yes", value="yes"), app_commands.Choice(name="No", value="no")], ping_everyone=PING_CHOICES)
async def send_cmd(interaction: discord.Interaction, channel: discord.TextChannel, message: str, picture: Optional[discord.Attachment] = None, show_sender: str = "no", ping_everyone: str = "no"):
    await interaction.response.defer(ephemeral=True)
    if not channel: return
    content_pieces = [f"{message}\n\n*👤 Sender Identification: {interaction.user.mention}*" if show_sender == "yes" else message]
    gonderilecek_icerik = ("@everyone\n" if ping_everyone == "yes" else "") + "\n".join(content_pieces)
    files_to_send = [await picture.to_file()] if picture else []
    try:
        await channel.send(content=gonderilecek_icerik, files=files_to_send) if files_to_send else await channel.send(content=gonderilecek_icerik)
        await interaction.followup.send(embed=create_embed("✅ Success", f"Message delivered to {channel.mention}.", discord.Color.green()))
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="txt", description="Converts input text parameters directly into a downloadable .txt document asset.")
@app_commands.choices(ping_everyone=PING_CHOICES)
async def txt_cmd(interaction: discord.Interaction, file_name: str, content: str, message: Optional[str] = None, picture: Optional[discord.Attachment] = None, ping_everyone: str = "no"):
    await interaction.response.defer(ephemeral=True)
    file_name = file_name.replace(" ", "_") + (".txt" if not file_name.endswith(".txt") else "")
    dosya_byte = io.BytesIO(content.encode("utf-8"))
    embed = create_embed("📄 Your Custom Document is Ready", f"File artifact: **`{file_name}`** created.", discord.Color.gold())
    if message: embed.add_field(name="💬 Content", value=message, inline=False)
    if picture: embed.set_image(url=picture.url)
    try: await interaction.followup.send(content="@everyone" if ping_everyone == "yes" else None, embed=embed, file=discord.File(fp=dosya_byte, filename=file_name))
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="sendtxt", description="Transforms string characters into a .txt file asset and delivers it to a channel.")
@app_commands.choices(show_sender=[app_commands.Choice(name="Yes", value="yes"), app_commands.Choice(name="No", value="no")], ping_everyone=PING_CHOICES)
async def sendtxt_cmd(interaction: discord.Interaction, channel: discord.TextChannel, file_name: str, content: str, message: Optional[str] = None, picture: Optional[discord.Attachment] = None, show_sender: str = "no", ping_everyone: str = "no"):
    await interaction.response.defer(ephemeral=True)
    file_name = file_name.replace(" ", "_") + (".txt" if not file_name.endswith(".txt") else "")
    embed = discord.Embed(title="📁 A New Document Has Been Uploaded", color=discord.Color.dark_theme(), timestamp=discord.utils.utcnow())
    if show_sender == "yes": embed.add_field(name="Sender", value=interaction.user.mention, inline=False)
    embed.add_field(name="Label", value=f"`{file_name}`", inline=False)
    if message: embed.add_field(name="💬 Text", value=message, inline=False)
    dosya_byte = io.BytesIO(content.encode("utf-8"))
    try:
        await channel.send(content="@everyone" if ping_everyone == "yes" else None, embed=embed, file=discord.File(fp=dosya_byte, filename=file_name))
        await interaction.followup.send(f"✅ Uploaded to {channel.mention}.")
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="modifytxt", description="Flattens all vertical newline text arguments into a uniform horizontal block.")
@app_commands.choices(show_sender=[app_commands.Choice(name="Yes", value="yes"), app_commands.Choice(name="No", value="no")], ping_everyone=PING_CHOICES)
async def modifytxt_cmd(interaction: discord.Interaction, channel: discord.TextChannel, file_name: str, content: str, message: Optional[str] = None, picture: Optional[discord.Attachment] = None, show_sender: str = "no", ping_everyone: str = "no"):
    await interaction.response.defer(ephemeral=True)
    file_name = file_name.replace(" ", "_") + (".txt" if not file_name.endswith(".txt") else "")
    flattened_content = " ".join([line.strip() for line in content.splitlines() if line.strip()])
    dosya_byte = io.BytesIO(flattened_content.encode("utf-8"))
    embed = discord.Embed(title="📁 A Modified Document Uploaded", color=discord.Color.orange(), timestamp=discord.utils.utcnow())
    if message: embed.add_field(name="💬 Notes", value=message, inline=False)
    try:
        await channel.send(content="@everyone" if ping_everyone == "yes" else None, embed=embed, file=discord.File(fp=dosya_byte, filename=file_name))
        await interaction.followup.send(f"✅ Uploaded to {channel.mention}.")
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="sendmytxt", description="Reads an uploaded local .txt document, copies it, and forwards it.")
@app_commands.choices(ping_everyone=PING_CHOICES)
async def sendmytxt_cmd(interaction: discord.Interaction, channel: discord.TextChannel, file: discord.Attachment, message: Optional[str] = None, picture: Optional[discord.Attachment] = None, ping_everyone: str = "no"):
    await interaction.response.defer(ephemeral=True)
    if not file.filename.lower().endswith('.txt'):
        await interaction.followup.send("❌ Error: Requires `.txt` format.")
        return
    try:
        dosya_byte = io.BytesIO(await file.read())
        embed = discord.Embed(title="📥 Forwarded File Arrived", color=discord.Color.purple(), timestamp=discord.utils.utcnow())
        if message: embed.add_field(name="💬 Notes", value=message, inline=False)
        await channel.send(content="@everyone" if ping_everyone == "yes" else None, embed=embed, file=discord.File(fp=dosya_byte, filename=file.filename))
        await interaction.followup.send(f"✅ Forwarded to {channel.mention}.")
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="sendmyfile", description="Accepts and routes any generic binary file format layout across channels.")
@app_commands.choices(ping_everyone=PING_CHOICES)
async def sendmyfile_cmd(interaction: discord.Interaction, channel: discord.TextChannel, file: discord.Attachment, message: Optional[str] = None, picture: Optional[discord.Attachment] = None, ping_everyone: str = "no"):
    await interaction.response.defer(ephemeral=True)
    try:
        dosya_byte = io.BytesIO(await file.read())
        embed = discord.Embed(title="📦 New File Package Arrived", color=discord.Color.teal(), timestamp=discord.utils.utcnow())
        if message: embed.add_field(name="💬 Notes", value=message, inline=False)
        await channel.send(content="@everyone" if ping_everyone == "yes" else None, embed=embed, file=discord.File(fp=dosya_byte, filename=file.filename))
        await interaction.followup.send(f"✅ Forwarded to {channel.mention}.")
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="paste", description="Uploads comprehensive raw text data packages directly into Pastebin.")
@app_commands.choices(expiration=EXPIRATION_CHOICES, ping_everyone=PING_CHOICES)
async def paste_cmd(interaction: discord.Interaction, channel: discord.TextChannel, content: str, title: Optional[str] = "Untitled Paste", expiration: str = "N", message: Optional[str] = None, picture: Optional[discord.Attachment] = None, ping_everyone: str = "no"):
    await interaction.response.defer(ephemeral=True)
    payload = {"api_dev_key": PASTEBIN_API_KEY, "api_option": "paste", "api_paste_code": content, "api_paste_name": title, "api_paste_expire_date": expiration, "api_paste_private": "0"}
    try:
        response = await asyncio.to_thread(requests.post, PASTEBIN_URL, data=payload, timeout=10)
        if response.status_code == 200 and "pastebin.com" in response.text:
            proxy_url = response.text.strip().replace("pastebin.com", "pastebinp.com")
            embed = discord.Embed(title="🎉 Text Data Successfully Pasted!", color=discord.Color.blue(), timestamp=discord.utils.utcnow())
            await channel.send(content="@everyone" if ping_everyone == "yes" else None, embed=embed, view=PasteLinkView(url=proxy_url))
            await interaction.followup.send(f"✅ Proxy URL generated: {proxy_url}")
        else: await interaction.followup.send(f"❌ Error: `{response.text}`")
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="bulk", description="Bundles and dispatches up to 10 assorted unique attachments simultaneously.")
@app_commands.choices(ping_everyone=PING_CHOICES)
async def bulk_cmd(interaction: discord.Interaction, channel: discord.TextChannel, file1: discord.Attachment, file2: Optional[discord.Attachment] = None, file3: Optional[discord.Attachment] = None, file4: Optional[discord.Attachment] = None, file5: Optional[discord.Attachment] = None, file6: Optional[discord.Attachment] = None, file7: Optional[discord.Attachment] = None, file8: Optional[discord.Attachment] = None, file9: Optional[discord.Attachment] = None, file10: Optional[discord.Attachment] = None, message: Optional[str] = None, picture: Optional[discord.Attachment] = None, ping_everyone: str = "no"):
    await interaction.response.defer(ephemeral=True)
    active = [f for f in [file1, file2, file3, file4, file5, file6, file7, file8, file9, file10] if f]
    try:
        files = [discord.File(fp=io.BytesIO(await a.read()), filename=a.filename) for a in active]
        embed = discord.Embed(title="📦 Bulk Package Consignment Arrived", color=discord.Color.dark_teal(), timestamp=discord.utils.utcnow())
        await channel.send(content="@everyone" if ping_everyone == "yes" else None, embed=embed, files=files)
        await interaction.followup.send(f"✅ {len(files)} files deployed.")
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="bulktxt", description="Bundles and dispatches up to 10 unique text format (.txt) attachments.")
@app_commands.choices(ping_everyone=PING_CHOICES)
async def bulktxt_cmd(interaction: discord.Interaction, channel: discord.TextChannel, file1: discord.Attachment, file2: Optional[discord.Attachment] = None, file3: Optional[discord.Attachment] = None, file4: Optional[discord.Attachment] = None, file5: Optional[discord.Attachment] = None, file6: Optional[discord.Attachment] = None, file7: Optional[discord.Attachment] = None, file8: Optional[discord.Attachment] = None, file9: Optional[discord.Attachment] = None, file10: Optional[discord.Attachment] = None, message: Optional[str] = None, picture: Optional[discord.Attachment] = None, ping_everyone: str = "no"):
    await interaction.response.defer(ephemeral=True)
    active = [f for f in [file1, file2, file3, file4, file5, file6, file7, file8, file9, file10] if f]
    for a in active:
        if not a.filename.lower().endswith('.txt'): return await interaction.followup.send(f"❌ File `{a.filename}` is not `.txt`.")
    try:
        files = [discord.File(fp=io.BytesIO(await a.read()), filename=a.filename) for a in active]
        embed = discord.Embed(title="📝 Bulk TXT Documents Shipment Arrived", color=discord.Color.dark_purple(), timestamp=discord.utils.utcnow())
        await channel.send(content="@everyone" if ping_everyone == "yes" else None, embed=embed, files=files)
        await interaction.followup.send(f"✅ {len(files)} TXT files deployed.")
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="botinfo", description="Reports gateway latency and footprint indicators.")
async def botinfo_cmd(interaction: discord.Interaction):
    embed = discord.Embed(title="🤖 Runtime Statistics", color=discord.Color.brand_green(), timestamp=discord.utils.utcnow())
    embed.add_field(name="Gateway Latency", value=f"`{round(bot.latency * 1000)}ms`", inline=True)
    embed.add_field(name="Guild Footprint", value=f"`{len(bot.guilds)}` connected", inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="startwelcome", description="Locks greeting events directly to a specified channel.")
@app_commands.checks.has_permissions(manage_guild=True)
async def startwelcome_cmd(interaction: discord.Interaction, channel: discord.TextChannel):
    await interaction.response.defer(ephemeral=True)
    bot.welcome_channels[interaction.guild.id] = channel.id
    try: bot.invites[interaction.guild.id] = await interaction.guild.invites()
    except: pass
    await interaction.followup.send(embed=create_embed("✨ Introduction Routing Activated", f"Linked to {channel.mention}.", discord.Color.green()))

@bot.tree.command(name="purge", description="Removes bulk message history tracking data from targeted channels.")
@app_commands.checks.has_permissions(manage_messages=True)
async def purge_cmd(interaction: discord.Interaction, amount: int = 0, channel: Optional[discord.TextChannel] = None):
    await interaction.response.defer(ephemeral=True)
    target = channel if channel else interaction.channel
    try:
        await target.purge(limit=None if amount == 0 else amount)
        await interaction.followup.send(embed=create_embed("🧹 Environment Cleared", f"Target segment cleared inside {target.mention}.", discord.Color.brand_green()))
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="encode", description="Transforms simple string formats securely into raw base64 cryptographic packages.")
async def encode_cmd(interaction: discord.Interaction, content: str, file_name: Optional[str] = "encoded.txt"):
    await interaction.response.defer(ephemeral=True)
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    if not file_name.endswith(".txt"): file_name += ".txt"
    try:
        await interaction.followup.send(embed=create_embed("🔒 Cipher Rendered", "Payload transformed to Base64.", discord.Color.blue()), file=discord.File(fp=io.BytesIO(encoded.encode("utf-8")), filename=file_name))
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="sendwebhook", description="Deploys transient masking webhooks.")
@app_commands.choices(show_sender=[app_commands.Choice(name="Yes", value="yes"), app_commands.Choice(name="No", value="no")], ping_everyone=PING_CHOICES)
async def sendwebhook_cmd(interaction: discord.Interaction, channel: discord.TextChannel, message: str, webhook_name: str, avatar_url: Optional[str] = None, show_sender: str = "no", ping_everyone: str = "no"):
    await interaction.response.defer(ephemeral=True)
    if not channel.permissions_for(interaction.guild.me).manage_webhooks: return await interaction.followup.send("❌ Lack 'Manage Webhooks' flag.")
    content = ("@everyone\n" if ping_everyone == "yes" else "") + (f"{message}\n\n*👤 Source: {interaction.user.mention}*" if show_sender == "yes" else message)
    try:
        wh = await channel.create_webhook(name="Proxy Engine")
        await wh.send(content=content, username=webhook_name, avatar_url=avatar_url)
        await wh.delete()
        await interaction.followup.send(f"✅ Webhook sent to {channel.mention}!")
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="sendannounce", description="Sends the Booster validation layout to the setup verification channel.")
@app_commands.checks.has_permissions(administrator=True)
async def sendannounce_cmd(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    VERIFY_CHANNEL_ID = 1518971603063410753
    channel = interaction.client.get_channel(VERIFY_CHANNEL_ID)
    if not channel:
        try: channel = await interaction.client.fetch_channel(VERIFY_CHANNEL_ID)
        except: return await interaction.followup.send("❌ Channel resolve error.", ephemeral=True)

    embed = discord.Embed(
        title="🌟 Server Booster Verification",
        description="Thank you for supporting our community! 💖\nIf you have boosted our **Main Server**, click the **Verify** button below to sync your status and instantly unlock your exclusive rewards.",
        color=discord.Color.magenta(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text="Global Booster Sync Engine")
    try:
        await channel.send(embed=embed, view=VerifyBoosterView())
        await interaction.followup.send("✅ Booster panel deployed.", ephemeral=True)
    except Exception as e: await interaction.followup.send(f"❌ Error: {e}", ephemeral=True)

@bot.tree.command(name="ticketsetup", description="Deploys the persistent smart category ticketing board to a channel.")
@app_commands.checks.has_permissions(administrator=True)
async def ticketsetup_cmd(interaction: discord.Interaction, channel: discord.TextChannel):
    await interaction.response.defer(ephemeral=True)
    embed = discord.Embed(
        title="📩 Support Dispatch Services Panel",
        description=(
            "If you are encountering network configuration issues, need account sync adjustments, "
            "or wish to file claims/reports, select an appropriate routing category from the dropdown menu below.\n\n"
            "**Operational Rules:**\n"
            "• Flooding or launching spam inquiries leads to systematic penalties.\n"
            "• Created private channels are only accessible to you and network team leads.\n"
            "• Sessions will be entirely transcribed and archived upon completion."
        ),
        color=discord.Color.dark_blue(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(text="Official Advanced Ticket System Infrastructure")
    try:
        await channel.send(embed=embed, view=TicketSetupView())
        await interaction.followup.send(f"✅ Smart Ticketing routing node deployed to {channel.mention}.", ephemeral=True)
    except Exception as e: await interaction.followup.send(f"❌ Interrupt crash: {e}", ephemeral=True)

# ---------------------------------------------------------
# COMMAND 18: /purgetickets (MASS TICKET TERMINATION)
# ---------------------------------------------------------
@bot.tree.command(name="purgetickets", description="Mass terminates and deletes all active ticket workspaces globally.")
@app_commands.checks.has_permissions(administrator=True)
async def purgetickets_cmd(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    deleted_count = 0
    
    # Iterate through all text channels searching for standard ticket prefixes
    for channel in interaction.guild.text_channels:
        if channel.name.startswith("ticket-"):
            try:
                await channel.delete()
                deleted_count += 1
            except discord.Forbidden:
                logger.warning(f"Failed to delete {channel.name} due to missing permissions.")
            except Exception as e:
                logger.error(f"Error purging channel {channel.name}: {e}")
                
    await interaction.followup.send(f"✅ Mass purge protocol complete. Successfully terminated `{deleted_count}` open workspace(s).", ephemeral=True)
    logger.info(f"[PURGE-TICKETS] Executed global wipe command. Deleted {deleted_count} channels.")

# ========================================================================
# 8. SERVER RUN TRIGGER
# ========================================================================
if __name__ == "__main__":
    if not TOKEN:
        logger.critical("Critical Error: DISCORD_TOKEN environment variable is not defined in the Railway panel!")
    else:
        try:
            bot.run(TOKEN)
        except Exception as e:
            logger.critical(f"Unexpected system error while starting the bot: {e}")
