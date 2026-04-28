/**
 * Frontend types for the OnCue API.
 *
 * These mirror `apps/api/src/oncue/dtos/*` where they exist, and define
 * shapes the UI needs that the backend hasn't modeled yet. Fields marked
 * "// not yet in backend" are the contract — the API will catch up.
 */

export type ISODateString = string;

// ── Core entities (mirror existing Python DTOs) ──────────────────────

export type User = {
  id: string;
  phone_number: string;
  display_name: string | null;
  email: string | null; // not yet in backend (auth provider will populate)
  created_at: ISODateString;
  updated_at: ISODateString;
};

export type CallStatus = "in-progress" | "completed" | "failed" | "no-answer";

export type Call = {
  id: string;
  call_sid: string;
  user_id: string | null;
  status: CallStatus;
  from_number: string;
  to_number: string;
  started_at: ISODateString;
  ended_at: ISODateString | null;
  duration_seconds: number | null; // derived; not yet in backend
  summary: string | null; // not yet in backend (AI-generated one-liner)
};

export type CallTurnRole = "user" | "assistant" | "tool";

export type CallToolCall = {
  name: string;
  display: string; // human-friendly description e.g. "Played Deep Focus on Spotify"
};

export type CallTurn = {
  id: string;
  call_id: string;
  role: CallTurnRole;
  transcript: string | null;
  tool_calls: CallToolCall[] | null;
  offset_seconds: number; // not yet in backend (derived from created_at - call.started_at)
  created_at: ISODateString;
};

// ── Integrations ─────────────────────────────────────────────────────

export type IntegrationId = "spotify" | "trip_planning" | "food_coffee";

export type IntegrationStatus = "connected" | "disconnected" | "coming_soon";

export type Integration = {
  id: IntegrationId;
  name: string;
  status: IntegrationStatus;
  account_label: string | null; // e.g. spotify account email
  launches: string | null; // e.g. "Launching 2026" for coming_soon
};

// ── Stats / usage ────────────────────────────────────────────────────

export type UsageSummary = {
  total_calls: number;
  total_commands: number;
  minutes_used_this_month: number;
  minutes_cap: number;
};

// ── Settings ─────────────────────────────────────────────────────────
// All of this is "not yet in backend" — frontend defines the contract.

export type ResponseLength = "terse" | "standard" | "chatty";

export type VoiceOption = {
  id: string;
  name: string;
};

export type VoicePreferences = {
  voice_id: string;
  response_length: ResponseLength;
  wake_confirmation_tone: boolean;
};

export type PlaybackDevice = {
  id: string;
  name: string;
};

export type SpotifySettings = {
  default_playback_device: string; // device id, or "last_active"
};

// ── Billing ──────────────────────────────────────────────────────────
// Entirely "not yet in backend."

export type PlanTier = "free" | "starter" | "pro";

export type Plan = {
  tier: PlanTier;
  name: string;
  monthly_price_cents: number;
  features: string[];
  next_billing_date: ISODateString;
};

export type PaymentMethod = {
  brand: "visa" | "mastercard" | "amex" | "discover";
  last4: string;
  exp_month: number;
  exp_year: number;
};

export type InvoiceStatus = "paid" | "open" | "void";

export type Invoice = {
  id: string;
  date: ISODateString;
  amount_cents: number;
  status: InvoiceStatus;
  pdf_url: string;
};
