import { cn } from "@/lib/utils";
import { StatusDot } from "@/components/common/status-dot";

export function Wordmark({
  className,
  size = "md",
}: {
  className?: string;
  size?: "md" | "lg";
}) {
  return (
    <span
      className={cn(
        "font-heading text-accent inline-flex items-center gap-1.5 font-black tracking-tighter uppercase",
        size === "md" ? "text-xl" : "text-2xl",
        className,
      )}
    >
      OnCue
      <StatusDot className="mt-1" />
    </span>
  );
}
