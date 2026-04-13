import { cn } from "@/lib/utils";

export function RadialGlow({ className }: { className?: string }) {
  return (
    <div
      aria-hidden
      className={cn(
        "radial-glow pointer-events-none absolute inset-0 -z-10",
        className,
      )}
    />
  );
}
