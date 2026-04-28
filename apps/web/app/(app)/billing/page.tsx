import type { Metadata } from "next";
import { BillingScreen } from "@/components/screens/billing";

export const metadata: Metadata = {
  title: "Billing — OnCue",
};

export default function BillingRoute() {
  return <BillingScreen />;
}
