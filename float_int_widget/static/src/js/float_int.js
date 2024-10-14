/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { onRendered } from "@odoo/owl";
import {Component, useState} from "@odoo/owl";
import { useRef, useEffect, onWillRender, onMounted } from "@odoo/owl";
import { parseFloat } from "@web/views/fields/parsers";

export class FloatInt extends Component {
    static template = "float_int_widget.FloatIntField";
//    console.log('template : ',template),
    setup() {
        this.input = useRef('inputfloatint')
        useInputField({
            getValue: () => this.props.record.data[this.props.name] || "",
            refName: "inputfloatint",
            parse: (v) => parseFloat(v),
        });
        onWillRender(() => {
            this.rounded()
        });
        onMounted(() => {
            this.rounded()
        });
    }
    rounded() {
        if (this.input.el) {
            this.props.record.data[this.props.name] = Math.round(this.input.el.value)
        }
    }
}
FloatInt.component = FloatInt
FloatInt.supportedTypes = ["float"]
registry.category("fields").add("float_int_widget", FloatInt);
