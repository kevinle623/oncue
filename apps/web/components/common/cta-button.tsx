import Link from "next/link";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type Props = {
  href?: string;
  variant?: "primary" | "outline";
  disabled?: boolean;
  disabledLabel?: string;
  children: React.ReactNode;
  className?: string;
};

const baseClasses =
  "h-auto rounded-sm px-8 py-4 text-xs font-bold tracking-[0.15em] uppercase";

const variantClasses = {
  primary: "bg-accent text-accent-foreground hover:bg-accent/90",
  outline:
    "border-border text-foreground hover:border-border-strong border bg-transparent hover:bg-transparent",
};

export function CtaButton({
  href = "#",
  variant = "primary",
  disabled = false,
  disabledLabel = "Coming soon",
  children,
  className,
}: Props) {
  if (disabled) {
    return (
      <span
        aria-disabled
        className={cn(
          baseClasses,
          "border-border text-muted-foreground inline-flex cursor-not-allowed items-center justify-center border bg-transparent",
          className,
        )}
      >
        {disabledLabel}
      </span>
    );
  }

  return (
    <Button
      asChild
      className={cn(baseClasses, variantClasses[variant], className)}
    >
      <Link href={href}>{children}</Link>
    </Button>
  );
}
