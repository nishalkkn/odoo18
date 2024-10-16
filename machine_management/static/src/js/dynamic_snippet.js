/** @odoo-module */


import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToFragment } from "@web/core/utils/render";

function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}


PublicWidget.registry.DynamicSnippet = PublicWidget.Widget.extend({
    selector: '.best_seller_product_snippet',
    willStart: async function() {
        this.data = await jsonrpc('/top_selling_machine', {})
    },
    start: function() {
        const refEl = this.$el.find("#top_machines_carousel")
        const chunkData = chunk(this.data, 4)
        chunkData[0].is_active = true,
        refEl.html(renderToFragment('machine_management.machine_created_wise', {
            chunkData
        }))
    }
});
return PublicWidget.registry.DynamicSnippet
