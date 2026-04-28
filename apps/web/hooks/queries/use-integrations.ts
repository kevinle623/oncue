"use client";

import { useQuery } from "@tanstack/react-query";
import { listIntegrations } from "@/lib/api/integrations";
import { queryKeys } from "@/lib/query-keys";

export function useIntegrations() {
  return useQuery({
    queryKey: queryKeys.integrations,
    queryFn: listIntegrations,
  });
}
