import type { Call, CallTurn } from "@/types/api";
import { mockCallTurns, mockCalls } from "@/lib/api/mocks";
import { delay } from "@/lib/api/util";

export async function listCalls(): Promise<Call[]> {
  await delay();
  return mockCalls;
}

export async function getCall(
  id: string,
): Promise<{ call: Call; turns: CallTurn[] } | null> {
  await delay();
  const call = mockCalls.find((c) => c.id === id);
  if (!call) return null;
  return { call, turns: mockCallTurns[id] ?? [] };
}
