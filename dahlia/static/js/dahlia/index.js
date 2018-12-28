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
 * Dashboard initialisation.
 */
function init_dahlia_index() {
    $(function () {
        $('#category-tree').jstree();
    });
}
