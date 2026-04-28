"use client";

import { useQuery } from "@tanstack/react-query";
import { getProfile } from "@/lib/api/account";
import { queryKeys } from "@/lib/query-keys";

export function useProfile() {
  return useQuery({
    queryKey: queryKeys.profile,
    queryFn: getProfile,
  });
}
