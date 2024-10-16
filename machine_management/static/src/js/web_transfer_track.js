/** @odoo-module */


import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.transferTableRow = publicWidget.Widget.extend({
    selector: '.machine_transfer_table_row',
    events: {
        'click .table_row_transfer': '_onClickTableRow',
    },

    _onClickTableRow: function(e){
        var id = $(e.currentTarget).children().children().html()
        window.location = `/webtransfer/${id}`
    },
});
