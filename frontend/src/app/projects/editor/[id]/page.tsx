/* eslint-disable jsx-a11y/alt-text */
/* eslint-disable @next/next/no-img-element */
'use client'

import { use, useEffect, useState, useCallback } from "react";
import { socket } from "../../../../../socket";
import favicon from "../../../favicon.ico"
import project_styling from "../../projects.module.css"
import DOMPurify from 'dompurify';

// function HTMLEditor() {
//     const [text, setText] = useState("");

//     const get_text = (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
//         setText(event.target.value);
//     }
// };

export default function Editor({ params }: { params: Promise<{ id: string }> }) {
    const { id } = use(params);
    const [html, setHTML] = useState({
        __html: "",
        alteredHTML: "",
    });
    const [editorText, setEditorText] = useState("");

    socket.on("return_project_data", (data) => {
        const sanitized_data = DOMPurify.sanitize(data);
        setHTML({__html: sanitized_data, alteredHTML: html.alteredHTML});
        setEditorText(sanitized_data);
    });


    const [selectedElement, setSelectedElement] = useState<{
        type: string;
        id: string;
        classes: string[];
    }>({
        type: "",
        id: "",
        classes: [],
    });

    const [viewManager, changeView] = useState({
        showViewport: true,
        showHTMLEditor: false,
    });

    interface ViewManagerEvent extends React.MouseEvent<HTMLButtonElement> {
        target: HTMLButtonElement & {
            getAttribute(name: string): string | null;
        };
    }

    const setViewManager = (event: ViewManagerEvent): void => {
        const { name } = event.target;
        changeView(prevState => ({
            ...prevState,
            [name]: event.target.getAttribute("data-set_view") === "true",
        }));
    };

    useEffect(() => {
        socket.emit("get_project_data", id);
    }, [id]);

    useEffect(() => {
        const project_render = document.getElementsByClassName(project_styling.render)[0];

        if (project_render) {
            const main = project_render.getElementsByTagName("main")[0];
    
            if (main) {
                main.addEventListener("click", (element) => {
                    const target = element.target as HTMLElement | null;
                    const pre_list: string[] = [];
    
                    target?.classList.forEach((entry) => {
                        pre_list.push(entry);
                    });
    
                    setSelectedElement((prev) => ({
                        ...prev,
                        classes: pre_list,
                        id: `#${target?.id}`
                    }));
                })
            }
        }

    })

    const get_editor_text = (event: React.ChangeEvent<HTMLTextAreaElement>): void => {
        setEditorText(event.target.value);
    }

    useEffect(() => {
        const sanitizedContent = DOMPurify.sanitize(editorText)
        setHTML({__html: sanitizedContent, alteredHTML: sanitizedContent})
    }, [editorText])

    useEffect(() => {

        const editor = document.getElementById(project_styling.code_editor);
        if (editor) {
            editor.onkeydown = function(e) {
                if (e.key == "Tab") {
                    const textarea = this as HTMLTextAreaElement;
                    textarea.setRangeText('\t', textarea.selectionStart, textarea.selectionStart, 'end');
                    return false;
                }
            }
        }
    })
    

    const project_write = useCallback((html: string) => {
        socket.emit("project_write", id, html);
    }, [id]);

    return (
        <div className={project_styling.editor}>
            <div className={project_styling.editor_nav}>
                <p>{id}</p>
                <img src={favicon.src} width="33" height="33"/>
                <button onClick={() => project_write(html.alteredHTML)}>Save</button>
            </div>

            <div className={project_styling.editor_panels}>
                <div className={project_styling.mode_switch_panel}>
                    <button data-set_view={true} name="showViewport" onClick={setViewManager}>V</button>
                    <button data-set_view={true} name="showHTMLEditor" onClick={setViewManager}>H</button>
                </div>

                <div className={project_styling.editor_panel}>
                    <div className={project_styling.panel_header}>
                        <p>Elements</p>
                    </div>
                </div>

                <div className={project_styling.project_viewer}>
                    <div className={project_styling.panel_header}>
                        <p>Device Viewport</p>
                    </div>

                    {viewManager.showViewport && 
                        <div className={project_styling.render} dangerouslySetInnerHTML={html}></div>
                    }


                    {viewManager.showHTMLEditor && 
                        <textarea id={project_styling.code_editor} value={editorText} onChange={get_editor_text} spellCheck={false}></textarea>
                    }
                </div>

                <div className={project_styling.editor_panel}>
                    <div className={project_styling.panel_header}>
                        <p>{selectedElement.id}</p>
                    </div>
                    
                    {selectedElement.classes.map((classes, index) => (
                        <button key={index}>{classes}</button>
                    ))}
                </div>
            </div>
        </div>
    );
}