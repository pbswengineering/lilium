// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

/**
 * albopretorio-comune-acquasparta
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 *
 * Scraper for the register of the "Comune di Acquasparta".
 *
 * :copyright: (c) 2018 Paolo Paolo Bernardi.
 * :license: GNU AGPL version 3, see LICENSE for more details.
 */

var casper = require('casper').create();
//var casper = require('casper').create({ verbose: true, logLevel: 'debug' });

var SOURCE = "Albo Pretorio del Comune di Acquasparta";
var BASE_URL = 'http://asp.urbi.it/urbi/progs/urp/';
var START_PAGE = BASE_URL + 'ur1ME002.sto?DB_NAME=n1201560';
var TEMPLATE_DETAIL = START_PAGE + '&StwEvent=102&IdMePubblica=${ID_PUB}&Archivio=${ARCHIVIO}';

var data = [];

/**
 * Returns the links present in the page that have the "bottoneprova" CSS class.
 * @returns {string[]} the links relative URLs
 */
function getLinks() {
    var links = document.querySelectorAll('a.bottoneprova');
    return Array.prototype.map.call(links, function (e) {
        return e.getAttribute('href');
    });
}

/**
 * Return the publications in JSON format, including their attachments.
 * @param {string} source name of the data source
 * @returns {{source: *, attachments: Array}}
 */
function getPublicationData(source, baseUrl) {
    /**
     * Convert the label from the website to a standard PBOTS publication label.
     * @param {string} label
     * @returns {string}
     */
    function standardizeLabel(label) {
        var map = {
            "Ente Mittente": "publisher",
            "In Pubblicazione dal": "date_start",
            "al": "date_end",
            "N.Reg": "number",
            "Oggetto": "subject",
            "Tipologia": "type"
        };
        if (label in map) {
            return map[label];
        } else {
            return label.toLowerCase();
        }
    }

    var res = {
        source: source,
        attachments: []
    };

    $('.testata').each(function (k, v) {
        var label = $(v).find('.infolabel').text();
        var value = $(v).find('.infodato').text();
        res[standardizeLabel(label)] = value;
    });

    $('.dettaglio').each(function (k, v) {
        var labels = $(v).find('.infolabel');
        var datos = $(v).find('.infodato');
        for (var i = 0; i < labels.length; i++) {
            res[standardizeLabel($(labels[i]).text())] = $(datos[i]).text();
        }
    });

    $('tr').each(function (k, v) {
        var tds = $(v).find('td');
        var label = $(tds[0]).text();
        if (!label) {
            return; // Skip headers
        }
        var url = baseUrl + $(tds[1]).find('a').attr('href');
        res.attachments.push({
            name: label,
            url: url
        });
    });
    return res;
}

/**
 * Convert JS function calls to URLs.
 * @param {string} js the JavaScript function call (e.g. "javascript:Dettagli(10651,'')")
 * @returns {string} the URL.
 */
function jsToLink(js) {
    // e.g. javascript:Dettagli(10651,'');
    var idPub = js.split('(')[1].split(',')[0];
    var archi = js.split("'")[1];
    return TEMPLATE_DETAIL
        .replace('${ID_PUB}', idPub)
        .replace('${ARCHIVIO}', archi);
}

// Main program

casper.userAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X)');
casper.start(START_PAGE);

casper.then(function () {
    this.evaluate(function () {
        $('fieldset.generica:nth-child(3) > div:nth-child(2) > div:nth-child(2) > input:nth-child(1)').click()
    });
    this.wait(500);
    this.evaluate(function () {
        eval($('.pulsante').attr('href'));
    });
});

casper.then(function () {
    var that = this;
    var jsLinks = this.evaluate(getLinks);
    for (var i = 0; i < jsLinks.length; i++) (function () {
        var converted = jsToLink(jsLinks[i]);
        that.thenOpen(converted, function () {
            var pub = this.evaluate(getPublicationData, SOURCE, BASE_URL);
            pub.url = converted;
            data.push(pub);
        });
    })();
});

casper.run(function () {
    console.log(JSON.stringify(data));
    casper.exit();
});
