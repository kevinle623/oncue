import type { Metadata } from "next";
import { SettingsScreen } from "@/components/screens/settings";

export const metadata: Metadata = {
  title: "Settings — OnCue",
};

export default function SettingsRoute() {
  return <SettingsScreen />;
}
