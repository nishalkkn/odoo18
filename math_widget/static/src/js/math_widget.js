/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { useRef, onWillRender, onMounted, Component } from "@odoo/owl";

export class MathWidget extends Component {
    static template = "math_widget.MathWidget";
    setup() {
        this.input = useRef('mathinput'),
            useInputField({
                getValue: () => this.props.record.data[this.props.name] || "",
                refName: "mathinput",
            });
        onWillRender(() => {
            this.math()
        });
        onMounted(() => {
            this.math()
        });
    }
    math() {
        if (this.input.el) {
            try {
                this.props.record.data[this.props.name] = eval(this.input.el.value)
            } catch (err) {
                this.props.record.data[this.props.name] = false,
                    alert("Value in field cannot be calculated !!!");
            }
        }
    }
}
MathWidget.component = MathWidget
registry.category("fields").add("math_widget", MathWidget);
