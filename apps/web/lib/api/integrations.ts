import type { Integration } from "@/types/api";
import { mockIntegrations } from "@/lib/api/mocks";
import { delay } from "@/lib/api/util";

export async function listIntegrations(): Promise<Integration[]> {
  await delay();
  return mockIntegrations;
}

export async function disconnectSpotify(): Promise<void> {
  await delay();
}
