"use client";

import { usePathname } from "next/navigation";
import { useCallback, useState } from "react";
import { DesktopSidebar } from "@/components/layout/desktop-sidebar";
import { MobileHeader } from "@/components/layout/mobile-header";
import { MobileTabBar } from "@/components/layout/mobile-tab-bar";
import { preferences } from "@/lib/preferences";

const COLLAPSED_WIDTH = "66px";
const EXPANDED_WIDTH = "16rem";

export function AppShell({
  children,
  initialSidebarCollapsed = false,
}: {
  children: React.ReactNode;
  initialSidebarCollapsed?: boolean;
}) {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(initialSidebarCollapsed);

  const handleToggle = useCallback(() => {
    setCollapsed((prev) => {
      const next = !prev;
      preferences.set("sidebar-collapsed", String(next));
      return next;
    });
  }, []);

  const sidebarWidth = collapsed ? COLLAPSED_WIDTH : EXPANDED_WIDTH;

  return (
    <>
      <DesktopSidebar
        pathname={pathname}
        collapsed={collapsed}
        onToggle={handleToggle}
      />
      <MobileHeader />
      <main
        className="min-h-svh pt-16 pb-24 transition-[margin-left] duration-300 ease-in-out lg:pt-0 lg:pb-0 max-lg:!ml-0"
        style={{ marginLeft: sidebarWidth }}
      >
        {children}
      </main>
      <MobileTabBar pathname={pathname} />
    </>
  );
}
