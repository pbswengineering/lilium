// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

/**
 * cecilia/sensor_details.js
 * ~~~~~~~~~~~~~~~~~~~~~~~~~
 *
 * JavaScript code to support the Cecilia sensor details page:
 * live readings, sensor specifications and ~7 days graph.
 *
 * @copyright (c) 2018 Paolo Paolo Bernardi.
 * @license GNU AGPL version 3, see LICENSE for more details.
 */

/**
 * Update the specified sensor's widget and the chart.
 * Please note that the sensor is specified directly in the Ajax call URL.
 * @param url_sensor_data endpoint of the Ajax call to get the data of the desired sensor
 * @param must_update_chart whether or not the chart should be updated
 */
function get_sensor_data(url_sensor_data, must_update_chart) {
    var url = url_sensor_data + '?max_results=10080';  // 7 days data
    $.getJSON(url, function (sensor_data) {
        update_live_sensor(sensor_data);
        if (must_update_chart) {
            update_chart(sensor_data, true, "(no automatic refresh)");
        }
    }).fail(function () {
        console.error("Connection error, couldn't get sensor data.");
    });
}

/**
 * Periodic update of the specified sensor's widget and one-shot update for the sensor's chart.
 * RATIONALE: in this detail page the user should be able to analyse and drill the chart as he pleases, without
 * having the refresh resetting the chart's state.
 * Please note that the sensor is specified directly in the Ajax call URL.
 * @param url_sensor_data endpoint of the Ajax call to get the data of the desired sensor
 */
function init_cecilia_sensor(url_sensor_data) {
    $(function () {
        get_sensor_data(url_sensor_data, true);
         setInterval(function () {
             get_sensor_data(url_sensor_data, false);
        }, 60000);
    })
}
