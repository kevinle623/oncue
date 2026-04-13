import { cn } from "@/lib/utils";

const bars = [16, 32, 48, 24, 40, 20, 36];

export function HeroPhone({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "border-border bg-surface-lowest relative aspect-[9/18.5] w-full max-w-[340px] rounded-[3rem] border p-4",
        className,
      )}
    >
      <div className="relative flex h-full w-full flex-col items-center justify-center overflow-hidden rounded-[2.2rem] bg-black">
        <div
          aria-hidden
          className="bg-surface-lowest absolute top-6 left-1/2 z-20 h-6 w-20 -translate-x-1/2 rounded-full"
        />
        <div
          aria-hidden
          className="absolute inset-0 opacity-60"
          style={{
            background:
              "radial-gradient(circle at 50% 40%, rgba(255,181,71,0.35) 0%, transparent 55%), radial-gradient(circle at 30% 70%, rgba(255,181,71,0.15) 0%, transparent 60%)",
          }}
        />
        <div className="relative z-10 flex flex-col items-center gap-4">
          <div className="flex h-12 items-end gap-1">
            {bars.map((h, i) => (
              <span
                key={i}
                className="bg-accent w-1 rounded-full"
                style={{ height: `${h}px` }}
              />
            ))}
          </div>
          <span className="text-accent font-sans text-[10px] tracking-[0.3em] uppercase">
            Listening...
          </span>
        </div>
      </div>
    </div>
  );
}
