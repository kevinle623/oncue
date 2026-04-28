import { AppShell } from "@/components/layout/app-shell";
import { getServerPreference } from "@/lib/server-preferences";

export default async function AppGroupLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const sidebarCollapsed =
    (await getServerPreference("sidebar-collapsed")) === "true";

  return (
    <AppShell initialSidebarCollapsed={sidebarCollapsed}>{children}</AppShell>
  );
}
