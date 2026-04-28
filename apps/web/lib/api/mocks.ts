import type {
  Call,
  CallTurn,
  Integration,
  Invoice,
  PaymentMethod,
  PlaybackDevice,
  Plan,
  SpotifySettings,
  UsageSummary,
  User,
  VoiceOption,
  VoicePreferences,
} from "@/types/api";

export const ONCUE_NUMBER_E164 = "+14150138492";
export const ONCUE_NUMBER_DISPLAY = "+1 (415) 013-8492";

export const mockUser: User = {
  id: "user_alex",
  phone_number: "+15551234567",
  display_name: "Alex Mercer",
  email: "alex@gmail.com",
  created_at: "2026-01-15T09:00:00Z",
  updated_at: "2026-04-01T10:00:00Z",
};

export const mockCalls: Call[] = [
  {
    id: "call_1",
    call_sid: "CA1",
    user_id: mockUser.id,
    status: "completed",
    from_number: mockUser.phone_number,
    to_number: ONCUE_NUMBER_E164,
    started_at: "2026-04-27T09:41:00-07:00",
    ended_at: "2026-04-27T09:43:14-07:00",
    duration_seconds: 134,
    summary: "Played focus playlist, adjusted volume twice",
  },
  {
    id: "call_2",
    call_sid: "CA2",
    user_id: mockUser.id,
    status: "completed",
    from_number: mockUser.phone_number,
    to_number: ONCUE_NUMBER_E164,
    started_at: "2026-04-27T08:03:00-07:00",
    ended_at: "2026-04-27T08:03:47-07:00",
    duration_seconds: 47,
    summary: "Skipped track, asked what song was playing",
  },
  {
    id: "call_3",
    call_sid: "CA3",
    user_id: mockUser.id,
    status: "completed",
    from_number: mockUser.phone_number,
    to_number: ONCUE_NUMBER_E164,
    started_at: "2026-04-26T18:28:00-07:00",
    ended_at: "2026-04-26T18:32:02-07:00",
    duration_seconds: 242,
    summary: "Queued road trip playlist, turned volume up",
  },
  {
    id: "call_4",
    call_sid: "CA4",
    user_id: mockUser.id,
    status: "completed",
    from_number: mockUser.phone_number,
    to_number: ONCUE_NUMBER_E164,
    started_at: "2026-04-26T14:15:00-07:00",
    ended_at: "2026-04-26T14:16:08-07:00",
    duration_seconds: 68,
    summary: "Asked what song was playing",
  },
];

export const mockCallTurns: Record<string, CallTurn[]> = {
  call_1: [
    {
      id: "t1",
      call_id: "call_1",
      role: "user",
      transcript: "Play something to help me focus.",
      tool_calls: null,
      offset_seconds: 2,
      created_at: "2026-04-27T09:41:02-07:00",
    },
    {
      id: "t2",
      call_id: "call_1",
      role: "tool",
      transcript: null,
      tool_calls: [
        {
          name: "spotify_search_tracks",
          display: 'Searched Spotify for "focus" playlists',
        },
      ],
      offset_seconds: 4,
      created_at: "2026-04-27T09:41:04-07:00",
    },
    {
      id: "t3",
      call_id: "call_1",
      role: "assistant",
      transcript: "Playing Deep Focus on Spotify.",
      tool_calls: null,
      offset_seconds: 4,
      created_at: "2026-04-27T09:41:04-07:00",
    },
    {
      id: "t4",
      call_id: "call_1",
      role: "user",
      transcript: "Turn it down a bit.",
      tool_calls: null,
      offset_seconds: 34,
      created_at: "2026-04-27T09:41:34-07:00",
    },
    {
      id: "t5",
      call_id: "call_1",
      role: "tool",
      transcript: null,
      tool_calls: [
        { name: "spotify_set_volume", display: "Set Spotify volume to 60%" },
      ],
      offset_seconds: 36,
      created_at: "2026-04-27T09:41:36-07:00",
    },
    {
      id: "t6",
      call_id: "call_1",
      role: "assistant",
      transcript: "Done, volume at 60%.",
      tool_calls: null,
      offset_seconds: 36,
      created_at: "2026-04-27T09:41:36-07:00",
    },
    {
      id: "t7",
      call_id: "call_1",
      role: "user",
      transcript: "What's this song?",
      tool_calls: null,
      offset_seconds: 72,
      created_at: "2026-04-27T09:42:12-07:00",
    },
    {
      id: "t8",
      call_id: "call_1",
      role: "assistant",
      transcript: "That's Weightless by Marconi Union.",
      tool_calls: null,
      offset_seconds: 74,
      created_at: "2026-04-27T09:42:14-07:00",
    },
  ],
};

export const mockIntegrations: Integration[] = [
  {
    id: "spotify",
    name: "Spotify",
    status: "connected",
    account_label: "alex@gmail.com",
    launches: null,
  },
  {
    id: "trip_planning",
    name: "Trip Planning",
    status: "coming_soon",
    account_label: null,
    launches: "Launching 2026",
  },
  {
    id: "food_coffee",
    name: "Food & Coffee",
    status: "coming_soon",
    account_label: null,
    launches: "Launching 2026",
  },
];

export const mockUsage: UsageSummary = {
  total_calls: 24,
  total_commands: 87,
  minutes_used_this_month: 14,
  minutes_cap: 60,
};

export const mockVoiceOptions: VoiceOption[] = [
  { id: "aria", name: "Aria" },
  { id: "nova", name: "Nova" },
  { id: "echo", name: "Echo" },
  { id: "fable", name: "Fable" },
];

export const mockVoicePreferences: VoicePreferences = {
  voice_id: "aria",
  response_length: "standard",
  wake_confirmation_tone: true,
};

export const mockPlaybackDevices: PlaybackDevice[] = [
  { id: "last_active", name: "Last active device" },
  { id: "iphone_alex", name: "My iPhone" },
  { id: "macbook_pro", name: "MacBook Pro" },
];

export const mockSpotifySettings: SpotifySettings = {
  default_playback_device: "last_active",
};

export const mockPlan: Plan = {
  tier: "starter",
  name: "Starter",
  monthly_price_cents: 900,
  features: [
    "60 minutes/month",
    "All live integrations",
    "Email support",
    "Beta access to new integrations",
  ],
  next_billing_date: "2026-05-15T00:00:00Z",
};

export const mockPaymentMethod: PaymentMethod = {
  brand: "visa",
  last4: "4242",
  exp_month: 8,
  exp_year: 27,
};

export const mockInvoices: Invoice[] = [
  {
    id: "in_1",
    date: "2026-04-15T00:00:00Z",
    amount_cents: 900,
    status: "paid",
    pdf_url: "#",
  },
  {
    id: "in_2",
    date: "2026-03-15T00:00:00Z",
    amount_cents: 900,
    status: "paid",
    pdf_url: "#",
  },
  {
    id: "in_3",
    date: "2026-02-15T00:00:00Z",
    amount_cents: 900,
    status: "paid",
    pdf_url: "#",
  },
];
