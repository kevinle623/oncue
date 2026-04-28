import Link from "next/link";
import { NAV_ITEMS } from "@/components/layout/nav-config";
import { cn } from "@/lib/utils";

export function MobileTabBar({ pathname }: { pathname: string }) {
  return (
    <nav
      className="border-border bg-surface-lowest fixed bottom-0 left-0 z-50 flex w-full items-center justify-around border-t px-2 py-3 lg:hidden"
      style={{ paddingBottom: "max(0.75rem, env(safe-area-inset-bottom))" }}
    >
      {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
        const isActive = pathname === href || pathname.startsWith(`${href}/`);
        return (
          <Link
            key={href}
            href={href}
            className={cn(
              "flex touch-manipulation flex-col items-center justify-center gap-1 transition-colors",
              isActive ? "text-accent" : "text-muted-foreground",
            )}
          >
            <Icon className="size-5" />
            <span className="text-[10px] tracking-[0.12em] uppercase">
              {label}
            </span>
          </Link>
        );
      })}
    </nav>
  );
}
