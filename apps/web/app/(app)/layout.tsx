import { AppShell } from "@/components/layout/app-shell";
import { QueryProvider } from "@/components/providers/query-provider";
import { getServerPreference } from "@/lib/server-preferences";

export default async function AppGroupLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const sidebarCollapsed =
    (await getServerPreference("sidebar-collapsed")) === "true";

  return (
    <QueryProvider>
      <AppShell initialSidebarCollapsed={sidebarCollapsed}>{children}</AppShell>
    </QueryProvider>
  );
}
