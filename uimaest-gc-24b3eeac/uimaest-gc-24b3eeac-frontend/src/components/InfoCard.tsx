interface InfoProps {
  heading: string;
  description: string;
}
export const InfoCard = ({ heading, description }: InfoProps) => {
  return (
    <div className="bg-neutral-50 flex flex-col gap-1 justify-start p-4 text-neutral-800 rounded-lg text-xs w-40 h-40">
      <h1 className="flex font-semibold text-sm items-center w-full">
        {" "}
        {/* <Lightbulb className="w-4 h-4" /> */}
        {heading}
      </h1>

      <p className="break-words">{description}</p>
    </div>
  );
};
