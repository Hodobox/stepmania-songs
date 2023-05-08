from datetime import datetime, timedelta
from copy import deepcopy

#ok this is very bad code at this point, turn away now

BPM = 142
SCROLL_CHANGE = (1-0.125)/12
T_LAST_MINE_STR = "02:18:164"
T_FIRST_BEAT_STR = "02:18:235"
T_END_BEAT_STR = "02:19:925"
T_HOLD_FINISH_STR = "02:20:347"
T_LAST_MINE = datetime.strptime(T_LAST_MINE_STR, "%M:%S:%f")
T_FIRST_BEAT = datetime.strptime(T_FIRST_BEAT_STR, "%M:%S:%f")
T_END_BEAT = datetime.strptime(T_END_BEAT_STR, "%M:%S:%f")
T_HOLD_FINISH = datetime.strptime(T_HOLD_FINISH_STR, "%M:%S:%f")
BEAT_TIME = (60/BPM)
HALF_BEAT_TIME = BEAT_TIME / 2

def get_time(dt):
	return (dt-T_LAST_MINE).total_seconds()

def get_dt(t):
	return T_LAST_MINE + timedelta(seconds=t)

def compute_scroll_speed_timestamps():
	res = []
	t_speedup_start = T_FIRST_BEAT + timedelta(seconds=BEAT_TIME)
	scroll_speed = 0.125
	t_passed = 0

	while scroll_speed <= 1:
		t = get_time(t_speedup_start + timedelta(seconds=t_passed))
		res.append( (t, scroll_speed) )

		scroll_speed += SCROLL_CHANGE
		t_passed += (BEAT_TIME*3)/12

	res.append( (get_time(T_END_BEAT) + 1000, 1) )

	return res



SCROLL_SPEEDS = [ (0, 0.1875), (get_time(T_FIRST_BEAT), 0.15625)] + compute_scroll_speed_timestamps()



def find_next_mine_time(last_mine_seconds):

	cur_time = 0
	cur_speed = SCROLL_SPEEDS[0][1]
	visual_halfbeats = 0

	for next_change, scroll_speed in SCROLL_SPEEDS:

		if next_change <= last_mine_seconds:
			cur_time = next_change
			cur_speed = scroll_speed
			continue

		visual_halfbeats_needed = 1 - visual_halfbeats

		visual_halfbeats_since = max(last_mine_seconds, cur_time)
		time_left = next_change - visual_halfbeats_since
		portion_of_beat_left = time_left / BEAT_TIME
		visual_halfbeats_at_current_speed = cur_speed*portion_of_beat_left*2

		# print(f"for mine at {last_mine_seconds*1000:.1f}, speed {cur_time*1000:.1f} to {next_slowdown*1000:.1f}")
		# print(f"time on visual since {visual_halfbeats_since*1000:.1f}, which is {portion_of_beat_left:.3f} of the beat")
		# print(f" = {visual_halfbeats_at_current_speed:.1f} visual half beats, need {visual_halfbeats_needed:.1f}")

		if visual_halfbeats_needed > visual_halfbeats_at_current_speed:
			visual_halfbeats += visual_halfbeats_at_current_speed
			cur_time = next_change
			cur_speed = scroll_speed
			continue			

		return (visual_halfbeats_needed/visual_halfbeats_at_current_speed)*time_left + visual_halfbeats_since


print(T_LAST_MINE.strftime("%M:%S:%f"))
last_mine_seconds = 0
while True:

	next_mine_seconds = find_next_mine_time(last_mine_seconds)
	next_mine_dt = get_dt(next_mine_seconds)

	if next_mine_seconds >  get_time(T_HOLD_FINISH+ timedelta(seconds=0.01)):
		break

	print(next_mine_dt.strftime("%M:%S:%f"))

	last_mine_seconds = next_mine_seconds

