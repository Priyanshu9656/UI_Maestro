import { Plus } from "lucide-react";
import { Popover, PopoverContent, PopoverTrigger } from "./ui/popover";
import {
  Sidebar,
  SidebarHeader,
  SidebarContent,
  SidebarMenu,
  SidebarMenuItem,
} from "./ui/sidebar";
import { useForm, SubmitHandler } from "react-hook-form";
import axios from "axios";
import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "./ui/tooltip";
import ProjectComponent from "./ProjectComponent";

interface FormValues {
  project_name: string;
  project_desc: string;
}

export interface Project {
  name: string;
  description: string;
  dir: string;
}

interface Prop {
  setCurrentProject(newState: string): void;
  currentProject: string;
}

export const SidebarComponent = ({
  setCurrentProject,
  currentProject,
}: Prop) => {
  const { register, handleSubmit, reset } = useForm<FormValues>();
  const newProjectRef = useRef<HTMLButtonElement>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [projects, setProjects] = useState<Project[]>([]);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await axios.get("http://localhost:8000/projects");
        setProjects(response.data.filter((item: Project) => item.name != ""));
        console.log("Success:", response.data);
      } catch (error) {
        console.error("Error:", error);
      }
    };

    fetchProjects();
  }, [currentProject]);

  const runReactApp = async (dir: string) => {
    setCurrentProject(dir);
    try {
      const response = await axios.get(`http://localhost:8000/run?dir=${dir}`);
      console.log("Success:", response.data);
    } catch (error) {
      console.error("Error:", error);
    }
  };
  const onSubmit: SubmitHandler<FormValues> = async (data) => {
    setIsCreating(true);
    try {
      const response = await axios.post(
        "http://localhost:8000/new_project",
        data
      );
      setCurrentProject(data.project_name);
      runReactApp(data.project_name);

      console.log("Success:", response.data);

      setIsCreating(false);
      toast.success("New Project Created", {
        description: "You can now start building UI!",
      });

      reset();
      newProjectRef.current && newProjectRef.current.click();
    } catch (error: any) {
      toast.error("Project Creation Failed", {
        description: error.response.data.detail,
      });
      setIsCreating(false);
      console.error("Error:", error);
    }
  };

  return (
    <Sidebar className=" px-2 bg-transparent pb-4 pl-3 ">
      <SidebarContent className="overflow-hidden bg-neutral-50 text-neutral-800   hover:overflow-y-auto mt-4 p-3  group/sidebar group/messages rounded-xl">
        <SidebarHeader className=" flex items-center justify-between mb-2   rounded-[3px] pt-4  px-4">
          <div className="flex gap-2 items-center">
            <img src="/logo.svg" className="w-5 h-5" alt="UI Maestro" />
            <h1 className="  font-bold brand-blue-text ">UI Maestro</h1>
          </div>
          <Popover>
            <PopoverTrigger ref={newProjectRef} className="flex items-center ">
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger className=" rounded-full">
                    <Plus className="w-5 h-5 brand-blue-text " />
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>New Project</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </PopoverTrigger>
            <PopoverContent
              sideOffset={16}
              className="rounded-lg  shadow  w-80   bg-brand-secondary flex flex-col"
            >
              <form
                className="flex flex-col   gap-3 text-xs"
                onSubmit={handleSubmit(onSubmit)}
              >
                <input
                  className="flex bg-brand-secondary items-center bg-sidebar border-b   pt-3 pb-1   placeholder:text-neutral-400 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50  "
                  type="text"
                  {...register("project_name", { required: true })}
                  placeholder="Project Name"
                />
                <input
                  className="flex bg-brand-secondary items-center border-b  bg-sidebar  resize-none border-neutral-200    bg-white   pt-3 pb-1   placeholder:text-neutral-400 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50  "
                  {...register("project_desc")}
                  placeholder="Project Description"
                />
                <button
                  type="submit"
                  className="text-white bg-brand   self-end w-8 h-8  flex justify-center items-center rounded-3xl  text-xs"
                >
                  {isCreating ? <div className="loader"></div> : <Plus />}
                </button>
              </form>
            </PopoverContent>
          </Popover>
        </SidebarHeader>

        <SidebarMenu>
          <SidebarMenuItem className="">
            <div className="flex flex-col gap-2  rounded">
              {projects &&
                projects.map((project) => (
                  <ProjectComponent
                    runReactApp={runReactApp}
                    currentProject={currentProject}
                    setProjects={setProjects}
                    projects={projects}
                    setCurrentProject={setCurrentProject}
                    project={project}
                  />
                ))}
            </div>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarContent>
    </Sidebar>
  );
};
