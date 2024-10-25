/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from  "@odoo/owl";
import { user } from "@web/core/user";

const actionRegistry = registry.category("actions");
class EmployeeDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this.current_employee_id = null;
        this._fetch_data();
    }

    _fetch_data() {
        var self = this;
        this.orm.call("hr.employee", "get_tiles_data", [], {}).then(function(result) {
            self.current_employee_id = result.current_employee_id;
            document.getElementById('attendance_count').append(result.attendance_count);
            document.getElementById('leave_count').append(result.leave_count);
            document.getElementById('project_count').append(result.project_count);
            document.getElementById('employee_name').append(user.name);
            document.getElementById('employee_job_title').append(result.employee_job_title);
            document.getElementById('year_of_experience').append('Experience : ', result.years_of_experience,' Years');

            self._fetch_org_chart(self.current_employee_id);
        });
    }

    _fetch_org_chart() {
        this.orm.call("hr.employee", "get_org_chart_data", [], {}).then(function(orgChart) {
            document.getElementById('organization_chart').innerHTML += orgChart;
        });
    }

    attendanceTileClicked() {
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.attendance",
            domain: [
                ['employee_id', '=', this.current_employee_id]
            ],
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: 'current',
        });
    }

    leaveTileClicked() {
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.leave",
            domain: [
                ['employee_id', '=', this.current_employee_id]
            ],
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: 'current',
        });
    }

    projectTileClicked() {
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "project.project",
            domain: [
                ['user_id', '=', user.userId]
            ],
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: 'current',
        });
    }

    personalInfoTileClicked() {
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.employee",
            res_id: this.current_employee_id,
            views: [
                [false, "form"]
            ],
            target: 'current',
        });
    }

    hierarchyTileClicked() {
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.employee",
            res_id: this.current_employee_id,
            domain: [
                ['user_id', '=', user.userId]
            ],
            views: [
                [false, "hierarchy"]
            ],
            context: {
                hierarchy_id: this.current_employee_id,
            },
            target: 'current',
        });
    }

}

EmployeeDashboard.template = "employee_dashboard.EmployeeDashboard";
actionRegistry.add("employee_dashboard_tag", EmployeeDashboard);
