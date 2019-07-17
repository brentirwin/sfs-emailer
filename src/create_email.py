from dotmap import DotMap
from .enums import Frequency

def createEmail(frequency, data):

  if frequency == Frequency.DAILY:
    return dailyCall(data)
  if frequency == Frequency.WEEKLY:
    return weeklyCall(data)
''' 
    switch = {
      Frequency.DAILY: dailyCall(data),
      Frequency.WEEKLY: weeklyCall(data)
    }

    return switch.get(frequency)
'''
def assignRoles(roles):
    r = DotMap()
    if roles.alternate == roles.wrangler:
        r[roles.alternate] = 'alt/wr'
    else:
        r[roles.alternate] = 'alt'
        r[roles.wrangler] = 'wr'
    r[roles.drinker] = 'dr'
    return r

def formatRoles(person, role):
    switch = {
        'dr':       '**' + person + ' (dr)**',
        'alt':      '*' + person + ' (alt)*',
        'wr':       '*' + person + ' (wr)*',
        'alt/wr':   '*' + person + ' (alt/wr)*'
    }
    return switch.get(role)

def nextCast(cur, nex):
    nextCast = []
    for member in nex:
        if member in cur:
            nextCast.append('**' + member + '**')
        else:
            nextCast.append(member)
    return nextCast

def getDaily(day_data):
    d = DotMap(day_data)
    c = d.cast.copy()
    r = assignRoles(d.roles)

    ## Format cast

    for member in c:
        if member == 'showrunner':
            break
        if c[member] in r.toDict():
            c[member] = formatRoles(c[member], r[c[member]])

    # Create Markdown email

    return '  \n'.join([
        '## ' + d.date + ' at ' + d.time,
        '*Romeo and Juliet* at ' + d.location,
        '',
        'Drink-up location: ' + d.drink_up,
        '',
        'Drink-up call: ' + d.schedule.drink_up_call,
        'Ensemble call: ' + d.schedule.ensemble_call,
        'Fight/dance call: ' + d.schedule.fight_dance_call,
        'Mic check: ' + d.schedule.mic_check,
        'House open: ' + d.schedule.house_open,
        '',
        'Benvolia - ' + c.benvolia,
        'Juliet - ' + c.juliet,
        'Mercutio - ' + c.mercutio,
        'Romeo - ' + c.romeo,
        'Tybalt - ' + c.tybalt,
        '',
        'Compere - ' + c.compere,
        'Board Op - ' + c.board_op,
        'Showrunner - ' + c.showrunner
    ])

def getNext(next_data, current_cast):
    if next_data:
      n = DotMap(next_data)
      c = nextCast(current_cast, n.cast)

      return '\n'.join([
          '### Next Show',
          n.date + ' at ' + n.location,
          '',
          '  \n'.join(c)
      ])
    return '### Next Show\nThe next show is on the next ROTA.'

def dailyCall(data):
    d = data[0]
    return '\n\n'.join([
        getDaily(d),
        getNext(d['next_show'], list(d['cast'].values()))
    ])

def weeklyCall(data):
    return '\n\n'.join(list(map(getDaily, data)))

