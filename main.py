import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)

@bot.event
async def on_ready():
    print("Bot inicializado.")
    
@bot.command()
@commands.has_permissions(manage_roles=True)
async def addcargo(ctx, membro: discord.Member, *, nome_cargo):

    cargo = discord.utils.get(ctx.guild.roles, name=nome_cargo)
    
    if cargo is None:
        await ctx.send(f"Não achei o cargo '{nome_cargo}'.")
        return
    
    try:

        await membro.add_roles(cargo)
        await ctx.send(f"{membro.mention} recebeu o cargo '{cargo.name}'!")
    except discord.Forbidden:
        await ctx.send("Não tenho permissão para adicionar esse cargo.")
    except Exception as erro:
        await ctx.send(f"Ocorreu um erro: {erro}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removercargo(ctx, membro: discord.Member, *, nome_cargo):

    cargo = discord.utils.get(ctx.guild.roles, name=nome_cargo)

    if cargo is None:
        await ctx.send(f"Não achei o cargo com o nome {nome_cargo}.")
        return
    try:

        await membro.remove_roles(cargo)
        await ctx.send(f"O cargo '{cargo.name}' foi removido com sucesso do usuario {membro.mention}.")
    except discord.Forbidden:
        await ctx.send(f"Não foi possivel remover o cargo.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, membro: discord.Member, *, motivo="Motivo não especificado."):
    try:
        await membro.ban(reason=motivo)
        await ctx.send(f"{membro.mention} foi banido do servidor. \nMotivo: {motivo}")
    except discord.Forbidden:
        await ctx.send("Não tenho permissão para banir esse usuário.")
    except Exception as erro:
        await ctx.send(f"Ocorreu um erro: {erro}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, membro_id: int):
    async for ban_entry in ctx.guild.bans():
        user = ban_entry.user
        if user.id == membro_id:
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} foi desbanido do servidor.")
            return

    await ctx.send(f"Usuário com ID {membro_id} não está banido.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, membro: discord.Member, *, motivo="Motivo não especificado."):
    try:
        await membro.kick(reason=motivo)
        await ctx.send(f"{membro.mention} foi expulso do servidor.\nMotivo:{motivo}")
    except discord.Forbidden:
        await ctx.send("Não tenho permissão para expulsar esse usuário.")
    except Exception as error:
        await ctx.send(f"Ocorreu um erro: {error}")

bot.run("DISCORD_TOKEN")