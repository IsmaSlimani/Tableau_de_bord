def format_timedelta(td):
    total_seconds = int(td.total_seconds())

    hours = total_seconds // 3600
    remaining_seconds = total_seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    def pluralize(n, singular, plural):
        if n == 1:
            return f"{n} {singular}"
        else:
            return f"{n} {plural}"

    parts = []
    if hours > 0:
        parts.append(pluralize(hours, "hour", "hours"))
    if minutes > 0:
        parts.append(pluralize(minutes, "minute", "minutes"))
    if seconds > 0:
        parts.append(pluralize(seconds, "second", "seconds"))

    return ' '.join(parts)
