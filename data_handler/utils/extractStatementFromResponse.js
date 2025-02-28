const keys = ['verb', 'actor', 'level', 'success', 'score', 'timestamp'];

const level_keys = ['level', 'scenario', 'mission'];

function extractStatementFromResponse(response) {
    try {
        const statement = {};
        let level = null;
        statement['verb'] = response['verb']['display']['en-US'];

        if (
            statement['verb'] != 'launched' &&
            statement['verb'] != 'exited' &&
            statement['verb'] != 'completed'
        ) {
            return [null, null];
        }

        statement['actor'] = response['actor']['name'];
        // statement['target'] = response['target']['definition']['name']['en-US'];

        if (statement['verb'] == 'launched' || statement['verb'] == 'exited') {
            statement['level'] =
                response['target']['definition']['extensions'][
                    'https://spy.lip6.fr/xapi/extensions/value'
                ][0];
        }

        if (statement['verb'] == 'launched') {
            level = {};
            level['level'] =
                response['target']['definition']['extensions'][
                    'https://spy.lip6.fr/xapi/extensions/value'
                ][0];
            level['scenario'] =
                response['target']['definition']['extensions'][
                    'https://spy.lip6.fr/xapi/extensions/context'
                ][0];
            level['mission'] =
                response['target']['definition']['extensions'][
                    'https://w3id.org/xapi/seriousgames/extensions/progress'
                ][0];
        }

        if (statement['verb'] == 'completed') {
            statement['success'] = response['result']['success'];
            statement['score'] = statement['success']
                ? response['result']['extensions'][
                      'https://spy.lip6.fr/xapi/extensions/score'
                  ][0]
                : 0;
        }
        statement['timestamp'] = response['timestamp'];
        return [statement, level];
    } catch (error) {
        console.log(error);
        return [null, null];
    }
}

function statementToRow(statement) {
    if (statement === null) {
        throw new Error('Statement is null');
    }
    const values = [];
    keys.forEach((key) => {
        values.push(statement[key]);
    });
    return values.join(',');
}

function levelToRow(level) {
    if (level === null) {
        throw new Error('Level is null');
    }
    const values = [];
    level_keys.forEach((key) => {
        values.push(level[key]);
    });
    return values.join(',');
}

module.exports = { extractStatementFromResponse, statementToRow, levelToRow };
