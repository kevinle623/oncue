import { cn } from "@/lib/utils";

export function StatusDot({
  className,
  pulse = false,
}: {
  className?: string;
  pulse?: boolean;
}) {
  return (
    <span
      className={cn(
        "bg-accent inline-block size-1.5 rounded-full",
        pulse && "animate-pulse",
        className,
      )}
      aria-hidden
    />
  );
}
