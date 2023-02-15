import openpyxl as op
import time
import math
from datetime import datetime
from pytz import timezone

GOAL = {
    'JW': 10,
    'SM' : 10,
    'KO' : 10,
    'HM' : 10
}

# 1. 현재 시간 체크
# 파일 읽어서, 본인 이름에 대한 시간들을 모두 더해서 보여주기 + 일주일 목표 + 최종 목표
# 결과값 - 오늘 공부시간 / 이번주 공부시간 / 이번주 공부 목표 // 총 시간 / 최종 총 시간
def check_status(ctx):
    wb = op.load_workbook(r"result.xlsx") #Workbook 객체 생성
    ws = wb.active #활성화 된 시트 객체 생성

    total_time = 0
    today_time = 0
    week_time = 0

    semester = math.ceil(time.localtime().tm_mon / 3.0)

    for row in ws.rows:
        if ctx.message.author.name == row[1].value and semester == row[0].value and row[5].value is not None:
            total_time += row[5].value
            if row[2].value == time.strftime('%Y%m%d', time.localtime()):
                today_time += row[5].value

    return total_time, today_time, week_time


# 2. 시간 체크 시작하는 함수
def start_timer(ctx):

    semester = math.ceil(time.localtime().tm_mon / 3.0) #학기 체크
    author_name = ctx.message.author.name #이름
    now = datetime.now(timezone('Asia/Seoul'))
    date = now.strftime('%Y%m%d') # 날짜
    start_time = now.strftime('%Y-%m-%d %H:%M:%S') #시간

    wb = op.load_workbook(r"result.xlsx") #Workbook 객체 생성
    ws = wb.active #활성화 된 시트 객체 생성

    ws.append([semester, author_name, date, start_time]) # 열 추가
    wb.save(r"result.xlsx")

    return start_time


# 3. 시간 체크 종료하는 함수
def end_timer(ctx):

    wb = op.load_workbook(r"result.xlsx") #Workbook 객체 생성
    ws = wb.active #활성화 된 시트 객체 생성

    end_time = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S') # 종료 시간

    for row in ws.rows:
        if row[1].value == ctx.message.author.name and row[4].value is None: # 시작을 했고, 닉네임이 같은 유저가 있으면
            gap = (datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') - datetime.strptime(row[3].value, '%Y-%m-%d %H:%M:%S')).seconds
            row[4].value = end_time #종료시간을 넣어줌.
            row[5].value = gap #얼마나 공부했는지 넣어줌

            wb.save(r"result.xlsx")

            return end_time, time_stamp_to_time(gap)

    return 0,0


#초기 엑셀 세팅 -> 필요 없음.
def setting():
    wb = op.load_workbook(r"result.xlsx") #Workbook 객체 생성
    ws = wb.active #활성화 된 시트 객체 생성 

    col_names = ['학기', '이름', '날짜', '시작시간', '종료시간', '공부시간']
    for seq, name in enumerate(col_names):
        ws.cell(row=1, column=seq+1, value=name)

    wb.save(r"result.xlsx") #결과 엑셀파일 저장


# timestamp를 시간 / 분 / 초로 변환하는 함수
def time_stamp_to_time(ts, seperate=False):
    hour = ts // 3600
    ts -= hour*3600
    minute = ts // 60
    second = ts - minute*60 

    if seperate:
        return (int(hour), int(minute), int(second))

    return_string = ''
    return_string += f'{int(hour)}시간 ' if hour != 0 else ''
    return_string += f'{int(minute)}분 ' if minute != 0 else ''
    return_string += f'{int(second)}초 ' if second != 0 else ''

    return f'{int(hour)}시간 {int(minute)}분 {int(second)}초'

