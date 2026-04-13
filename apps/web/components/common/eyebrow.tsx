import { cn } from "@/lib/utils";

export function Eyebrow({
  className,
  tone = "muted",
  ...props
}: React.ComponentProps<"span"> & { tone?: "muted" | "accent" }) {
  return (
    <span
      className={cn(
        "text-xs font-medium tracking-[0.2em] uppercase",
        tone === "accent" ? "text-accent" : "text-muted-foreground",
        className,
      )}
      {...props}
    />
  );
}
