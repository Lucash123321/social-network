import datetime as dt


def year(request):
    time = dt.date.today().year
    return {'year': time}
