import type { User } from "@/types/api";
import { mockUser } from "@/lib/api/mocks";
import { delay } from "@/lib/api/util";

export async function getProfile(): Promise<User> {
  await delay();
  return mockUser;
}

export async function updateProfile(
  patch: Partial<Pick<User, "display_name" | "phone_number">>,
): Promise<User> {
  await delay();
  return { ...mockUser, ...patch, updated_at: new Date().toISOString() };
}
