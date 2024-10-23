/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from  "@odoo/owl";
const actionRegistry = registry.category("actions");
class EmployeeDashboard extends Component {
    setup() {
        super.setup()
        this.orm = useService('orm')
        this._fetch_data()
    }
    _fetch_data() {
        var self = this;
        this.orm.call("hr.employee", "get_tiles_data", [], {}).then(function(result) {
            document.getElementById('attendance_count').append(result.attendance_count);
            // document.getElementById('total_attendance_count').append( result.total_attendance_count);
            document.getElementById('leave_count').append(result.leave_count);
            document.getElementById('project_count').append(result.project_count);
        });
    };
    attendanceTileClicked() {
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.attendance",
            views: [
                [false, "list"],
                [false, "form"]],
            target: 'current',
        });
    }
    leaveTileClicked() {
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.leave",
            views: [
                [false, "list"],
                [false, "form"]],
            target: 'current',
        });
    }
    projectTileClicked() {
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "project.project",
            views: [
                [false, "list"],
                [false, "form"]],
            target: 'current',
        });
    }
}
EmployeeDashboard.template = "employee_dashboard.EmployeeDashboard";
actionRegistry.add("employee_dashboard_tag", EmployeeDashboard);
