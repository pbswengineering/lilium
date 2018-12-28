// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

/**
 * dahlia/index.js
 * ~~~~~~~~~~~~~~~
 *
 * JavaScript code to support the Dahlia dashboard.
 *
 * @copyright (c) 2018 Paolo Paolo Bernardi.
 * @license GNU AGPL version 3, see LICENSE for more details.
 */

/**
 * Get the category tree data in JSTree id/parent format.
 * @param url_category_tree endpoint of the Ajax call to get category tree in JSON format
 */
function get_category_tree(url_category_tree) {
    $.getJSON(url_category_tree, function (category_tree) {
        console.log(category_tree["categories"]);
        $('#category-tree').jstree({
            core: {
                data: category_tree["categories"]
            }
        });
    }).fail(function () {
        console.error("Connection error, couldn't get category tree data.");
    });
}

/**
 * Dashboard initialisation.
 * @param url_category_tree endpoint of the Ajax call to get category tree in JSON format
 */
function init_dahlia_index(url_category_tree) {
    $(function () {
        get_category_tree(url_category_tree);
    });
}
