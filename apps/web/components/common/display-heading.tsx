import { cn } from "@/lib/utils";

type Size = "sm" | "md" | "lg" | "xl";

const sizeClass: Record<Size, string> = {
  // Privacy heading
  sm: "text-[clamp(30px,4vw,44px)]",
  // Default section title
  md: "text-[clamp(34px,5vw,56px)]",
  // CTA / waitlist
  lg: "text-[clamp(36px,6vw,64px)]",
  // Hero
  xl: "text-[clamp(44px,8vw,88px)]",
};

export function DisplayHeading({
  as: Component = "h2",
  size = "md",
  className,
  children,
}: {
  as?: "h1" | "h2" | "h3";
  size?: Size;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <Component
      className={cn(
        "font-display text-foreground leading-[1.05] tracking-[-0.02em]",
        "[&_em]:text-accent [&_em]:italic",
        sizeClass[size],
        className,
      )}
    >
      {children}
    </Component>
  );
}
