// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

/**
 * cecilia/shared.js
 * ~~~~~~~~~~~~~~~~~
 *
 * JavaScript code to support the Cecilia pages: live sensor and chart updates.
 *
 * @copyright (c) 2018 Paolo Paolo Bernardi.
 * @license GNU AGPL version 3, see LICENSE for more details.
 */

/**
 * Update a live sensor widget.
 * @param {object} sensor_data sensor data, as returned by the sensor_data Ajax call
 */
function update_live_sensor(sensor_data) {
    var $card = $("#live-widget-" + sensor_data.name);
    var $icon_warning = $card.find(".icon-warning");
    var $icon_ok = $card.find(".icon-ok");
    var $temperature = $card.find(".temperature");
    var $humidity = $card.find(".humidity");
    var $warning = $card.find(".badge-warning");
    var $last_update = $card.find(".last-update");
    var last_reading = {
        tstamp: "...",
        temperature: "...",
        humidity: "..."
    };
    // sensor_data.readings is sorted in descending order, as per
    // server-side specifications
    if (sensor_data.readings && sensor_data.readings.length > 0) {
        last_reading = sensor_data.readings[0];
    }
    $icon_warning.show();
    $warning.show();
    if (!sensor_data.reachable) {
        $icon_ok.hide();
        $icon_warning.show();
        $warning.show();
    } else {
        $icon_ok.show();
        $icon_warning.hide();
        $warning.hide();
    }
    $last_update.text(last_reading.tstamp);
    $temperature.text(last_reading.temperature + '°');
    $humidity.text(last_reading.humidity + '%');
    $card.removeClass("card-red");
    $card.removeClass("card-yellow");
    $card.removeClass("card-green");
    $card.removeClass("card-blue");
    $card.addClass(sensor_data.css_class);
}

/**
 * Update a sensor temperature/humidity chart.
 * @param {object} sensor_data sensor data, as returned by the sensor_data Ajax call
 * @param {boolean} animation_enabled whether or not the graph will be animated
 * @param {string} extra_title extra title appended to the sensor name on the widget's header
 */
function update_chart(sensor_data, animation_enabled, extra_title) {
    var $extra_title = $("#chart-" + sensor_data.name).find(".extra-title");
    if ($extra_title) {
        $extra_title.html(extra_title);
    }
    var $chart_container = $("#chart-" + sensor_data.name).find(".chart-container");
    var temperature_data_points = sensor_data.readings.map(function (reading) {
        return {
            x: new Date(reading.tstamp),
            y: reading.temperature
        }
    });
    var humidity_data_points = sensor_data.readings.map(function (reading) {
        return {
            x: new Date(reading.tstamp),
            y: reading.humidity
        }
    });
    $chart_container.CanvasJSChart({
        animationEnabled: animation_enabled,
        zoomEnabled: true,
        axisX: {
            valueFormatString: "HH:mm",
            labelFontSize: 12,
            gridThickness: 1
        },
        axisY: {
            minimum: 0,
            maximum: 40,
            interval: 4,
            labelFontSize: 12,
            gridThickness: 1
        },
        axisY2: {
            minimum: 0,
            maximum: 100,
            interval: 20,
            labelFontSize: 12,
            gridThickness: 1
        },
        legend: {
            cursor: "pointer",
            fontSize: 10
        },
        toolTip: {
            shared: true
        },
        data: [{
            color: "#EDC240",
            lineThickness: 3,
            name: "Temperature",
            type: "line",
            yValueFormatString: "#0.##°",
            xValueFormatString: 'DDD YYYY-MM-DD"<br>"HH:mm',
            showInLegend: true,
            dataPoints: temperature_data_points
        }, {
            color: "#AFD8F8",
            lineThickness: 3,
            name: "Humidity",
            axisYType: "secondary",
            type: "line",
            yValueFormatString: '#0"%"',
            showInLegend: true,
            dataPoints: humidity_data_points
        }]
    });
}
