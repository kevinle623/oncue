import { cn } from "@/lib/utils";

export function Divider({ className }: { className?: string }) {
  return (
    <div
      className={cn("bg-border mx-auto h-px w-full max-w-[1080px]", className)}
    />
  );
}
