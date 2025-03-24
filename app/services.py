from datetime import date, time
from typing import Optional, Set

def events_overlap(sd1: date, st1: time, d1: int, r1: Optional[Set[int]],
                   sd2: date, st2: time, d2: int, r2: Optional[Set[int]]) -> bool:
    r1 = r1 or set()
    r2 = r2 or set()
    if not r1 and not r2:
        if sd1 != sd2:
            return False
        return time_intervals_overlap(st1, d1, st2, d2)
    if r1 and r2:
        if r1.isdisjoint(r2):
            return False
        return time_intervals_overlap(st1, d1, st2, d2)
    if r1 and not r2:
        if sd2.weekday() not in r1:
            return False
        return time_intervals_overlap(st1, d1, st2, d2)
    if r2 and not r1:
        if sd1.weekday() not in r2:
            return False
        return time_intervals_overlap(st1, d1, st2, d2)

def time_intervals_overlap(st1: time, d1: int, st2: time, d2: int) -> bool:
    s1 = st1.hour * 60 + st1.minute
    s2 = st2.hour * 60 + st2.minute
    e1 = s1 + d1
    e2 = s2 + d2
    return (s1 < e2) and (s2 < e1)
