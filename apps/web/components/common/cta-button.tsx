import Link from "next/link";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type Props = {
  href?: string;
  variant?: "primary" | "outline";
  children: React.ReactNode;
  className?: string;
};

export function CtaButton({
  href = "#",
  variant = "primary",
  children,
  className,
}: Props) {
  return (
    <Button
      asChild
      className={cn(
        "h-auto rounded-sm px-8 py-4 text-xs font-bold tracking-[0.15em] uppercase",
        variant === "primary" &&
          "bg-accent text-accent-foreground hover:bg-accent/90",
        variant === "outline" &&
          "border-border text-foreground hover:border-border-strong border bg-transparent hover:bg-transparent",
        className,
      )}
    >
      <Link href={href}>{children}</Link>
    </Button>
  );
}
