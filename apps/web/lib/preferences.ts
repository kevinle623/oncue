export type PreferenceKey = "sidebar-collapsed";

export const PREFERENCE_PREFIX = "oncue:";

const SSR_KEYS: Set<PreferenceKey> = new Set(["sidebar-collapsed"]);

export interface PreferencesStore {
  get(key: PreferenceKey): string | null;
  set(key: PreferenceKey, value: string): void;
  remove(key: PreferenceKey): void;
}

function prefixed(key: PreferenceKey): string {
  return `${PREFERENCE_PREFIX}${key}`;
}

function setCookie(name: string, value: string) {
  document.cookie = `${name}=${encodeURIComponent(value)};path=/;max-age=${60 * 60 * 24 * 365};SameSite=Lax`;
}

function removeCookie(name: string) {
  document.cookie = `${name}=;path=/;max-age=0`;
}

export const preferences: PreferencesStore = {
  get(key) {
    if (typeof window === "undefined") return null;
    return localStorage.getItem(prefixed(key));
  },
  set(key, value) {
    if (typeof window === "undefined") return;
    localStorage.setItem(prefixed(key), value);
    if (SSR_KEYS.has(key)) setCookie(prefixed(key), value);
  },
  remove(key) {
    if (typeof window === "undefined") return;
    localStorage.removeItem(prefixed(key));
    if (SSR_KEYS.has(key)) removeCookie(prefixed(key));
  },
};
