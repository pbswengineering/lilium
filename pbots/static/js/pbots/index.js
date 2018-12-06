// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

/**
 * pbots/index.js
 * ~~~~~~~~~~~~~~
 *
 * JavaScript code to support the PBOTS dashboard: source table refreshing
 * and run/stop commands.
 *
 * @copyright (c) 2018 Paolo Paolo Bernardi.
 * @license GNU AGPL version 3, see LICENSE for more details.
 */

/**
 * GETs the specified URL and shows the resulting message on the modal.
 * The result must be a JSON with the message property.
 * @param {string} url URL of the desired Ajax call (run/stop)
 * @param {string} url_status URL of the Ajax call that returns the PBOTS status
 * @param {string} template_url_run URL of the Ajax call that starts a PBOTS with ID 0
 * @param {string} template_url_stop URL of the Ajax call that stops a PBOTS with ID 0
 */
function run_ajax(url, url_status, template_url_run, template_url_stop) {
    $.getJSON(url, function (res) {
        var $modal = $("#ajaxModal");
        $modal.find(".modal-body").html(res.message);
        $modal.modal("show");
        refresh_table(url_status, template_url_run, template_url_stop);
    }).fail(function () {
        console.error("Connection error, couldn't interact with PBOTS.");
    });
}

/**
 * Request the PBOTS status and show it on the table.
 * @param {string} url_status URL of the Ajax call that returns the PBOTS status
 * @param {string} template_url_run URL of the Ajax call that starts a PBOTS with ID 0
 * @param {string} template_url_stop URL of the Ajax call that stops a PBOTS with ID 0
 */
function refresh_table(url_status, template_url_run, template_url_stop) {
    $.getJSON(url_status, function (status) {
        var $tbody = $("#status-table").find("tbody");
        $tbody.empty();
        $.each(status.sources, function (index, source) {
            var url_run = template_url_run.replace("0", source["id"]);
            var js_run = "run_ajax('" + url_run + "', '" + url_status + "', '" + template_url_run + "', '" + template_url_stop + "')";
            var url_stop = template_url_stop.replace("0", source["id"]);
            var js_stop = "run_ajax('" + url_stop + "', '" + url_status + "', '" + template_url_run + "', '" + template_url_stop + "')";
            var $tr = $('<tr class="' + source['css_class'] + '">' +
                '<td>' + source['name'] + '</td>' +
                '<td>' + (source['running'] ? 'Yes' : 'No') + '</td>' +
                '<td>' + (source['started_at'] || '-') + '</td>' +
                '<td>' + (source['finished_at'] || '-') + '</td>' +
                '<td>' + source['executions'] + ' (last: ' + source['last_execution_ok'] + ')</td>' +
                '<td>' +
                '<div class="btn-group" role="group" aria-label="PBOTS commands">' +
                '<button type="button" class="btn btn-primary" onclick="' + js_run + '">Run</button>' +
                '<button type="button" class="btn btn-secondary" onclick="' + js_stop + '">Stop</button>' +
                '</div>' +
                '</td>' +
                '</tr>');
            $tbody.append($tr);
        });
    }).fail(function () {
        console.error("Connection error, couldn't get PBOTS data.");
    });
}

/**
 * Initialize the PBOTS index page JavaScript code.
 * This function must be called after including this file.
 * @param {string} url_status URL of the Ajax call that returns the PBOTS status
 * @param {string} template_url_run URL of the Ajax to start a PBOTS with ID 0
 * @param {string} template_url_stop URL to stop a PBOTS with ID 0
 */
function init_pbots_index(url_status, template_url_run, template_url_stop) {
    $(function () {
        refresh_table(url_status, template_url_run, template_url_stop);
        setInterval(function () {
            refresh_table(url_status, template_url_run, template_url_stop);
        }, 2000);
    });
}
