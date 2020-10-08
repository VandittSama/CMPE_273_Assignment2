import yaml
import sys
import schedule
import time

CONST_INVOKE = "::invoke"
CONST_PRINT = "::print"
CONST_DAYS = {'0': 'sunday', '1': 'monday', '2': 'tuesday', '3': 'wednesday', '4': 'thursday', '5': 'friday', '6': 'saturday', '7': 'sunday'}
cmd = ""
is_scheduled = False

def executeStep(step):
    print("to code")

def job():
    print("job started")
    print("\n")
    print(contents)
    print("\n")

def weekDayJob():
    #Setting minutely execution for a particular day
    schedule.every(int(minute)).minutes.do(job)
    

# file needs to be opened in both scheduled and manual runs
with open(str(sys.argv[1]), 'r') as stream:
    try:
        contents = yaml.safe_load(stream)
        #read the scheduler and set automatic invocation of job
        when = contents['Scheduler']['when']
        minuteHourDay = when.split()
        minute = minuteHourDay[0]
        hour = minuteHourDay[1]
        day = minuteHourDay[2]

        if minute != "*" and int(minute) < 10:
            minute = "0" + minute

        if hour != "*" and int(hour) < 10:
            hour = "0" + hour
        
        if day == "*":
            if hour == "*":
                if minute == "*":
                    # -- * * * --     (not valid)
                    print("all stars, invalid")
                
                elif int(minute) >= 0 and int(minute) <= 59:
                    # -- 5 * * --     (run every 5 minutes)
                    print("only minute provided")
                    schedule.every(int(minute)).minutes.do(job)
                    is_scheduled = True

            elif int(hour) >= 0 and int(hour) <= 23:
                if minute == "*":
                    # -- * 2 * --     (run everyday at 2:00)
                    print("only hour provided")
                    schedule.every().day.at("%d:00"%int(hour)).do(job)
                    is_scheduled = True

                elif int(minute) >= 0 and int(minute) <= 59:
                    # -- 5 1 * --     (run (everyday) at 1:05)
                    print("minute and hour provided")
                    schedule.every().day.at("%d:%d"%(int(hour),int(minute))).do(job)
                    is_scheduled = True

        elif int(day) >= 0 and int(day) <= 7:
            if hour == "*":
                if minute == "*":
                    # -- * * 3 -- (run every wednesday at 00:00)
                    print("only day provided")
                    cmd = "schedule.every()." + CONST_DAYS[day] + ".at(\"00:00\").do(job)"
                    is_scheduled = True

                elif int(minute) >= 0 and int(minute) <= 59:
                    # -- 5 * 2 -- (run every 5 minutes on every tuesday -- not mentioned)
                    print("minute and day provided")
                    cmd = "schedule.every()." + CONST_DAYS[day] + ".at(\"00:00\").do(weekDayJob)"
                    is_scheduled = True

            elif int(hour) >= 0 and int(hour) <= 23:
                if minute == "*":
                    # -- * 15 4 --    (run every thursday at 15:00 -- not mentioned)
                    print("hour and day provided")
                    cmd = "schedule.every()." + CONST_DAYS[day] + ".at(\"" + hour + ":00\").do(job)"
                    is_scheduled = True

                elif int(minute) >= 0 and int(minute) <= 59:
                    # -- 10 23 1 --       (run every monday at 23:10)
                    print("everything provided")
                    cmd = "schedule.every()." + CONST_DAYS[day] + ".at(\"" + hour + ":" + minute + "\").do(job)"
                    is_scheduled = True

        # schedule.every(5).seconds.do(job)
        if is_scheduled is True and cmd:
            #print(cmd)
            exec(cmd)
        while is_scheduled is True:
            schedule.run_pending()
            time.sleep(1)

    except yaml.YAMLError as exc:
        print(exc)