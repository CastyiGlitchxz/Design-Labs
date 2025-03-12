'use client'

import { use } from "react";
import { socket } from "../../../../../socket";
import project_styling from "../../projects.module.css"

export default function Editor({ params }: { params: Promise<{ id: string }> }) {
    const { id } = use(params);
    
    return (
        <div>
            <iframe src={`http://localhost:8000/projects/${id}`} className={project_styling.project_viewer}></iframe>
        </div>
    )
}