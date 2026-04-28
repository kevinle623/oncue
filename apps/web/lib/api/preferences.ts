import type {
  PlaybackDevice,
  SpotifySettings,
  VoiceOption,
  VoicePreferences,
} from "@/types/api";
import {
  mockPlaybackDevices,
  mockSpotifySettings,
  mockVoiceOptions,
  mockVoicePreferences,
} from "@/lib/api/mocks";
import { delay } from "@/lib/api/util";

export async function getVoiceOptions(): Promise<VoiceOption[]> {
  await delay();
  return mockVoiceOptions;
}

export async function getVoicePreferences(): Promise<VoicePreferences> {
  await delay();
  return mockVoicePreferences;
}

export async function updateVoicePreferences(
  patch: Partial<VoicePreferences>,
): Promise<VoicePreferences> {
  await delay();
  return { ...mockVoicePreferences, ...patch };
}

export async function getPlaybackDevices(): Promise<PlaybackDevice[]> {
  await delay();
  return mockPlaybackDevices;
}

export async function getSpotifySettings(): Promise<SpotifySettings> {
  await delay();
  return mockSpotifySettings;
}

export async function updateSpotifySettings(
  patch: Partial<SpotifySettings>,
): Promise<SpotifySettings> {
  await delay();
  return { ...mockSpotifySettings, ...patch };
}
