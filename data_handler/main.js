const TinCan = require('tincanjs');
const fs = require('fs');
const Query = require('./utils/query');
const {
    extractStatementFromResponse,
    statementToRow,
    levelToRow,
} = require('./utils/extractStatementFromResponse');
const getCurrentTimestamp = require('./utils/time');
const configs = require('../configs/configs');

const myTinCan = new TinCan();

myTinCan.lrs = new TinCan.LRS({
    endpoint: configs.endpoint,
    username: configs.username,
    password: configs.password,
});

let sessionData = [];
let levels = [];
const batch_size = 10000;
const fetch_levels = false;
const verbs = ['launched', 'exited', 'completed'];

const query = new Query(10000);

if (fs.existsSync('./last_run')) {
    const timestamp = fs.readFileSync('./last_run', 'utf8');
    query.setSince(timestamp);
} else {
    const current_timestamp = getCurrentTimestamp();
    fs.writeFileSync('./last_run', current_timestamp);
}

if (!fs.existsSync(configs.output_file)) {
    fs.writeFileSync(
        configs.output_file,
        'verb,player,level,success,score,timestamp\n'
    );
}

if (fetch_levels && !fs.existsSync(configs.levels_file)) {
    fs.writeFileSync(configs.levels_file, 'level,scenario,mission\n');
}

function processLrsResult(err, response, myTinCanLRS) {
    if (err !== null) {
        console.log('Failed to query statements: ' + err);
        return;
    }

    if (sessionData.length > batch_size) {
        fs.appendFileSync(configs.output_file, sessionData.join('\n') + '\n');
        console.log('Saved statements to file: ' + sessionData.length);
        sessionData = [];
    }

    if (fetch_levels && levels.length > batch_size) {
        fs.appendFileSync(configs.levels_file, levels.join('\n') + '\n');
        console.log('Saved levels to file: ' + levels.length);
        levels = [];
    }

    console.log('Statements received: ' + response.statements.length);
    if (response.statements.length > 0) {
        // enregistrement du statement
        for (let i = 0; i < response.statements.length; i++) {
            const [statement, level] = extractStatementFromResponse(
                response.statements[i]
            );
            if (statement !== null) {
                sessionData.push(statementToRow(statement));
            }
            if (fetch_levels && level !== null) {
                levels.push(levelToRow(level));
            }
        }

        // Vérifier si l'on doit récupérer plus de données
        if (response.more !== null && response.more !== '') {
            console.log('Require to fetch more data');
            myTinCanLRS.moreStatements({
                url: response.more,
                callback: function (err, response) {
                    processLrsResult(err, response, myTinCanLRS);
                },
            });
        } else {
            fs.appendFileSync(
                configs.output_file,
                sessionData.join('\n') + '\n'
            );
            console.log('Saved statements to file: ' + sessionData.length);
            sessionData = [];
            if (fetch_levels) {
                fs.appendFileSync(
                    configs.levels_file,
                    levels.join('\n') + '\n'
                );
                console.log('Saved levels to file: ' + levels.length);
                levels = [];
            }
        }
    } else {
        console.log('No statements received');
    }
}


verbs.forEach((verb) => {
    myTinCan.lrs.queryStatements({
        params: query.setVerb(verb),
        callback: function (err, response) {
            processLrsResult(err, response, myTinCan.lrs);
        },
    });
});
