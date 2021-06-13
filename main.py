import os
import sqlite3
import datetime
import discord
from discord.ext import commands


def check_id(user_id):
    alr_exist = []
    con = sqlite3.connect('Test.db', isolation_level=None)
    cur = con.cursor()
    cur.execute(
        "SELECT id FROM UserList WHERE id = ?",
        (user_id,)
    )

    rows = cur.fetchall()
    for i in rows:
        alr_exist.append(i[0])
    # user id 가 이미 있을 경우 True 리턴
    if user_id in alr_exist:
        return True
    else:
        return False
    con.close()


# 명령어 접두어 설정
bot = commands.Bot(command_prefix='!', help_command=None)


@bot.event  # Bot 온라인 접속 이벤트
async def on_ready():
    print(f'로그인 성공 : {bot.user.name}!')
    game = discord.Game("Beta Ver")  # ~~하는중에 표시
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command()
async def 도움(ctx):
    embed = discord.Embed(
        title="도움말",
        description='''
        **!등록**
        RR Stock 게임 서비스에 등록할 수 있습니다.
                                
        **!탈퇴**
        RR Stock 게임 서비스에서 탈퇴할 수 있습니다.
        
        ''',
        color=0xffc0cb
    )
    embed.set_footer(
        text=f"{ctx.message.author.name} | RR Stock", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
async def 등록(ctx, member: discord.Member = None):
    member = ctx.author if not member else member

    con = sqlite3.connect("Test.db", isolation_level=None)
    cur = con.cursor()
    now = datetime.datetime.now()
    datetime_now = now.strftime("%Y-%m-%d %H:%M:%S")

    user_id = ctx.author.id
    check = check_id(user_id)

    if check:
        embed = discord.Embed(
            title=':wave: 등록',
            description='이미 RR Stock 게임 서비스에 등록되어 있습니다.', color=0xff0000)
        embed.set_footer(
            text=f"{ctx.message.author.name} | RR Stock", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        cur.execute(
            "INSERT INTO UserList VALUES(?, ?, ?, ?)",
            (user_id, member.display_name, 0, datetime_now,)
        )
        embed = discord.Embed(
            title=':wave: 등록',
            description='성공적으로 RR Stock 게임 서비스에 등록되셨습니다.', color=0xffc0cb)
        embed.set_footer(
            text=f"{ctx.message.author.name} | RR Stock", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    con.close()


@bot.command()
async def ulist(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    embed = discord.Embed(colour=member.color)
    embed.set_author(name=f"유저정보 - {member}")
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="display name:", value=member.display_name)
    embed.add_field(
        name=f"Roles ({len(roles)}):",
        value=" ".join([role.mention for role in roles])
    )

    await ctx.send(embed=embed)


@bot.command()
async def 탈퇴(ctx):
    user_id = ctx.author.id
    con = sqlite3.connect("Test.db", isolation_level=None)
    cur = con.cursor()
    check = check_id(user_id)

    if check:
        cur.execute(
            "DELETE FROM UserList WHERE id = ?",
            (user_id,)
        )

        embed = discord.Embed(
            title=':wave: 탈퇴',
            description='''
            성공적으로 RR Stock 게임 서비스에서 탈퇴되었습니다.
            `서비스를 다시 이용하시려면 !가입 명령어를 이용해 주세요.`
            ''',
            color=0xffc0cb)
        embed.set_footer(
            text=f"{ctx.message.author.name} | RR Stock", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title=':wave: 탈퇴',
            description='RR Stock 게임 서비스에 가입되어 있지 않습니다.', color=0xff0000)
        embed.set_footer(
            text=f"{ctx.message.author.name} | RR Stock", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    con.close()


@bot.command()
async def 잔고(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    user_id = ctx.author.id
    check = check_id(user_id)

    con = sqlite3.connect("Test.db", isolation_level=None)
    cur = con.cursor()

    if check:
        cur.execute(
            "SELECT balance FROM UserList WHERE id = ?",
            (user_id,)
        )
        # fetch data
        rows = cur.fetchall()
        balance = 1
        for row in rows:
            balance = row[0]

        print(balance)

        embed = discord.Embed(
            title=':wave: 잔고',
            description=f'{member.display_name}님의 잔고: {balance}', color=0xffc0cb)
        embed.set_footer(
            text=f"{ctx.message.author.name} | RR Stock", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    con.close()


@bot.command()
async def 돈주기(ctx, amount):
    con = sqlite3.connect("Test.db", isolation_level=None)
    cur = con.cursor()

    cur.execute(
        "UPDATE UserList SET balance = balance + ?",
        (amount,)
    )
    embed = discord.Embed(
        title=':wave: 돈주기',
        description=f'모든 멤버들에게 +{amount}만큼 돈을 주었습니다.', color=0xffc0cb)
    embed.set_footer(
        text=f"{ctx.message.author.name} | RR Stock", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)

    con.close()


with open("token.txt", 'r') as f:
    bot.run(f.read())

# bot.run(os.environ['token'])
