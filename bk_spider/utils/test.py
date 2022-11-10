import datetime

t = ["11", "22", "33", 15.99, 27.88]

# print([x for x in t if x == "11"])
#
# print(float("".join(["11.233"])) if 2 > 2 else 0.00)

flag_time = datetime.datetime.strptime("2022-02-20 20:56:00.522741", "%Y-%m-%d %H:%M:%S.%f")

print(flag_time)

while 1:
    now_time = datetime.datetime.now()
    if now_time > flag_time:
        print("执行代码----")
        break
    else:
        print("还未到指定时间")
        print(now_time.strftime("%Y-%m-%d %H:%M:%S.%f"))
