"use client";

import { useQuery } from "@tanstack/react-query";
import {
  getPlaybackDevices,
  getSpotifySettings,
  getVoiceOptions,
  getVoicePreferences,
} from "@/lib/api/preferences";
import { queryKeys } from "@/lib/query-keys";

export function useVoiceOptions() {
  return useQuery({
    queryKey: queryKeys.voiceOptions,
    queryFn: getVoiceOptions,
  });
}

export function useVoicePreferences() {
  return useQuery({
    queryKey: queryKeys.voicePreferences,
    queryFn: getVoicePreferences,
  });
}

export function usePlaybackDevices() {
  return useQuery({
    queryKey: queryKeys.playbackDevices,
    queryFn: getPlaybackDevices,
  });
}

export function useSpotifySettings() {
  return useQuery({
    queryKey: queryKeys.spotifySettings,
    queryFn: getSpotifySettings,
  });
}
