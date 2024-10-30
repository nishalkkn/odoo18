/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart, useRef } from  "@odoo/owl";
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
        this.allButtonShow = true;
        this.showLess = false;
        this.moreButtonShow = true;
        this.chunkValue = 0;
        this._fetch_data();

        this.attendanceCount = useRef("attendance_count")
        this.leaveCount = useRef("leave_count")
        this.projectCount = useRef("project_count")
        this.employeeName = useRef("employee_name")
        this.employeeJobTitle = useRef("employee_job_title")
        this.yearOfExperience = useRef("year_of_experience")
        this.organizationChart = useRef("organization_chart")

        this.state = useState({
            value: {},
        });

        onWillStart(async () => {
            this.isEmployeeManager = await user.hasGroup("hr.group_hr_manager");
        });
    }

    //    function for fetching data from model
    //    async _fetch_data() {
    //        var employees = null;
    //        const result =  await this.orm.call("hr.employee", "get_tiles_data", [], {})
    //
    //        employees = result.employees;
    //
    //        this.current_employee_id = result.current_employee_id;
    //        this.current_employee_name = result.current_employee_name;
    //        this.attendanceCount.el.innerText = result.attendance_count;
    //        this.employeeName.el.innerText = user.name;
    //        this.leaveCount.el.innerText = result.leave_count;
    //        this.projectCount.el.innerText = result.project_count;
    //        this.employeeJobTitle.el.innerText = result.employee_job_title;
    //        this.yearOfExperience.el.innerText = `Experience : ${result.years_of_experience} Years`;
    //
    //        this._fetch_org_chart(self.current_employee_id);
    //
    //        this.allEmployees = employees,
    //        this.chunkData = chunk(employees, 8),
    //        this.chunkData[0].is_active = true,
    //        this.state.value = this.chunkData[0];
    //        this.state.value = employees;
    //    }

    _fetch_data() {
        var self = this;
        var employees = null;
        this.orm.call("hr.employee", "get_tiles_data", [], {}).then(function(result) {
            employees = result.employees;

            self.current_employee_id = result.current_employee_id;
            self.current_employee_name = result.current_employee_name;
            self.attendanceCount.el.innerText = result.attendance_count;
            self.employeeName.el.innerText = user.name;
            self.leaveCount.el.innerText = result.leave_count;
            self.projectCount.el.innerText = result.project_count;
            self.employeeJobTitle.el.innerText = result.employee_job_title;
            self.yearOfExperience.el.innerText = `Experience : ${result.years_of_experience} Years`;

            self.allEmployees = employees,
            self.chunkData = chunk(employees, 8),
            self.chunkData[0].is_active = true,
            self.state.value = self.chunkData[0];
            self._fetch_org_chart(self.current_employee_id);
        });
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
            for (const child in children) {
                const child_name = children[child].name;
                org_chart_html += `<div style='margin-left: 40px; color: #bf80ff;' class='o_treeEntry py-2'>${child_name}</div>`;
            }
        }
        this.organizationChart.el.innerHTML = org_chart_html;
    }

    // button to show all employees
    showAllEmployeesClicked() {
        this.state.value = this.allEmployees;
        this.allButtonShow = false;
        this.showLess = true;
        this.moreButtonShow = false;
    };

    // button to show more employees
    showMoreEmployeesClicked() {
        this.chunkValue += 1;
        if (this.chunkValue < this.chunkData.length) {
            this.state.value = this.state.value.concat(this.chunkData[this.chunkValue]);
            this.showLess = true;
        } else {
            this.moreButtonShow = false;
            this.allButtonShow = false;
            this.showLess = true;
        }
    };

    // button to show less employees
    showLessEmployeesClicked() {
        this.chunkValue = 0;
        this.state.value = this.chunkData[0];
        this.allButtonShow = true;
        this.showLess = false;
        this.moreButtonShow = true;
    };

    attendanceTileClicked() {
        const employeeId = this.employ_tile || this.current_employee_id
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.attendance",
            name: this.employeeName.el.innerText,
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
        console.log(this.employeeName.el.innerText)
        this.env.services.action.doAction({
            type: "ir.actions.act_window",
            res_model: "hr.leave",
            name: this.employeeName.el.innerText,
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
            name: this.employeeName.el.innerText,
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
        this.attendanceCount.el.innerText = attendance;
        //        finding and replacing attendance count
        var leave = await this.orm.searchCount('hr.leave', [
            ["employee_id", "=", employ_id]
        ]);
        this.leaveCount.el.innerText = leave;
        //        finding and replacing attendance count
        var project = await this.orm.searchCount('project.project', [
            ["user_id", "=", user_id]
        ]);
        this.projectCount.el.innerText = project;
        //        replacing employee name, job title and experience
        this.employeeName.el.innerText = employ_name;
        this.employeeJobTitle.el.innerText = job_title;
        this.yearOfExperience.el.innerText = `Experience : ${employee_experience} Years`;

        // assigning values to handle view of details
        this.employ_tile = employ_id;
        this.employName_tile = employ_name;
        this.user_tile = user_id;
        this._fetch_org_chart();
    }
}

const actionRegistry = registry.category("actions");
EmployeeDashboard.template = "employee_dashboard.EmployeeDashboard";
actionRegistry.add("employee_dashboard_tag", EmployeeDashboard);
