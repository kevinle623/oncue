import { cn } from "@/lib/utils";

type Tone = "default" | "surface-low" | "accent-soft";

const toneClass: Record<Tone, string> = {
  default: "bg-background",
  "surface-low": "bg-surface-low border-border border-y",
  "accent-soft":
    "bg-accent-soft border-y border-[rgba(26,24,20,0.12)]",
};

type Padding = "default" | "compact";

const paddingClass: Record<Padding, string> = {
  default: "py-[100px]",
  compact: "py-20",
};

export function Section({
  className,
  tone = "default",
  padding = "default",
  children,
  ...props
}: React.ComponentProps<"section"> & {
  tone?: Tone;
  padding?: Padding;
}) {
  return (
    <section
      className={cn(
        "relative px-0",
        toneClass[tone],
        paddingClass[padding],
        className,
      )}
      {...props}
    >
      {children}
    </section>
  );
}
