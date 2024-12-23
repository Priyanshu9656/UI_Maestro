import {
  ArrowRight,
  FilePlus2,
  ImagePlus,
  Paperclip,
  SquareArrowOutUpRight,
} from "lucide-react";
import { SidebarTrigger } from "../components/ui/sidebar";
import { UploadedFile } from "../components/UploadedFile";
import { useForm, SubmitHandler } from "react-hook-form";
import axios from "axios";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "../components/ui/popover";
import { Resizable } from "re-resizable";
import { useRef, useState, useEffect } from "react";
import { TooltipProvider } from "@radix-ui/react-tooltip";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "../components/ui/tooltip";
import { InfoCard } from "../components/InfoCard";

interface FormInterface {
  query: string;
  figma_link: string;
  dir: string;
}

interface Props {
  currentProject: string;
}
interface messageInterface {
  sender: string;
  message: string;
}

export const ChatInterface = ({ currentProject }: Props) => {
  const attachmentRef = useRef<HTMLButtonElement>(null);
  const [preview,] = useState(false);
  const [uploadedFileNames, setUploadedFileNames] = useState<string[]>([]);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const { register, handleSubmit, reset } = useForm<FormInterface>();
  const [queryProcessing, setQueryProcessing] = useState(false);
  const [messages, setMessages] = useState<messageInterface[]>([
    { sender: "Bot", message: "HI" },
    { sender: "You", message: "HI" },
  ]);
  const [useCustomLib, setUseCustomLib] = useState(false);

  useEffect(() => {
    setMessages([]);
    setUploadedFileNames([]);
  }, [currentProject]);
  const onSubmit: SubmitHandler<FormInterface> = async (data) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: "You", message: data.query },
    ]);
    data.dir = currentProject;
    console.log(useCustomLib, currentProject);
    console.log("jkhakjdhkas");
    if (useCustomLib) {
      try {
        reset();
        setQueryProcessing(true);

        const response = await axios.post(
          `http://localhost:8000/process-prompt/${currentProject}`,
          {
            user_prompt: data.query,
            dir: currentProject,
          }
        );
        console.log("Query Success:", response.data);
        setQueryProcessing(false);
        response.data.message !== "" &&
          setMessages((prevMessages) => [
            ...prevMessages,
            { sender: "Bot", message: response.data.message },
          ]);

        // // console.log(data)
        // const response = await axios.post(
        //   `http://localhost:8000/process-prompt/${currentProject}`,
        //   {
        //     user_prompt: {
        //       prompt: data.query,
        //     },
        //     dir: currentProject,
        //     // user_prompt: { prompt: data.query },
        //     // dir: currentProject,
        //   }
        // );
      } catch (error) {
        console.error("Error calling process_prompt:", error);
      }
    } else {
      try {
        reset();
        setQueryProcessing(true);
        const response = await axios.post(`http://localhost:8000/query`, data);
        console.log("Query Success:", response.data);
        setQueryProcessing(false);
        response.data.message !== "" &&
          setMessages((prevMessages) => [
            ...prevMessages,
            { sender: "Bot", message: response.data.message },
          ]);
      } catch (error) {
        console.error("Query Error:", error);
      }
    }
  };

  const fetchDoc = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/get-docs/${currentProject}`
      );
      console.log(response);
      setUseCustomLib(true);
    } catch (err) {
      setUseCustomLib(false);
      console.log(err);
    }
  };

  useEffect(() => {
    currentProject !== "" && fetchDoc();
  }, [currentProject]);

  const deleteImage = async (imageName: string): Promise<void> => {
    try {
      const response = await axios.delete(
        `http://localhost:8000/delete-image/${currentProject}/${imageName}`
      );
      console.log("Image deleted successfully:", response.data);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error(
          "Error deleting image:",
          error.response ? error.response.data : error.message
        );
      } else {
        console.error("Unexpected error:", error);
      }
    }
  };
  const deleteDoc = async (docName: string): Promise<void> => {
    try {
      const response = await axios.delete(
        `http://localhost:8000/delete-doc/${currentProject}/${docName}`
      );
      console.log("Document deleted successfully:", response.data);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error(
          "Error deleting document:",
          error.response ? error.response.data : error.message
        );
      } else {
        console.error("Unexpected error:", error);
      }
    }
  };
  const removeFile = (filename: string) => {
    setUploadedFileNames((prev) => prev.filter((i) => i !== filename));
    const fileExtension = filename.split(".").pop()?.toLowerCase();
    if (
      fileExtension === "jpg" ||
      fileExtension === "jpeg" ||
      fileExtension === "png"
    ) {
      deleteImage(filename);
    } else if (
      fileExtension === "pdf" ||
      fileExtension === "docx" ||
      fileExtension === "doc" ||
      fileExtension === "txt"
    ) {
      deleteDoc(filename);
    }
  };

  const uploadImage = async (e: React.ChangeEvent<HTMLInputElement>) => {
    attachmentRef.current && attachmentRef.current.click();
    const files: FileList | null = e.target.files;
    files && setUploadedFileNames((prev) => [...prev, files[0].name]);
    if (files && files.length > 0) {
      const formData = new FormData();
      formData.append("file", files[0]);
      try {
        const response = await axios.post(
          `http://localhost:8000/upload-image/${currentProject}`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        setTimeout(() => {
          document
            .getElementsByClassName(files[0].name)[0]
            ?.classList.add("opacity-0");
        }, 1000);

        console.log("Image Upload Success:", response.data);
      } catch (error) {
        console.error("Image Upload Error:", error);
      }
    }
  };

  const uploadDocument = async (e: React.ChangeEvent<HTMLInputElement>) => {
    attachmentRef.current && attachmentRef.current.click();
    const files: FileList | null = e.target.files;
    files && setUploadedFileNames((prev) => [...prev, files[0].name]);
    if (files && files.length > 0) {
      const formData = new FormData();
      formData.append("file", files[0]);
      try {
        const response = await axios.post(
          `http://localhost:8000/upload-doc/${currentProject}`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        setTimeout(() => {
          document
            .getElementsByClassName(files[0].name)[0]
            ?.classList.add("opacity-0");
        }, 1000);
        setUseCustomLib(true);
        console.log("Document Upload Success:", response.data);
      } catch (error) {
        console.error("Document Upload Error:", error);
      }
    }
  };

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="w-full custom-scrollbar bg-main max-h-screen overflow-hidden grid grid-rows-[auto,10fr,1fr] grid-cols-1 gap-4 a  pb-4 pt-6  px-4 items-center justify-center justify-items-center">
      <div className="flex items-start h-auto  gap-3 mt-6  justify-self-start">
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger>
              <SidebarTrigger />
            </TooltipTrigger>
            <TooltipContent>
              <p>Toggle Sidebar</p>
            </TooltipContent>
          </Tooltip>

          <button
            disabled={currentProject === ""}
            onClick={() => window.open("http://localhost:3001/", "_blank")}
            className=" justify-center  items-center flex"
          >
            <Tooltip>
              <TooltipTrigger>
                <SquareArrowOutUpRight
                  className={`${
                    currentProject !== ""
                      ? "text-neutral-600"
                      : "text-neutral-400"
                  } w-4 h-4`}
                />
              </TooltipTrigger>
              <TooltipContent>
                <p>Preview in a new window</p>
              </TooltipContent>
            </Tooltip>
          </button>
          {/* <button
            disabled={currentProject === ""}
            onClick={() => setPreview((prev) => !prev)}
            className=" justify-center  items-center flex"
          >
            <Tooltip>
              <TooltipTrigger>
                <RadioTower
                  className={`${
                    preview ? "text-neutral-500" : "text-neutral-400"
                  } w-4 h-4`}
                />
              </TooltipTrigger>
              <TooltipContent>
                <p>Preview</p>
              </TooltipContent>
            </Tooltip>
          </button> */}
        </TooltipProvider>
      </div>
      {preview && (
        <section className="web view bg-white  absolute z-[10000] top-10 ">
          <Resizable
            defaultSize={{
              width: 720,
              height: 320,
            }}
            maxHeight={400}
            maxWidth={800}
          >
            <iframe
              className="w-full h-full border absolute z-[999999999] "
              src="http://localhost:3001/"
            ></iframe>
          </Resizable>
        </section>
      )}
      <section
        ref={chatContainerRef}
        className="chat gap-4 md:px-4 px-4 w-[80%] md:w-[70%] overflow-hidden group/messages  hover:overflow-y-auto transition-all  flex flex-col h-full"
      >
        {messages.length <= 0 && (
          <div className="welcome-message text-neutral-600 mt-12  flex flex-col gap-4">
            <h1 className="font-semibold text-4xl brand-blue-text">
              Welcome👋 <br />
            </h1>
            <p className="text-md text-neutral-600  font-semibold">
              Let's build something amazing together. What would you like to
              start with today?
            </p>
            {/* <p className="text-xs mt-4">
            {" "}
          </p> */}
            <section className="flex gap-4">
              <InfoCard
                heading="🚀 Get Started"
                description="Kick off your project or run an existing one to begin building amazing things!"
              />
              <InfoCard
                heading="📚 Custom Library"
                description="Provide your UI library documentation, and I'll create stunning websites for you!"
              />
              <InfoCard
                heading="🖼️ Image to Code"
                description="Transform your designs into functional code effortlessly!"
              />
            </section>
          </div>
        )}

        {/* <div
          className={`new-message-bot
          flex gap-1 relative items-center justify-start `}
        >
          <span
            className={`flex  brand-chat-gradient  text-white items-center gap-2  px-4 max-w-[70dvw] md:max-w-[40vw] rounded-3xl  py-2`}
          >
            <img
              src="/logo.svg"
              className={`
               w-6 h-6 -ml-2 rounded-full`}
              alt=""
            />
            Create a new project or run an existing one to start building!
          </span>
        </div> */}
        {messages &&
          messages.map((data: messageInterface) => (
            <div
              className={`${
                data.sender == "You" &&
                "justify-end group-hover/messages:mr-0  mr-[2.8px]  "
              } flex gap-1 relative items-center `}
            >
              <span
                className={`${
                  data.sender == "Bot"
                    ? "new-message-bot "
                    : "new-message-you  "
                } flex text-neutral-800 bg-neutral-50   items-start gap-2  px-4 max-w-[70dvw] md:max-w-[40vw] rounded-3xl  py-2`}
              >
                <img
                  src="/logo.svg"
                  className={`${
                    data.sender == "You" && "hidden"
                  } w-6 h-6 -ml-2 rounded-full`}
                  alt=""
                />
                {data.message}
              </span>
            </div>
          ))}
        {queryProcessing && (
          <div
            className={`
          flex gap-1 relative items-center justify-start `}
          >
            <span
              className={`flex  text-neutral-800 bg-neutral-50 items-center gap-2  px-4 max-w-[70dvw] md:max-w-[40vw] rounded-3xl  py-2`}
            >
              <img
                src="/logo.svg"
                className={`
               w-6 h-6 -ml-2 query-processing rounded-full`}
                alt=""
              />
              Hang tight! UI Maestro is processing your request.
            </span>
          </div>
        )}
      </section>

      <section className="w-[80%] md:w-[70%] flex items-center  px-4">
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="flex flex-col gap-1 justify-center w-full  shadow-sm border  rounded-3xl p-2 mr-[3px] bg-brand-secondary "
        >
          {" "}
          {uploadedFileNames.length > 0 && (
            <section className="flex px-4 flex-wrap gap-2">
              {uploadedFileNames.map((name: string) => (
                <UploadedFile filename={name} removeFile={removeFile} />
              ))}
            </section>
          )}
          <section className="flex gap-4 justify-center">
            <input
              disabled={currentProject === ""}
              {...register("query", { required: true })}
              type="text"
              placeholder="Type your message..."
              className="flex items-center  rounded-3xl  bg-brand-secondary  px-4 w-full   placeholder:text-neutral-400 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 text-sm  "
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  handleSubmit(onSubmit)();
                }
              }}
            />
            <Popover>
              <PopoverTrigger ref={attachmentRef} asChild>
                <button
                  disabled={currentProject === ""}
                  className="text-neutral-600"
                >
                  <Paperclip />
                </button>
              </PopoverTrigger>
              <PopoverContent
                sideOffset={16}
                className="w-80 rounded-lg bg-brand-secondary text-neutral-600 shadow flex flex-col"
              >
                <div className="grid grid-row-2 gap-3 text-xs items-center">
                  <input
                    type="file"
                    className="custom-image-upload hidden bg-brand-secondary  py-2   rounded-lg "
                    id="image"
                    onChange={uploadImage}
                    accept="image/*"
                  />
                  <label
                    className="flex items-center gap-1 cursor-pointer"
                    htmlFor="image"
                  >
                    <ImagePlus className="text-[#ffa35d] w-4 h-4" />
                    Add an image to chat
                  </label>
                  <input
                    id="document"
                    type="file"
                    className="custom-document-upload hidden py-2   rounded-lg "
                    onChange={uploadDocument}
                    accept=".pdf,.docx,.txt"
                  />
                  <label
                    htmlFor="document"
                    className="flex  items-center gap-1 cursor-pointer"
                  >
                    <FilePlus2 className="text-[#ffa35d] w-4  h-4" />
                    Add custom library
                  </label>
                  <p className="">
                    Supported image formats: .JPG, .JPEG , .PNG <br />
                    Supported formats for custom library: .DOCX, .PDF
                  </p>
                  {/*              
                  <input
                    className="flex items-center border-b border-neutral-200   bg-brand-secondary px- py-3   placeholder:text-neutral-400 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 text-sm  "
                    type="text"
                    placeholder="Paste your figma link here"
                  /> */}
                </div>
              </PopoverContent>
            </Popover>
            <button
              disabled={currentProject === ""}
              type="submit"
              className=" bg-brand  text-white flex justify-center items-center  aspect-square p-2   rounded-full"
            >
              <ArrowRight className="h-auto w-auto" />
            </button>
          </section>
        </form>
      </section>
    </div>
  );
};
