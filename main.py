import sqlite3
import datetime
import discord
from discord.ext import commands, tasks

def gmser_check(id):
    alr_exist = []
    con = sqlite3.connect(r'파일의 경로 or 파일 이름', isolation_level=None)
    cur = con.cursor()
    cur.execute("SELECT id FROM UserInfo WHERE id = id")
    rows = cur.fetchall()
    for i in rows:
        alr_exist.append(i[0])
    if id not in alr_exist:
        return 0
    elif id in alr_exist:
        return 1
    con.close()


@bot.command()
async def 가입(ctx):
    id = ctx.author.id
    con = sqlite3.connect("Test.db", isolation_level=None)
    cur = con.cursor()
    check = gmser_check(id)
    now = datetime.datetime.now()
    nowDatetime = now.strftime("%Y-%m-%d %H:%M:%S")

    if check == 0:
        null = 'NULL'
        cur.execute("""
        INSERT INTO UserInfo VALUES(id, null, null , nowDatetime)
        """)
        embed = discord.Embed(title=':wave: 가입', description='성공적으로 RG Stock 게임 서비스에 가입되셨습니다.', color=0xffc0cb)
        embed.set_footer(text=f"{ctx.message.author.name} | RG Stock#1639", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    elif check == 1:
        embed = discord.Embed(title=':wave: 가입', description='이미 RG Stock 게임 서비스에 가입되어 있습니다.', color=0xff0000)
        embed.set_footer(text=f"{ctx.message.author.name} | RG Stock#1639", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    con.close()

@bot.command()
aync def 탈퇴(ctx):
    id = ctx.author.id
    con = sqlite3.connect("Test.db", isolation_level= None)
    cur = con.cursor()
    check = gmser_check(id)
    if check == 0 :
        embed = discord.Embed(title=':wave: 탈퇴', description='RG Stock 게임 서비스에 가입되어 있지 않습니다.', color=0xff0000)
        embed.set_footer(text=f"{ctx.message.author.name} | RG Stock#1639", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    elif check == 1:
        cur.execute("DELETE FROM UserInfo WHERE id = ?", (id,))
        embed = discord.Embed(title=':wave: 탈퇴',
                              description='성공적으로 RG Stock 게임 서비스에서 탈퇴되었습니다.\n`서비스를 다시 이용하시려면 !가입 명령어를 이용해 주세요.`',
                              color=0xffc0cb)
        embed.set_footer(text=f"{ctx.message.author.name} | RG Stock#1639", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    con.close()