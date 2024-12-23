import axios from "axios";
import { Project } from "./SidebarComponent";
import {
  ArrowDownToLine,
  CircleStop,
  EllipsisVertical,
  Play,
} from "lucide-react";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "./ui/tooltip";
import { toast } from "sonner";
import { useRef, useState } from "react";

interface Prop {
  currentProject: string;
  project: Project;
  runReactApp(dir: string): void;
  setProjects(projects: Project[]): void;
  projects: Project[];
  setCurrentProject(newState: string): void;
}

const ProjectComponent = ({
  currentProject,
  project,
  runReactApp,
  setCurrentProject,
}: Prop) => {
  const [isPopoverOpen, setIsPopoverOpen] = useState(false);
  const moreRef = useRef<HTMLButtonElement>(null);
  //const [isDeleting, setIsDeleting] = useState(false);

  const stopProject = async () => {
    try {
      const response = await axios.get("http://localhost:8000/stop-project");
      if (response.data.status === "success") {
        setCurrentProject("");
      } else {
      }
    } catch (error) {
      console.error("There was a problem stopping the project:", error);
    }
  };

  const downloadProject = async (projectName: string) => {
    moreRef.current && moreRef.current.click();
    toast.info("Download", {
      description: "Your download will begin shortly.",
    });
    try {
      const response = await axios.get(
        `http://localhost:8000/download-project/${projectName}`,
        {
          responseType: "blob",
        }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = `${projectName}.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("There was a problem with the download operation:", error);
    }
  };

  // const deleteProject = async (projectName: string): Promise<void> => {
  //   setIsDeleting(true);
  //   try {
  //     const response = await axios.delete(
  //       `http://localhost:8000/delete-project/${projectName}`
  //     );
  //     console.log("Project deleted successfully:", response.data);
  //     setTimeout(() => {
  //       moreRef.current && moreRef.current.click();
  //     }, 300);

  //     setIsDeleting(false);
  //     const currentProjects: Project[] = projects;
  //     const filteredProjects = currentProjects.filter(
  //       (p: Project) => p.name !== projectName
  //     );
  //     setProjects(filteredProjects);
  //   } catch (error) {
  //     if (axios.isAxiosError(error)) {
  //       console.error(
  //         "Error deleting project:",
  //         error.response ? error.response.data : error.message
  //       );
  //     } else {
  //       console.error("Unexpected error:", error);
  //     }
  //   }
  // };

  return (
    <div
      key={project.name}
      className={`relative group/item  mx-2    py-2 px-3 flex hover:bg-[#EEF4FE] rounded-md items-center justify-between ${
        isPopoverOpen && "bg-[#EEF4FE]"
      }`}
    >
      <h1 className=" text-neutral-800 text-xs"> {project.name} </h1>
      {currentProject == project.name && !isPopoverOpen && (
        <span className=" absolute right-[.6rem]    group-hover/item:hidden  p-1 items-center justify-center w-4 h-4  text-xs">
          <div className="bg-brand animate-pulse  rounded-full w-2 h-2"></div>
        </span>
      )}
      <Popover onOpenChange={(open) => setIsPopoverOpen(open)}>
        <PopoverTrigger ref={moreRef} className={` items-center   `}>
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger className="p-0">
                <EllipsisVertical
                  className={` opacity-0 group-hover/item:opacity-[100]  ${
                    isPopoverOpen && "opacity-[100]"
                  } w-4 h-4 
                    brand-blue-text `}
                />
              </TooltipTrigger>
              <TooltipContent>
                <p>More</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </PopoverTrigger>
        <PopoverContent
          sideOffset={16}
          className="rounded text-neutral-600  w-min gap-1 px-3 py-3 shadow items-start  text-xs   bg-brand-secondary flex flex-col"
        >
          <button
            className="hover:bg-neutral-50 p-1 rounded text-left  flex items-center gap-2  w-full"
            onClick={() => {
              {
                currentProject === project.name
                  ? stopProject()
                  : runReactApp(project.name);
              }
              moreRef.current && moreRef.current.click();
            }}
          >
            {currentProject == project.name ? (
              <CircleStop className="text-[#ff6d00] w-4 h-4" />
            ) : (
              <Play className="text-[#ff6d00]  w-4 h-4" />
            )}
            {currentProject == project.name ? "Stop" : "Run"}
          </button>
          {/* <button
            onClick={() => deleteProject(project.name)}
            className="text-red-400 p-1 rounded text-left  hover:bg-neutral-100  w-full"
          >
            {isDeleting ? "Deleting..." : "Delete"}
          </button> */}
          <button
            onClick={() => downloadProject(project.name)}
            className="hover:bg-neutral-50 text-left flex items- gap-2 rounded p-1 pr-2  group-hover/messages:pr-0 w-full"
          >
            <ArrowDownToLine className="text-[#ff6d00] w-4 h-4" /> Download
          </button>
        </PopoverContent>
      </Popover>
    </div>
  );
};
export default ProjectComponent;
