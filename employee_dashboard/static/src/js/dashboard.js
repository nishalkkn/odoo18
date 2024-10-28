/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from  "@odoo/owl";
import { user } from "@web/core/user";

const actionRegistry = registry.category("actions");
class EmployeeDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this.current_employee_id = null;
        this._fetch_data();

        this.state = useState({
            value: {},
        });
    }

    //    function for fetching data from model
    async _fetch_data() {
        var self = this;
        var employees = null;
        await this.orm.call("hr.employee", "get_tiles_data", [], {}).then(function(result) {
            employees = result.employees;

            self.current_employee_id = result.current_employee_id;
            document.getElementById('attendance_count').append(result.attendance_count);
            document.getElementById('leave_count').append(result.leave_count);
            document.getElementById('project_count').append(result.project_count);
            document.getElementById('employee_name').append(user.name);
            document.getElementById('employee_job_title').append(result.employee_job_title);
            document.getElementById('year_of_experience').append('Experience : ', result.years_of_experience, ' Years');

            self._fetch_org_chart(self.current_employee_id);
        });
        this.state.value = employees
    }

    //    function for fetch org chart data
    async _fetch_org_chart() {
        const current_employee = await this.orm.searchRead('hr.employee', [
            ['user_id', '=', user.userId]
        ], ['id', 'name']);
        if (current_employee.length > 0) {
            const current_employee_id = current_employee[0].id;
            const current_employee_name = current_employee[0].name;
            const parent = await this.orm.searchRead('hr.employee', [
                ['id', '=', current_employee_id]
            ], ['parent_id']);
            let parent_name = '';
            if (parent.length > 0) {
                parent_name = parent[0].parent_id[1];
            }
            const children = await this.orm.searchRead('hr.employee', [
                ['parent_id', '=', current_employee_id]
            ], ['id', 'name']);
            let org_chart_html = '';
            if (parent_name) {
                org_chart_html += `<div style='color: #bf80ff;'>${parent_name}</div>`;
            }
            org_chart_html += `<div style='margin-left: 20px;' class='o_treeEntry py-2'>${current_employee_name}</div>`;
            if (children.length > 0) {
                for (const child of children) {
                    const child_name = child.name;
                    org_chart_html += `<div style='margin-left: 40px; color: #bf80ff;' class='o_treeEntry py-2'>${child_name}</div>`;
                }
            }
            document.getElementById('organization_chart').innerHTML += org_chart_html;
        }
    }

//    attendanceTileClicked(employ_id = null) {
//        const employeeId = employ_id || this.current_employee_id;
//        this.env.services.action.doAction({
//            type: "ir.actions.act_window",
//            res_model: "hr.attendance",
//            domain: [
//                ['employee_id', '=', employeeId]
//            ],
//            views: [
//                [false, "list"],
//                [false, "form"]
//            ],
//            target: 'current',
//        });
//    }

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

    //    function for fetching data when click on employee tile
    async employeeTileClicked(e) {
        var mmm = e.target.lastChild.innerText
        var employ_id = parseInt(e.target.lastChild.innerText)
        var employ_name = e.target.innerText

        const employee_id_rec = await this.orm.searchRead('hr.employee', [
            ['id', '=', employ_id]
        ], ['user_id']);
        var user_id = parseInt(employee_id_rec[0].user_id[0]);
        const employee_job_rec = await this.orm.searchRead('hr.employee', [
            ['id', '=', employ_id]
        ], ['job_title']);
        var job_title = employee_job_rec[0].job_title;

        const employee_join_date_rec = await this.orm.searchRead('hr.employee', [
            ['id', '=', employ_id]
        ], ['create_date']);
        var join_date = parseInt(employee_join_date_rec[0].create_date.slice(0, 4))
        var employee_experience = new Date().getFullYear() - join_date

        //        finding and replacing attendance count
        var attendance = await this.orm.searchCount('hr.attendance', [
            ["employee_id", "=", employ_id]
        ]);
        document.getElementById('attendance_count').innerHTML = attendance;
        //        finding and replacing attendance count
        var leave = await this.orm.searchCount('hr.leave', [
            ["employee_id", "=", employ_id]
        ]);
        document.getElementById('leave_count').innerHTML = leave;
        //        finding and replacing attendance count
        var project = await this.orm.searchCount('project.project', [
            ["user_id", "=", user_id]
        ]);
        document.getElementById('project_count').innerHTML = project;
        //        replacing employee name, job title and experience
        document.getElementById('employee_name').innerHTML = employ_name;
        document.getElementById('employee_job_title').innerHTML = job_title;
        document.getElementById('year_of_experience').innerHTML = `Experience : ${employee_experience} Years`;

//        this.attendanceTileClicked(employ_id);

    }
}

EmployeeDashboard.template = "employee_dashboard.EmployeeDashboard";
actionRegistry.add("employee_dashboard_tag", EmployeeDashboard);
