// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

/**
 * bollettino-regione-umbria
 * ~~~~~~~~~~~~~~~~~~~~~~~~~
 *
 * Scraper for the register of the Region of Umbria (Italy).
 *
 * @copyright (c) 2018 Paolo Paolo Bernardi.
 * @license GNU AGPL version 3, see LICENSE for more details.
 */

var PUBLISHER = "Regione Umbria";
var SOURCE = "Bollettino ufficiale della Regione Umbria";

var system = require("system");
var args = system.args;
var page = new WebPage();
var stepIndex = 0;
var loadInProgress = false;

// This is required, since by default console.error writes to stdout
console.error = function () {
    system.stderr.write(Array.prototype.join.call(arguments, " ") + "\n");
};

// Again, avoid writing to stdout anything but the JSON scraping output
page.onConsoleMessage = function (msg) {
    console.error(msg);
};

// Keep track of page loading: it just started
page.onLoadStarted = function () {
    loadInProgress = true;
};

// Keep track of page loading: now it is over
page.onLoadFinished = function () {
    loadInProgress = false;
};

/**
 * Scrape a TD element containing a bulletin and return its metadata as a JSON object, including the attachments.
 * @param {HTMLElement} td
 * @param {string} source
 * @param {string} publisher
 * @returns {{publisher: *, source: *, subject: *, attachments: Array}}
 */
function scrapeBulletin(td, source, publisher) {
    function cleanName(name) {
        return name.trim().replace("- ", "");
    }

    var subject = td.innerText.trim();
    var childrenTds = td.querySelectorAll("table td");
    var docs = [];
    for (var i = 0; i < childrenTds.length; i++) (function () {
        var child = childrenTds.item(i);
        if (i % 2 === 0) { // Even TDs are the PDF file titles
            docs.push({
                name: cleanName(child.innerText)
            });
        } else { // Odd TDs are links to PDF files
            docs[docs.length - 1].td = child;
        }
    })();
    // Remove empty TDs and digitally signed bulletins
    docs = docs.filter(function (doc) {
        return doc.name && !doc.name.match(/firmato(.*)digitalmente/);
    });
    docs.map(function (doc) {
        var as = doc.td.querySelectorAll("a");
        var a = as.item(as.length - 1); // always the last
        doc.url = "http://www2.regione.umbria.it/bollettini/" + a.getAttribute("href");
        delete doc.td;
    });
    return {
        publisher: publisher,
        source: source,
        subject: subject,
        attachments: docs
    };
}

/**
 * Scraping functions to be executed sequentially.
 * @type {function[]}
 */
var steps = [
    /**
     * Load the main bulletin page.
     */
    function () {
        page.open("http://www2.regione.umbria.it/bollettini/consultazione.aspx?parte=" + serie);
    },
    /**
     * Select the bulletin month (all months).
     */
    function () {
        page.evaluate(function () {
            document.querySelector("#cphBody_SelezionaMese").click();
        });
    },
    /**
     * For each result, add the scraped JSON object to the output.
     * @returns {Array}
     */
    function () {
        // Output content of page to stdout after form has been submitted
        return page.evaluate(function (scrapeBulletin, source, publisher) {
            var pannelloRisultati = document.querySelector("#cphBody_PannelloRisultati");
            if (!pannelloRisultati) {
                return [];
            }
            var outerTable = pannelloRisultati.querySelector("table");
            var outerTbody = outerTable.children[0];
            var bulletins = [];
            for (var i in outerTbody.children) {
                (function () {
                    var child = outerTbody.children[i];
                    if (child.tagName !== "TR") {
                        return;
                    }
                    var td = child.children[0],
                        bulletin = scrapeBulletin(td, source, publisher);
                    bulletins.push(bulletin);
                })();
            }
            return bulletins;
        }, scrapeBulletin, SOURCE, PUBLISHER);
    }
];

/**
 * Show the script usage.
 */
function showHelp() {
    console.error("Usage: " + args[0] + " <1|2|3>");
    console.error("The argument is the bullettin series (general, news and contests, communications)\n");
}

// Main program

var serie = args[1]; // If args length is 1 this is undefined
if (["1", "2", "3"].indexOf(serie) === -1) {
    showHelp();
    phantom.exit(1);
}

setInterval(function () {
    if (!loadInProgress && typeof steps[stepIndex] === "function") {
        var bulletins = steps[stepIndex]();
        if (stepIndex === 2) {
            console.log(JSON.stringify(bulletins));
        }
        stepIndex++;
    }
    // Out of bounds items are undefined
    if (typeof steps[stepIndex] !== "function") {
        phantom.exit();
    }
}, 50);
