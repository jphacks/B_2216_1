from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from .schemas import ContinuousSittingTime, ContinuousSittingTimeCreate, TimeData
from .crud import find_continuous_sitting, create_continuous_sitting, update_continuous_sitting, get_user
from .apns import call_apns_api

def handle_timedata(db: Session, timedata: TimeData, duration_min: int = 2 * 60):
    is_sitting = timedata.value > 10

    prev_sitting = find_continuous_sitting(db, timedata.id)
    if prev_sitting == None:
        new_sitting = ContinuousSittingTime(
            user_id=timedata.id, last_stand=datetime.now(), last_notify=datetime.now())
        create_continuous_sitting(db, new_sitting)

    if is_sitting:
        last_stand = prev_sitting.last_stand
        last_notify = prev_sitting.last_notify

        if check_notify(timedata.timestamp, last_stand, last_notify, duration_min):
            # if we should send notify
            delta = timedata.timestamp - last_stand
            notify(db, timedata.id, delta)
            last_notify = timedata.timestamp

        new_sitting = ContinuousSittingTime(
            user_id=timedata.id, last_stand=last_stand, last_notify=last_notify)

        update_continuous_sitting(db, new_sitting)
    else:
        last_notify = prev_sitting.last_notify
        last_stand = timedata.timestamp
        new_sitting = ContinuousSittingTime(
            user_id=timedata.id, last_stand=last_stand, last_notify=last_notify)
        update_continuous_sitting(db, new_sitting)


def check_notify(now: datetime, last_stand: datetime, last_notify: datetime, duration_min: int) -> bool:
    duration = timedelta(minutes=duration_min)
    delta = min(now - last_stand, now - last_notify)
    if delta > duration:
        return True
    else:
        return False

def notify(db: Session, user_id: int, time: timedelta):
    user = get_user(db, user_id)
    device_token = user.device_token
    hour = time.total_seconds() / (60 * 60) # seconds -> hour
    
    title = '少し休憩しましょう'
    body = f'{int(hour):}時間連続で座っています'

    res = call_apns_api(device_token, title=title, body=body)

    if res.status_code == 200:
        return True
    else:
        return False
