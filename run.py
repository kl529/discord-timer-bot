import asyncio, discord
from discord.ext import commands, tasks
import time_check
import config

#prefix 및 토큰 설정
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
token = config.DISCORD_TOKEN

# 로그인 로그 확인
@bot.event
async def on_ready():
	print("We have loggedd in as {0.user}".format(bot))


# 안녕안녕
@bot.command()
async def hello(ctx):
    await ctx.send("hello")


# 해당 명령어가 없을 경우 나오는 메시지
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
    	await ctx.send("명령어를 찾지 못했습니다")


# 엑셀 기본 세팅
@bot.command()
async def setting(ctx):
    time_check.start_timer()


# 공부시간 체크 시작
@bot.command()
async def start(ctx):
    start_time = time_check.start_timer(ctx)
    await ctx.reply(f"{ctx.message.author.name}님 {start_time} 부터 공부를 시작합니다.🔥")


# 공부 시간 체크 종료
@bot.command()
async def end(ctx):
    end_time, hours = time_check.end_timer(ctx)
    if end_time == 0:
        await ctx.reply(f"{ctx.message.author.name}님 시작시간을 안찍었네요. 시간 측정이 안됐습니다.🤤")
    else:
        await ctx.reply(f"{ctx.message.author.name}님 {end_time}까지 {hours} 공부했습니다.🎉")
        await ctx.reply("TIL을 작성해주세요!!!")


# 공부시간 체크하는 명령어
@bot.command()
async def check(ctx):
    total_time, today_time, week_time = time_check.check_status(ctx)
    await ctx.reply(f"{ctx.message.author.name}님 이번 학기에 총 {total_time} 공부를 했습니다.🔥")
    await ctx.reply(f"{ctx.message.author.name}님 오늘 총 {today_time} 공부를 했습니다.🔥")


# 실행
bot.run(token)
