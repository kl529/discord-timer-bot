import  openpyxl  as  op
import time
import math
from datetime import datetime

GOAL = {

}

# 파일 읽기. -> 이름 / 날짜 / 시작시간 / 종료시간 행이 추가 됨.

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

    return time_stamp_to_time(total_time), time_stamp_to_time(today_time), time_stamp_to_time(week_time)

# 2. 시작
def start_timer(ctx):
    semester = math.ceil(time.localtime().tm_mon / 3.0)
    author_name = ctx.message.author.name
    now = time.localtime()
    date = time.strftime('%Y%m%d', now)
    start_time = time.strftime('%Y-%m-%d %I:%M:%S', now)


    wb = op.load_workbook(r"result.xlsx") #Workbook 객체 생성
    ws = wb.active #활성화 된 시트 객체 생성

    ws.append([semester, author_name, date, start_time])
    wb.save(r"result.xlsx")
    return start_time


# 3. 종료
def end_timer(ctx):

    wb = op.load_workbook(r"result.xlsx") #Workbook 객체 생성
    ws = wb.active #활성화 된 시트 객체 생성

    now = time.localtime()
    end_time = time.strftime('%Y-%m-%d %I:%M:%S', now)

    for row in ws.rows:
        if row[1].value == ctx.message.author.name and row[4].value is None: # 시작을 했다면
            row[4].value = end_time #종료를 찍고 시간 계산 후 끝내기
            gap = time.mktime(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').timetuple()) - time.mktime(datetime.strptime(row[3].value, '%Y-%m-%d %H:%M:%S').timetuple())
            row[5].value = gap
            wb.save(r"result.xlsx")
            return end_time, time_stamp_to_time(gap)

    return 0,0

#초기 엑셀 세팅
def setting():
    wb = op.load_workbook(r"result.xlsx") #Workbook 객체 생성
    ws = wb.active #활성화 된 시트 객체 생성 

    col_names = ['학기', '이름', '날짜', '시작시간', '종료시간', '공부시간']
    for seq, name in enumerate(col_names):
        ws.cell(row=1, column=seq+1, value=name)

    wb.save(r"result.xlsx") #결과 엑셀파일 저장

def time_stamp_to_time(ts):
    hour = 0
    minute = ts // 60
    if minute >= 60:
        hour = minute // 60
        minute-= 60 * hour
    second = ts % 60
    return f'{int(hour)}시간 {int(minute)}분 {int(second)}초'