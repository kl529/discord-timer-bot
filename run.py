import asyncio, discord
from discord.ext import commands, tasks
import time_check

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
token = 'MTA1Nzk3MDg2Mzg2NzE4NzI4MA.GSQXxd.UAM_9BDhnfLwJ3uSiopTpDNdzqBfQOl6NoFZ3s'

@bot.event
async def on_ready():
	print("We have loggedd in as {0.user}".format(bot))

@bot.command()
async def hello(ctx):
    await ctx.send("hello")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
    	await ctx.send("명령어를 찾지 못했습니다")

@bot.command()
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await ctx.send(channel)
        await channel.connect()
    else:
    	await ctx.send("음성채널 없음")

@bot.command()
async def leave(ctx):
	await bot.voice_clients[0].disconnect()

@bot.command()
async def setting(ctx):
    time_check.start_timer()

@bot.command()
async def start(ctx):
    start_time = time_check.start_timer(ctx)
    await ctx.reply(f"{ctx.message.author.name}님 {start_time} 부터 공부를 시작합니다.🔥")

@bot.command()
async def end(ctx):
    end_time, hours = time_check.end_timer(ctx)
    if end_time == 0:
        await ctx.reply(f"{ctx.message.author.name}님 시작시간을 안찍었네요. 시간 측정이 안됐습니다.🤤")
    else:
        await ctx.reply(f"{ctx.message.author.name}님 {end_time}까지 {hours} 공부했습니다.🎉")
        await ctx.reply("TIL을 작성해주세요!!!")

@bot.command()
async def check(ctx):
    total_time, today_time, week_time = time_check.check_status(ctx)
    await ctx.reply(f"{ctx.message.author.name}님 이번 학기에 총 {total_time} 공부를 했습니다.🔥")
    await ctx.reply(f"{ctx.message.author.name}님 오늘 총 {today_time} 공부를 했습니다.🔥")

@bot.event
async def on_typing(channel, user, when):
    print(channel) # 채널 이름
    print(user) # 유저 닉네임
    print(when) # 날짜 및 시간



# @bot.event
# async def on_ready():
#     check_goals()

# @tasks.loop(seconds=5)
# async def check_goals():
#     await bot.send('wow')


bot.run(token)