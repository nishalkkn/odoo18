/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useState, Component, onWillStart } from  "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";

const actionRegistry = registry.category("actions");
class EmployeeDashboard extends Component {
    setup() {
         super.setup()
         this.orm = useService('orm')
         this.action = useService("action")
         this.state = useState({
            value: "",
            user_name: "",
            user_val: "",
            user_job: "",
            emp_value: "",
            emp_user_id: user.userId,
            emp_id: "",
        })
         onWillStart(async () => {
            this.isEmployeeManager = await user.hasGroup("hr.group_hr_manager");
         });
         this._fetch_data()
    }
    async _fetch_data(){
    // fetch data to the dashboard
        this.state.value = await this.orm.searchRead("hr.employee", [], [])
        var obj = await this.state.value
        var user_data = []
        var child_list = []
        for (let i=0; i < obj.length; i++){
            if (obj[i].user_id[0] == user.userId){
                user_data.push(obj[i])
                child_list.push(obj[i].child_ids)
            }
        }
        this.state.user_val = user_data[0]
        var employee_id = user_data[0].id
        this.state.emp_id = parseInt(employee_id)
        this.state.user_name = user_data[0].display_name
        this.state.user_job = user_data[0].job_id[1]
        document.getElementById('experience').innerText = 'Experience: ' + user_data[0].experience + ' years';
        var child_array = child_list[0]
        for (let i=0; i < child_array.length; i++){
            var child_data = await this.orm.searchRead("hr.employee", [["id", "=", child_array[i]]], [])
            document.getElementById('chart_list').innerHTML +=(`<li class="o_org_chart_entry o_org_chart_entry_sub o_treeEntry d-flex position-relative py-2 overflow-visible">` + child_data[0].display_name + `</li>`);
        }
        this.orm.call("hr.employee", "get_tiles_data", [], {}).then(function(result){
        document.getElementById('attendance').innerText = result.total_attendance;
        document.getElementById('leaves').innerText = result.total_leave;
        document.getElementById('project').innerText = result.total_project;
        });
   };
   attendanceTileClick(){
   // Click function on attendance tile to display the attendance records of the user/selected employee
       this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'hr.attendance',
            domain: [["employee_id", "=", this.state.emp_id]],
            views: [[false, 'list'], [false, 'form']],
            target: 'current',
       })
   }
   leaveTileClick(){
  // Click function on leave tile to display the time-off records of the user/selected employee
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'hr.leave',
            domain: [["employee_id", "=", this.state.emp_id]],
            views: [[false, 'list'], [false, 'form']],
            target: 'current',
        })
   }
   projectTileClick(){
  // Click function on project tile to display the project records of the user/selected employee
        this.action.doAction({
                type: 'ir.actions.act_window',
                res_model: 'project.project',
                domain: [["user_id", "=", this.state.emp_user_id]],
                views: [[false, 'list'], [false, 'form']],
                target: 'current',
            })
   }
   personalInfoTileClick(e){
  // Click function on personal information tile to display the form view of the user/selected employee
        var action_employee = this.action
        action_employee.doAction({
            type: 'ir.actions.act_window',
            res_model: 'hr.employee',
            res_id: this.state.emp_id,
            views: [[false, "form"]],
            target: 'current',
        })
   }
   async empClick(e){
  // Click function from the list of employees only visible to the 'hr.group_hr_manager' to
  // display the selected employee data
        var target = e.target
        var emp_id = target.children[0].innerText;
        var emp_user_id = target.children[1].innerText
        this.state.emp_id = parseInt(emp_id)
        this.state.emp_user_id = parseInt(emp_user_id);
        this.state.emp_value = await this.orm.searchRead("hr.employee", [["id", "=", emp_id]], [])

        // calculate attendance count
        var emp_attendance = await this.orm.searchRead("hr.attendance", [], [])
        var att_data = []
        for (let i=0; i<emp_attendance.length; i++){
            if (emp_attendance[i].employee_id[0] == emp_id){
                att_data.push(emp_attendance[i])
            }
        }
        document.getElementById('attendance').innerText = att_data.length;

        // calculate leave count
        var leave = await this.orm.searchRead("hr.leave", [], ["id","employee_id"])
        var leave_data = []
        for (let i=0; i<leave.length; i++){
            if (leave[i].employee_id[0] == emp_id){
                leave_data.push(leave[i])
            }
        }
        document.getElementById('leaves').innerText = leave_data.length;

        // calculate project count
        var project = await this.orm.searchRead("project.project", [], [])
        var project_data = []
        for (let i=0; i<project.length; i++){
            if (project[i].user_id[0] == emp_user_id){
                project_data.push(project[i])
            }
        }
        document.getElementById('project').innerText = project_data.length;

        // Displays personal information and employee hierarchy based on the employee selection
        this.state.user_name = this.state.emp_value[0].display_name
        this.state.user_job = this.state.emp_value[0].job_id[1]
        document.getElementById("experience").innerText = 'Experience: ' + this.state.emp_value[0].experience + ' years'
        var child_val = this.state.emp_value[0].child_ids
        this.state.user_val = this.state.emp_value[0]
        document.getElementById("chart_list").style.display = "none";
        document.getElementById("emp_chart_list").innerHTML = ""
        if (child_val.length >= 1){
            for (let i=0; i<child_val.length; i++){
                var emp_child = await this.orm.searchRead("hr.employee", [["id", "=", child_val[i]]], [])
                document.getElementById("emp_chart_list").innerHTML +=(`<li class="o_org_chart_entry o_org_chart_entry_sub o_treeEntry d-flex position-relative py-2 overflow-visible">` + emp_child[0].display_name + `</li>`);
            }
        }
   }
}
EmployeeDashboard.template = "employee_dashboard.EmployeeDashboard";
actionRegistry.add("employee_dashboard_tag", EmployeeDashboard);