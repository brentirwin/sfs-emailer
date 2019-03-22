from dotmap import DotMap
from .enums import Frequency

def createEmail(frequency, data):

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

        return '\n'.join([
            '## ' + d.date + ' at ' + d.time,
            '*Romeo and Juliet* at ' + d.location,
            '',
            'Drink-up location: ' + d.drink_up,
            '',
            'Drink-up call: ',
            'Ensemble call: ',
            'Fight/dance call: ',
            'Mic check: ',
            'House open: ',
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
        n = DotMap(next_data)
        c = nextCast(current_cast, n.cast)

        return '\n'.join([
            '## Next Show',
            n.date + ' at ' + n.location,
            '',
            '\n'.join(c)
        ])

    def dailyCall():
        d = data[0]
        return '\n\n'.join([
            getDaily(d),
            getNext(d['next_show'], list(d['cast'].values()))
        ])

    def weeklyCall():
        return '\n\n'.join(list(map(getDaily, data)))

    switch = {
        Frequency.DAILY:    dailyCall(),
        Frequency.WEEKLY:   weeklyCall()
    }

    return switch.get(frequency)
