"use client";

import { useQuery } from "@tanstack/react-query";
import { getUsage } from "@/lib/api/usage";
import { queryKeys } from "@/lib/query-keys";

export function useUsage() {
  return useQuery({
    queryKey: queryKeys.usage,
    queryFn: getUsage,
  });
}
