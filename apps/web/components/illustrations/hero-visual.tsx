import { FadedImage } from "@/components/illustrations/faded-image";
import { cn } from "@/lib/utils";

export function HeroVisual({ className }: { className?: string }) {
  return (
    <FadedImage
      src="/images/hero.png"
      alt="Night driving scene with warm amber ambient light"
      fill
      sizes="(min-width: 1024px) 50vw, 100vw"
      priority
      className={cn("aspect-[3/2] w-full", className)}
    />
  );
}
