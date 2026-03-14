def get_minutes_and_seconds(seconds):
    minutes = int(seconds // 60)
    seconds_left = seconds - minutes * 60
    seconds_left = round(seconds_left, 2)
    return f"{minutes}:{seconds_left}"