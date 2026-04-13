import { cn } from "@/lib/utils";

export function Section({
  className,
  children,
  ...props
}: React.ComponentProps<"section">) {
  return (
    <section
      className={cn(
        "relative flex flex-col justify-center overflow-hidden px-0 py-24 lg:min-h-screen lg:py-20",
        className,
      )}
      {...props}
    >
      {children}
    </section>
  );
}
