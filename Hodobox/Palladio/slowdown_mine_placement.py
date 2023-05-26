from datetime import datetime, timedelta

BPM = 142
SCROLL_CHANGE = 1/32
T_START_STR = "02:06:826"
T_END_STR = "02:18:657"
T_START = datetime.strptime(T_START_STR, "%M:%S:%f")
T_END = datetime.strptime(T_END_STR, "%M:%S:%f")
BEAT_TIME = (60/BPM)
HALF_BEAT_TIME = BEAT_TIME / 2

def find_next_mine_time(last_mine_seconds):

	cur_time = 0
	cur_speed = 1
	visual_halfbeats = 0

	while True:

		next_slowdown = cur_time + BEAT_TIME 

		if next_slowdown <= last_mine_seconds:
			cur_time = next_slowdown
			cur_speed -= SCROLL_CHANGE
			continue

		visual_halfbeats_needed = 1 - visual_halfbeats

		visual_halfbeats_since = max(last_mine_seconds, cur_time)
		portion_of_beat_left = (next_slowdown - visual_halfbeats_since)/BEAT_TIME
		visual_halfbeats_at_current_speed = cur_speed*portion_of_beat_left*2

		# print(f"for mine at {last_mine_seconds*1000:.1f}, speed {cur_time*1000:.1f} to {next_slowdown*1000:.1f}")
		# print(f"time on visual since {visual_halfbeats_since*1000:.1f}, which is {portion_of_beat_left:.3f} of the beat")
		# print(f" = {visual_halfbeats_at_current_speed:.1f} visual half beats, need {visual_halfbeats_needed:.1f}")

		if visual_halfbeats_needed > visual_halfbeats_at_current_speed:
			visual_halfbeats += visual_halfbeats_at_current_speed
			cur_time = next_slowdown
			cur_speed -= SCROLL_CHANGE
			continue			

		return (visual_halfbeats_needed/visual_halfbeats_at_current_speed)*BEAT_TIME*portion_of_beat_left + visual_halfbeats_since


print(T_START.strftime("%M:%S:%f"))
last_mine_seconds = 0
while True:

	next_mine_seconds = find_next_mine_time(last_mine_seconds)
	next_mine_dt = T_START + timedelta(seconds=next_mine_seconds)

	if next_mine_dt > T_END + timedelta(seconds=0.01):
		break

	print(next_mine_dt.strftime("%M:%S:%f"))

	last_mine_seconds = next_mine_seconds

