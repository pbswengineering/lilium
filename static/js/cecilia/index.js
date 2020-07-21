// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

/**
 * cecilia/index.js
 * ~~~~~~~~~~~~~~~~
 *
 * JavaScript code to support the Cecilia dashboard: sensor live readings
 * and last 24h graph.
 *
 * @copyright (c) 2018 Paolo Paolo Bernardi.
 * @license GNU AGPL version 3, see LICENSE for more details.
 */

var currentTimer;

/**
 * Get all sensor data via an Ajax call and update all widgets and charts on the page.
 * @param url_all_sensor_data endpoint of the Ajax call to get the data of all configured sensors
 */
function get_all_sensor_data(url_all_sensor_data) {
    $.getJSON(url_all_sensor_data, function (all_sensor_data) {
        $.each(all_sensor_data.sensors, function (index, sensor_data) {
            update_live_sensor(sensor_data);
            update_chart(sensor_data, true, "");
            var count_down = 60;
            var update_count_down = function () {
                if (currentTimer) {
                    clearTimeout(currentTimer);
                }
                $(".countdown").html("Next refresh in " + count_down + "s");
                --count_down;
                if (count_down > 0) {
                    currentTimer = setTimeout(update_count_down, 1000);
                }
            };
            update_count_down();
        })
    }).fail(function () {
        console.error("Connection error, couldn't get sensor data.");
    });
}

/**
 * Periodic refresh of sensor widgets and charts.
 * @param url_all_sensor_data endpoint of the Ajax call to get the data of all configured sensors
 */
function init_cecilia_index(url_all_sensor_data) {
    $(function () {
        get_all_sensor_data(url_all_sensor_data, true);
        setInterval(function () {
            get_all_sensor_data(url_all_sensor_data);
        }, 60000);
    })
}
