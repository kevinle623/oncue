import { cn } from "@/lib/utils";

export function SectionLabel({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <p
      className={cn(
        "text-accent text-[11px] font-medium tracking-[0.18em] uppercase",
        className,
      )}
    >
      {children}
    </p>
  );
}
