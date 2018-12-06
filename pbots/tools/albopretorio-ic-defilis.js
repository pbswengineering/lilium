// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

/**
 * albopretorio-ic-defilis
 * ~~~~~~~~~~~~~~~~~~~~~~~
 *
 * Scraper for the register of the I. C. "A. De Filis" (Terni).
 *
 * :copyright: (c) 2018 Paolo Paolo Bernardi.
 * :license: GNU AGPL version 3, see LICENSE for more details.
 */

var casper = require('casper').create();
//var casper = require('casper').create({ verbose: true, logLevel: 'debug' });

var SOURCE = "Albo Pretorio dell'I. C. \"A. De Filis\", Terni";
var START_PAGE = 'http://www.defilisterni.gov.it/wp/wp-includes/albo_pretorio.php';

var data = [];

/**
 * Convert a date from Italian to ISO format
 * @param {string} ita date in Italian format (e.g. "31-12-2019")
 * @returns {string} date in ISO format (e.g. "2019-12-31")
 */
function dateItaToIso(ita) {
    return ita.substring(6, 10) + "-" + ita.substring(3, 5) + "-" + ita.substring(0, 2);
}

/**
 * Find dates in Italian format (dd-mm-yyyy) within a string.
 * @param {string} str
 * @returns {string[]} an array of string dates in Italian format
 */
function findItaDates(str) {
    // > var str = '11-02-2016<br>31-12-2019'
    // > str.match(/\d{2}.{1}\d{2}.{1}\d{4}/g)
    // [ '11-02-2016', '31-12-2019' ]
    return str.match(/\d{2}.{1}\d{2}.{1}\d{4}/g);
}

/**
 * Clean up a publication subject by removing attachment links, attachment sizes and newlines.
 * @param {HTMLElement} td the TD tag that contains the publication subject
 * @returns {string} the publication subject
 */
function cleanSubject(td) {
    // "ALBO PRETORIO SITO WEB<br>DECRETO DI AGGIUDICAZIONE DEFINITIVA 
    // AFFIDAMENTO SERVIZIO CASSA ANNI 2016-2019<br>\n<a title=\"Scarica il file\" 
    // href=\"https://www.villaggioscuola.it/aaa/albopret.php?act=d&amp;cm=tric811001&amp;id=29421&amp;fn=1\">
    // 20160211184907.pdf</a> (34KB)"
    var as = td.getElementsByTagName("a");
    // getElementsByTagName returns a nodelist, which gets updated
    // by removeChild, hence this weird looking loop
    while (as[0]) {
        td.removeChild(as[0]);
    }
    return td.innerHTML
        .replace(/\([0-9a-zA-Z]+\)/g, "")
        .replace(/<br\s*[\/]?>/gi, "\n")
        .trim() // Dispose of the <br> at the end of the stringify
        .replace("\n", " - ");
}

// Main program

casper.userAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X)');
casper.start(START_PAGE);

casper.then(function () {
    // The register is filled via JS
    var that = this;
    this.wait(500, function () {
        data = that.evaluate(function (SOURCE, START_PAGE, dateItaToIso, findItaDates, cleanSubject) {
            var trs = document.getElementsByTagName("tr");
            var res = [];
            // The first tr is the header, skip directly to the second one
            for (var i = 1; i < trs.length; i++) (function () {
                var tds = trs[i].getElementsByTagName("td");
                var dates = findItaDates(tds[3].innerHTML);
                var pub = {
                    source: SOURCE,
                    publisher: 'I. C. "A. De Filis", Terni',
                    url: START_PAGE,
                    number: tds[0].innerHTML,
                    date_start: dateItaToIso(dates[0]), // or dateItaToIso(tds[1].innerHTML)
                    date_end: dateItaToIso(dates[1]),
                    attachments: []
                };
                var as = tds[2].getElementsByTagName("a");
                for (var k = 0; k < as.length; k++) (function () {
                    pub.attachments.push({
                        name: as[k].innerHTML,
                        url: as[k].href // .getAttribute("href") gets the literal value of the attribute
                    });
                })();
                // This call removes the anchors, therefore it must be
                // called after searching for attachments
                pub.subject = cleanSubject(tds[2]);
                // Usually the I. C. "A. De Filis" publication subject is something like:
                // PUBLICATION TYPE - PUBLICATION SUBJECT
                var dashPosition = pub.subject.indexOf(" - ");
                if (dashPosition !== -1) {
                    // I intentionally not remove the publication type from the subject, as
                    // the publication mail template doesn't use it and it still makes the
                    // subject clearer, in this case
                    pub.type = pub.subject.substring(0, dashPosition);
                }
                res.push(pub);
            })();
            return res;
        }, SOURCE, START_PAGE, dateItaToIso, findItaDates, cleanSubject);
    });
});

casper.run(function () {
    console.log(JSON.stringify(data, null, 2));
    casper.exit();
});
