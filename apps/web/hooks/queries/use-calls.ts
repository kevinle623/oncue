"use client";

import { useQuery } from "@tanstack/react-query";
import { getCall, listCalls } from "@/lib/api/calls";
import { queryKeys } from "@/lib/query-keys";

export function useCalls() {
  return useQuery({
    queryKey: queryKeys.calls.list(),
    queryFn: listCalls,
  });
}

export function useCall(id: string | null) {
  return useQuery({
    queryKey: id ? queryKeys.calls.detail(id) : queryKeys.calls.all,
    queryFn: () => (id ? getCall(id) : Promise.resolve(null)),
    enabled: id !== null,
  });
}
