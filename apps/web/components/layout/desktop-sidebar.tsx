"use client";

import { PanelLeft } from "lucide-react";
import Link from "next/link";
import { useCallback, useState } from "react";
import { Wordmark } from "@/components/common/wordmark";
import { NAV_ITEMS } from "@/components/layout/nav-config";
import { SidebarUserRow } from "@/components/layout/sidebar-user-row";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";

const COLLAPSED_WIDTH = "66px";
const EXPANDED_WIDTH = "16rem";

function SidebarTooltip({
  enabled,
  children,
  content,
}: {
  enabled: boolean;
  children: React.ReactNode;
  content: React.ReactNode;
}) {
  const [hovered, setHovered] = useState(false);

  const handleOpenChange = useCallback(
    (open: boolean) => setHovered(enabled && open),
    [enabled],
  );

  return (
    <Tooltip open={enabled && hovered} onOpenChange={handleOpenChange}>
      <TooltipTrigger asChild>{children}</TooltipTrigger>
      <TooltipContent side="right">{content}</TooltipContent>
    </Tooltip>
  );
}

export function DesktopSidebar({
  pathname,
  collapsed,
  onToggle,
}: {
  pathname: string;
  collapsed: boolean;
  onToggle: () => void;
}) {
  const [showTooltips, setShowTooltips] = useState(collapsed);

  const handleToggle = useCallback(() => {
    setShowTooltips(false);
    onToggle();
  }, [onToggle]);

  const handleTransitionEnd = useCallback(() => {
    setShowTooltips(collapsed);
  }, [collapsed]);

  return (
    <TooltipProvider delayDuration={0}>
      <aside
        className="border-border bg-surface fixed top-0 left-0 z-50 hidden h-svh flex-col overflow-hidden border-r transition-[width] duration-300 ease-in-out lg:flex"
        style={{ width: collapsed ? COLLAPSED_WIDTH : EXPANDED_WIDTH }}
        onTransitionEnd={handleTransitionEnd}
      >
        <div className="border-border flex items-center gap-2 border-b px-4 py-5">
          <Link
            href="/"
            aria-label="OnCue home"
            className={cn(
              "min-w-0 overflow-hidden transition-all duration-300 ease-in-out",
              collapsed ? "w-0 flex-none opacity-0" : "flex-1 opacity-100",
            )}
          >
            <Wordmark size="md" />
          </Link>
          <SidebarTooltip
            enabled={showTooltips}
            content={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            <button
              type="button"
              onClick={handleToggle}
              aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
              className="text-muted-foreground hover:text-foreground flex flex-shrink-0 items-center justify-center transition-colors"
            >
              <PanelLeft
                className={cn(
                  "size-[18px] transition-transform duration-300",
                  collapsed && "rotate-180",
                )}
              />
            </button>
          </SidebarTooltip>
        </div>

        <nav className="flex flex-1 flex-col gap-0.5 overflow-y-auto p-2">
          <p
            className={cn(
              "text-muted px-3 pt-3 pb-1 text-[10px] font-medium tracking-[0.14em] uppercase transition-opacity duration-300",
              collapsed ? "opacity-0" : "opacity-100",
            )}
          >
            Menu
          </p>
          {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
            const isActive =
              pathname === href || pathname.startsWith(`${href}/`);
            return (
              <SidebarTooltip key={href} enabled={showTooltips} content={label}>
                <Link
                  href={href}
                  className={cn(
                    "flex items-center gap-2.5 rounded-md px-3 py-2.5 text-sm whitespace-nowrap transition-colors",
                    isActive
                      ? "bg-accent-soft text-accent font-medium"
                      : "text-muted-foreground hover:bg-foreground/[0.05] hover:text-foreground",
                  )}
                >
                  <Icon className="size-4 flex-shrink-0" />
                  <span
                    className={cn(
                      "transition-opacity duration-300",
                      collapsed ? "opacity-0" : "opacity-100",
                    )}
                  >
                    {label}
                  </span>
                </Link>
              </SidebarTooltip>
            );
          })}
        </nav>

        <div className="border-border border-t p-2">
          <SidebarUserRow collapsed={collapsed} />
        </div>
      </aside>
    </TooltipProvider>
  );
}
