"use client";

import { LogOut } from "lucide-react";
import { cn } from "@/lib/utils";

const MOCK_USER = {
  name: "Alex Mercer",
  email: "alex@gmail.com",
  initials: "AM",
};

export function SidebarUserRow({ collapsed }: { collapsed: boolean }) {
  return (
    <div
      className={cn(
        "flex items-center gap-2.5 rounded-md py-2",
        collapsed ? "justify-center px-0" : "px-3",
      )}
    >
      <div className="bg-accent text-accent-foreground flex size-7 flex-shrink-0 items-center justify-center rounded-full text-[11px] font-semibold">
        {MOCK_USER.initials}
      </div>
      <div
        className={cn(
          "min-w-0 flex-1 transition-opacity duration-300",
          collapsed ? "pointer-events-none w-0 opacity-0" : "opacity-100",
        )}
      >
        <div className="text-foreground truncate text-[13px] font-medium">
          {MOCK_USER.name}
        </div>
        <div className="text-muted-foreground truncate text-[11px]">
          {MOCK_USER.email}
        </div>
      </div>
      <button
        type="button"
        aria-label="Sign out"
        className={cn(
          "text-muted-foreground hover:text-foreground flex-shrink-0 p-1 transition-[opacity,color] duration-200",
          collapsed ? "pointer-events-none opacity-0" : "opacity-100",
        )}
      >
        <LogOut className="size-[15px]" />
      </button>
    </div>
  );
}
