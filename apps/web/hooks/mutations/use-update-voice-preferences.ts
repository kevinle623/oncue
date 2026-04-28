"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateVoicePreferences } from "@/lib/api/preferences";
import { queryKeys } from "@/lib/query-keys";
import type { VoicePreferences } from "@/types/api";

export function useUpdateVoicePreferences() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (patch: Partial<VoicePreferences>) =>
      updateVoicePreferences(patch),
    onSuccess: (prefs) => {
      qc.setQueryData(queryKeys.voicePreferences, prefs);
    },
  });
}
