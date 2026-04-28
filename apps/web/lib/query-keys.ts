/**
 * Centralized TanStack Query keys. Mutations import from here to invalidate.
 * Keep keys as `as const` tuples so cache reads are type-safe.
 */
export const queryKeys = {
  profile: ["profile"] as const,
  integrations: ["integrations"] as const,
  usage: ["usage"] as const,
  voiceOptions: ["voice-options"] as const,
  voicePreferences: ["voice-preferences"] as const,
  playbackDevices: ["playback-devices"] as const,
  spotifySettings: ["spotify-settings"] as const,
  plan: ["plan"] as const,
  paymentMethod: ["payment-method"] as const,
  invoices: ["invoices"] as const,
  calls: {
    all: ["calls"] as const,
    list: () => ["calls", "list"] as const,
    detail: (id: string) => ["calls", "detail", id] as const,
  },
} as const;
