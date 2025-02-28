const TinCan = require('tincanjs');

class Query {
    constructor(limit = 1000) {
        this.limit = limit;
    }

    setActor(actor) {
        this.agent = new TinCan.Agent({
            account: {
                homePage: 'https://www.lip6.fr/mocah/',
                name: actor,
            },
        });
        return this;
    }

    setVerb(verb) {
        this.verb = new TinCan.Verb({
            id: `http://adlnet.gov/expapi/verbs/${verb}`,
        });
        return this;
    }

    setLimit(limit) {
        this.limit = limit;
        return this;
    }
    setSince(timestamp) {
        let [date, time] = timestamp.split(' ');

        if (time === undefined) {
            time = '00:00';
        }

        const [day, month, year] = date.split('/');
        const [hours, minutes] = time.split(':');

        this.since = new Date(
            year,
            month - 1,
            day,
            hours,
            minutes
        ).toISOString();
        // console.log(this.since);
        return this;
    }
    setUntil(timestamp) {
        let [date, time] = timestamp.split(' ');

        if (time === undefined) {
            time = '00:00';
        }

        const [day, month, year] = date.split('/');
        const [hours, minutes] = time.split(':');

        this.until = new Date(
            year,
            month - 1,
            day,
            hours,
            minutes
        ).toISOString();
        // console.log(this.until);
        return this;
    }
}

module.exports = Query;
