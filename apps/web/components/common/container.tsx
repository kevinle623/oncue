import { cn } from "@/lib/utils";

type Width = "narrow" | "default" | "prose";

const widthClass: Record<Width, string> = {
  narrow: "max-w-[680px]",
  default: "max-w-[1080px]",
  prose: "max-w-3xl",
};

export function Container({
  className,
  width = "default",
  ...props
}: React.ComponentProps<"div"> & { width?: Width }) {
  return (
    <div
      className={cn("mx-auto w-full px-6", widthClass[width], className)}
      {...props}
    />
  );
}
