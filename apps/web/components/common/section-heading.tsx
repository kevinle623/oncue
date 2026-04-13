import { cn } from "@/lib/utils";
import { Eyebrow } from "./eyebrow";

export function SectionHeading({
  eyebrow,
  title,
  align = "left",
  className,
}: {
  eyebrow?: string;
  title: React.ReactNode;
  align?: "left" | "center";
  className?: string;
}) {
  return (
    <div
      className={cn(
        "space-y-4",
        align === "center" && "text-center",
        className,
      )}
    >
      {eyebrow && <Eyebrow tone="accent">{eyebrow}</Eyebrow>}
      <h2 className="font-heading text-4xl font-black tracking-[-0.03em] md:text-5xl">
        {title}
      </h2>
    </div>
  );
}
