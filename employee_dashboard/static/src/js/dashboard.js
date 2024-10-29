/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from  "@odoo/owl";
import { user } from "@web/core/user";

function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

class EmployeeDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService('orm');
        this.current_employee_id = null;
        this.current_employee_name = null;
        this.employ_tile = null;
        this.employName_tile = null;
        this.user_tile = null;
        this.chunkData = null
        this.allEmployees = null;
        this.buttonShow = true;
        this.showLess = false;
        this._fetch_data();
        this.a = 0;

        this.state = useState({
            value: {},
        });

        this.isEmployeeManager = user.hasGroup("hr.group_hr_manager");


        onWillStart(async () => {
            this.isEmployeeManager = await user.hasGroup("hr.group_hr_manager");
        });
    }

    //    function for fetching data from model
    async _fetch_data() {
        var self = this;
        var employees = null;
        await this.orm.call("hr.employee", "get_tiles_data", [], {}).then(function(result) {
            employees = result.employees;

            self.current_employee_id = result.current_employee_id;
            self.current_employee_name = result.current_employee_name;
            document.getElementById('attendance_count').append(result.attendance_count);
            document.getElementById('leave_count').append(result.leave_count);
            document.getElementById('project_count').append(result.project_count);
            document.getElementById('employee_name').append(user.name);
            document.getElementById('employee_job_title').append(result.employee_job_title);
            document.getElementById('year_of_experience').append('Experience : ', result.years_of_experience, ' Years');

            self._fetch_org_chart(self.current_employee_id);
        });

        this.allEmployees = employees,
        this.chunkData = chunk(employees, 8),
        this.chunkData[0].is_active = true,
        this.state.value = this.chunkData[0];
    }

    //    function for fetch org chart data
    async _fetch_org_chart() {
        const employeeId = this.employ_tile || this.current_employee_id
        const employeeName = this.employName_tile || this.current_employee_name
        const parent = await this.orm.searchRead('hr.employee', [
            ['id', '=', employeeId]
        ], ['parent_id']);
        let parent_name = '';
        if (parent.length > 0) {
            parent_name = parent[0].parent_id[1];
        }
        const children = await this.orm.searchRead('hr.employee', [
            ['parent_id', '=', employeeId]
        ], ['id', 'name']);
        let org_chart_html = '';
        if (parent_name) {
            org_chart_html += `<div style='color: #bf80ff;'>${parent_name}</div>`;
        }
        org_chart_html += `<div style='margin-left: 20px;' class='o_treeEntry py'>${employeeName}</div>`;
        if (children.length > 0) {
            for (const child of children) {
                const child_name = child.name;
                org_chart_html += `<div style='margin-left: 40px; color: #bf80ff;' class='o_treeEntry py-2'>${child_name}</div>`;
            }
        }
        document.getElementById('organization_chart').innerHTML = org_chart_html;
    }

    // button to show all employees
    showAllEmployeesClicked() {
        this.state.value = this.allEmployees;
        this.buttonShow = false;
        this.showLess = true;
    };

    // button to show more employees
//    showMoreEmployeesClicked() {
//    this.a +=1,
//    };

    // button to show less employees
    showLessEmployeesClicked() {
        this.state.value = this.chunkData[0];
        this.buttonShow = true;
        this.showLess = false;
    };

    attendanceTileClicked() {
        const employeeId = this.employ_tile || this.current_employee_id
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.attendance",
            domain: [
                ['employee_id', '=', employeeId]
            ],
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: 'current',
        });
    }

    leaveTileClicked() {
        const employeeId = this.employ_tile || this.current_employee_id
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.leave",
            domain: [
                ['employee_id', '=', employeeId]
            ],
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: 'current',
        });
    }

    projectTileClicked() {
        const userId = this.user_tile || user.userId
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "project.project",
            domain: [
                ['user_id', '=', userId]
            ],
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: 'current',
        });
    }

    personalInfoTileClicked() {
        const employeeId = this.employ_tile || this.current_employee_id
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.employee",
            res_id: employeeId,
            views: [
                [false, "form"]
            ],
            target: 'current',
        });
    }

    //    function for fetching data when click on employee tile
    async employeeTileClicked(e) {
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

        this.employ_tile = employ_id;
        this.employName_tile = employ_name;
        this.user_tile = user_id;
        this._fetch_org_chart();
    }
}

const actionRegistry = registry.category("actions");
EmployeeDashboard.template = "employee_dashboard.EmployeeDashboard";
actionRegistry.add("employee_dashboard_tag", EmployeeDashboard);
