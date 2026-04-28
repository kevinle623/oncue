import type { UsageSummary } from "@/types/api";
import { mockUsage } from "@/lib/api/mocks";
import { delay } from "@/lib/api/util";

export async function getUsage(): Promise<UsageSummary> {
  await delay();
  return mockUsage;
}
