import type { Metadata } from "next";
import { CallsScreen } from "@/components/screens/calls";

export const metadata: Metadata = {
  title: "Calls — OnCue",
};

export default function CallsRoute() {
  return <CallsScreen />;
}
