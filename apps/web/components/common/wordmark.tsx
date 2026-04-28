import { cn } from "@/lib/utils";

type Size = "sm" | "md" | "lg" | "inherit";

const sizeClass: Record<Size, string> = {
  sm: "text-xl",
  md: "text-2xl",
  lg: "text-3xl",
  inherit: "",
};

export function Wordmark({
  className,
  size = "md",
}: {
  className?: string;
  size?: Size;
}) {
  return (
    <span
      className={cn(
        "font-display text-foreground inline-flex items-baseline italic tracking-[-0.02em]",
        sizeClass[size],
        className,
      )}
    >
      <span className="opacity-35">on</span>
      <span>Cue</span>
    </span>
  );
}
