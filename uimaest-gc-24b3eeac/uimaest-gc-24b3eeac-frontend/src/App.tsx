import { useState } from "react";
import "./App.css";
import { SidebarComponent } from "./components/SidebarComponent";
import { SidebarProvider } from "./components/ui/sidebar";
import { ChatInterface } from "./pages/ChatInterface";
import { Toaster } from "./components/ui/sonner";
function App() {
  const [currentProject, setCurrentProject] = useState("");
  return (
    <div className="flex">
      <Toaster />
      <SidebarProvider>
        <SidebarComponent
          setCurrentProject={setCurrentProject}
          currentProject={currentProject}
        />
        <ChatInterface currentProject={currentProject} />
      </SidebarProvider>
    </div>
  );
}

export default App;
