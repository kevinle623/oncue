import { cn } from "@/lib/utils";

export function SectionBody({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <p
      className={cn(
        "text-muted-foreground max-w-[520px] text-[17px] leading-[1.65] font-light",
        className,
      )}
    >
      {children}
    </p>
  );
}
