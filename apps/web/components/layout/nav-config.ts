import { CreditCard, LayoutDashboard, Phone, Settings } from "lucide-react";

export type NavItem = {
  href: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
};

export const NAV_ITEMS: readonly NavItem[] = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/calls", label: "Calls", icon: Phone },
  { href: "/settings", label: "Settings", icon: Settings },
  { href: "/billing", label: "Billing", icon: CreditCard },
] as const;
