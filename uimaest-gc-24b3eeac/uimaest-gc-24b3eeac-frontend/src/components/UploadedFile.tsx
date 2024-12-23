import { X } from "lucide-react";

interface UploadedFileProps {
  filename: string;
  removeFile(filename: string): void;
}

function UploadedFile({ filename, removeFile }: UploadedFileProps) {
  function trimName(name: string) {
    let splitted = name.split(".");
    if (splitted[0].length < 15) return name;
    return (
      splitted[0].slice(0, 4) +
      "..." +
      splitted[0].slice(-3) +
      "." +
      splitted[1]
    );
  }

  return (
    <div className="file bg-[#ffe2cd]  pt-[.2rem] overflow-hidden  rounded text-xs text-neutral-600  flex flex-col">
      <span className="px-1 cursor-default mb-[.1rem] flex gap-1 ">
        {trimName(filename)}
        <button
          className="text-neutral-600 "
          onClick={() => {
            removeFile(filename);
          }}
        >
          <X className="w-3 h-3" />
        </button>
      </span>
      <div className={`uploading-animation ${filename}`}></div>
    </div>
  );
}

export { UploadedFile };
