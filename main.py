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
        "SELECT id FROM UserInfo WHERE id = ?",
        (user_id,)
    )

    rows = cur.fetchall()
    for i in rows:
        alr_exist.append(i[0])
    if user_id not in alr_exist:
        return True
    elif user_id in alr_exist:
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
        **!가입**
        RR Stock 게임 서비스에 가입할 수 있습니다.
                                
        **!탈퇴**
        RR Stock 게임 서비스에서 탈퇴할 수 있습니다.
        
        ''',
        color=0xffc0cb
    )
    embed.set_footer(
        text=f"{ctx.message.author.name} | RR Stock", icon_url=ctx.message.author.avatar_url)
    await ctx.send(embed=embed)


@bot.command()
async def 가입(ctx):
    user_id = ctx.author.id
    con = sqlite3.connect("Test.db", isolation_level=None)
    cur = con.cursor()
    check = check_id(user_id)
    now = datetime.datetime.now()
    datetime_now = now.strftime("%Y-%m-%d %H:%M:%S")

    if check:
        sql = f"""
        INSERT INTO UserInfo VALUES(?, ?, ?, ?, ?)
        """
        cur.execute(
            sql,
            (user_id, 'NULL', 'NULL', 'NULL', datetime_now,)
        )
        embed = discord.Embed(
            title=':wave: 가입',
            description='성공적으로 RR Stock 게임 서비스에 가입되셨습니다.', color=0xffc0cb)
        embed.set_footer(
            text=f"{ctx.message.author.name} | RR Stock", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title=':wave: 가입',
            description='이미 RR Stock 게임 서비스에 가입되어 있습니다.', color=0xff0000)
        embed.set_footer(
            text=f"{ctx.message.author.name} | RR Stock", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    con.close()


@bot.command()
async def 탈퇴(ctx):
    user_id = ctx.author.id
    con = sqlite3.connect("Test.db", isolation_level=None)
    cur = con.cursor()
    check = check_id(user_id)

    if check:
        embed = discord.Embed(
            title=':wave: 탈퇴',
            description='RR Stock 게임 서비스에 가입되어 있지 않습니다.', color=0xff0000)
        embed.set_footer(
            text=f"{ctx.message.author.name} | RR Stock", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        cur.execute(
            "DELETE FROM UserInfo WHERE id = ?",
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

    con.close()


bot.run(os.environ['token'])
