"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateProfile } from "@/lib/api/account";
import { queryKeys } from "@/lib/query-keys";
import type { User } from "@/types/api";

export function useUpdateProfile() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (
      patch: Partial<Pick<User, "display_name" | "phone_number">>,
    ) => updateProfile(patch),
    onSuccess: (user) => {
      qc.setQueryData(queryKeys.profile, user);
    },
  });
}
