/* eslint-disable @next/next/no-img-element */
'use client'

import { useEffect, useState } from "react";
import { socket } from "../../socket"
import { Is_logged_in, logout, login, Get_user } from "../../user";
import project_styles from "./projects/projects.module.css"
import app_stylesheet from "./index.module.css"
import { application } from "../../application";
import favicon from "./favicon.ico"

function Creation({close_func = new Function, create_func = new Function}) {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const formattedDate = `${year}-${month}-${day}`;

  const [projectInfo, setProjectInfo] = useState({
      project_name: "New Project",
      filename: "index.html",
      language: "JavaScript",
      scripting_file: "Yes",
      stylesheet_file: "Yes",
      creation_date: formattedDate,
  });

  const setInformation = (event) => {
      const {name, value} = event.target;
      setProjectInfo(prevState => ({
          ...prevState,
          [name]: value,
      }));
  };

  return (
    <div className={project_styles.project_creation_modal}>
        <div className={project_styles.modal_header}>
            <p>New Project</p>

            <button onClick={() => close_func()}>X</button>
        </div>

        <div className={project_styles.parent_container}>
            <div className={project_styles.modal_panel}>
                <span className={project_styles.info_badge}>
                    <p>Project Name: {projectInfo["project_name"]}</p>
                </span>

                <span className={project_styles.info_badge}>
                    <p>HTML File Name: {projectInfo["filename"]}</p>
                </span>

                <span className={project_styles.info_badge}>
                    <p>Language: {projectInfo["language"]}</p>
                </span>

                <span className={project_styles.info_badge}>
                    <p>Scripting File: {projectInfo["scripting_file"]}</p>
                </span>

                <span className={project_styles.info_badge}>
                    <p>Stylesheet File: {projectInfo["stylesheet_file"]}</p>
                </span>

                <span className={project_styles.info_badge}>
                    <p>Creation Date: {projectInfo["creation_date"]}</p>
                </span>
            </div>

            <div className={project_styles.modal_panel}>
                <input type="text" required={true} placeholder="Name your project" name="project_name" onChange={setInformation}/>
                <input type="text" required={true} placeholder="Name your html file" name="filename" onChange={setInformation}/>
                
                <span style={{display: "flex", gap: "12px"}}>
                    <input type="radio" id="ts" name="language" required value={"TypeScript"} onChange={setInformation}/>
                    <label htmlFor="ts">TypeScript</label>
                    <br/>
                    <input type="radio" id="js" name="language" required value={"JavaScript"} defaultChecked={true} onChange={setInformation}/>
                    <label htmlFor="js">JavaScript</label>
                </span>

                <span style={{display: "flex", gap: "12px"}}>
                    <input type="radio" id="scripting_yes" name="scripting_file" required value={"Yes"} onChange={setInformation} defaultChecked={true}/>
                    <label htmlFor="scripting_yes">Yes</label>
                    <br/>
                    <input type="radio" id="scripting_no" name="scripting_file" required value={"No"} onChange={setInformation}/>
                    <label htmlFor="scripting_no">No</label>
                </span>

                <span style={{display: "flex", gap: "12px"}}>
                    <input type="radio" id="stylesheet_yes" name="stylesheet_file" required value={"Yes"} onChange={setInformation} defaultChecked={true}/>
                    <label htmlFor="stylesheet_yes">Yes</label>
                    <br/>
                    <input type="radio" id="stylesheet_no" name="stylesheet_file" required value={"No"} onChange={setInformation}/>
                    <label htmlFor="stylesheet_no">No</label>
                </span>

            </div>
        </div>

        <div className={project_styles.modal_footer}>
            <button onClick={() => create_func(projectInfo["project_name"], projectInfo["filename"], projectInfo["stylesheet_file"], projectInfo["scripting_file"], projectInfo["language"])}>Create</button>
        </div>
    </div>
  )
}

function Profile_options() {
  return (
    <div className={app_stylesheet.profile_container}>
      <img src={favicon.src} height={120} width={120} className={app_stylesheet.user_profile} alt="a user's picture"/>
      <h1>{Get_user()}</h1>
      <button onClick={() => logout()} className={app_stylesheet.logout_button}>Logout</button>
    </div>
  )
}

function NotLoggedInPrompt() {
  return (
    <div className={app_stylesheet.not_logged_in}>
      <h3>You should consider logging in</h3>
      <ul>
        <li>You can manage your data better.</li>
        <li>You can make tasks.</li>
        <li>You can better manage your workflow</li>
      </ul>

      <button onClick={() => login()} className={app_stylesheet.login_button}>Login</button>
    </div>
  )
}

function TaskManager() {
  const [taskData, setTaskData] = useState({
    task_name: "",
    task_desc: "",
    date: new Date(),
  });

  const setInformation = (event) => {
    const {name, value} = event.target;
    setTaskData(prevState => ({
        ...prevState,
        [name]: value,
    }));
};

  function add_task() {
    socket.emit("add_task", taskData);
  }

  return (
    <div className={app_stylesheet.task_creator_panel}>
      <input type="text" placeholder="Task name" name="task_name" onChange={setInformation} className={app_stylesheet.task_panel_input}/>
      <input type="text" placeholder="Task description" name="task_desc" onChange={setInformation} className={app_stylesheet.task_panel_input}/>
      <input type="date" name="date" onChange={setInformation} className={app_stylesheet.task_panel_input}/>
      <button onClick={() => add_task()} className={app_stylesheet.task_panel_input}>Create</button>
    </div>
  )
}

export default function Home() {
    const [projects, setProjects] = useState([])
    const [tasks_list, setTasks] = useState<{ tasks: { name: string, desc: string }[] }>({ tasks: [] })
    // const [showCreation, setShowCreation] = useState(false);
    // const [showTaskCreator, setShowTaskCreator] = useState(false);
    const [modalManager, setModalManager] = useState({
      showCreation: false,
      showTaskCreator: true,
    })

    socket.emit("connection");
    
    useEffect(() => {
      socket.emit("get_tasks");
      
      socket.on("received_tasks", (task_data) => {
        setTasks(task_data);
      })
    }, [tasks_list])
    
    useEffect(() => {
      socket.once("projects_list", (fetched_projects) => {
          setProjects(fetched_projects);
      })
    }, [projects])

    function delete_project(project_name: string) {
        const deletion_message = prompt(`Type your project's name to delete "${project_name}" `);

        if (deletion_message === project_name) {
            socket.emit("delete_project", project_name);
        }
    }

    function open_project(project_name: string) {
        window.location.href = `/projects/editor/${project_name}`;
    }

    const set_manager = (event) => {
      const {name} = event.target;
      setModalManager(prevState => ({
          ...prevState,
          [name]: event.target.getAttribute("data-modalrevealed") === "true",
      }));
  
    };

    function close_modal() {
      setModalManager({showCreation: false, showTaskCreator: false})
    }

    function create_project(project_name: string, filename: string, css: false, js: false, file_ext: "") {
        socket.emit("create_project", project_name, filename, css, js, file_ext);
        setModalManager({showCreation: true, showTaskCreator: false})
    }

    const cut_replace = (text: string, length: number) => {
      if (text == null) {
          return "";
      }
      if (text.length <= length) {
          return text;
      }
      text = text.substring(0, length);
      const last = text.lastIndexOf("");
      text = text.substring(0, last);
      return text + "...";
    }

  return (
    <main>
      <div className={app_stylesheet.app_dashboard}>
        <div className={app_stylesheet.dash_container}>
          <div className={app_stylesheet.app_logo} data-app_name={application.app_name} suppressHydrationWarning></div>
          {Is_logged_in() === true ? <Profile_options/> : <NotLoggedInPrompt/>}
        </div>

        <div className={app_stylesheet.dash_container}>
          <div className={app_stylesheet.dash_container_nav}> 
            <button onClick={set_manager} className={project_styles.create_button} name="showCreation" data-modalrevealed={true}>Add New Project</button>
          </div>

          <div>
            {modalManager.showCreation && <Creation close_func={close_modal} create_func={create_project}/>}
            {projects.map((project, index) => (
                <div key={index} className={project_styles.project}>
                    <p>{project}</p>
                    <div className={project_styles.project_options}>
                        <button onClick={() => open_project(project)}>Editor</button>
                        <button onClick={() => delete_project(project)}>Delete</button>
                    </div>
                </div>
            ))}
          </div>
        </div>

        <div className={app_stylesheet.dash_container}>
          <h1>Task Manager</h1>

          <div className={app_stylesheet.task_tools}>
            <button onClick={set_manager} name="showTaskCreator" data-modalrevealed={true} className={app_stylesheet.new_task_button}>New Task</button>
            { modalManager.showTaskCreator && <button onClick={set_manager} name="showTaskCreator" data-modalrevealed={false} className={app_stylesheet.new_task_button}>Cancel</button>}
          </div>

          {modalManager.showTaskCreator && <TaskManager/>}

          <div className={app_stylesheet.task_list}>
            {tasks_list.tasks.map((key, i) => (
              <button key={i} className={app_stylesheet.task_button}>
                <h3>{key["name"]}</h3>
                <p>{cut_replace(key["desc"], 42)}</p>
              </button>
            ))}
          </div>

        </div>
      </div>

      <span className={app_stylesheet.version_badge}>{application.app_version}</span>
    </main>
  );
}
