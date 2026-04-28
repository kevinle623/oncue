"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { disconnectSpotify } from "@/lib/api/integrations";
import { queryKeys } from "@/lib/query-keys";

export function useDisconnectSpotify() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: disconnectSpotify,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: queryKeys.integrations });
    },
  });
}
