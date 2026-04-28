import type { Metadata } from "next";
import { DashboardScreen } from "@/components/screens/dashboard";

export const metadata: Metadata = {
  title: "Dashboard — OnCue",
};

export default function DashboardRoute() {
  return <DashboardScreen />;
}
