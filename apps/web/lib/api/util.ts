/**
 * Tiny artificial delay so mock fetches feel like real network requests.
 * Lets us see loading states during development. Remove when wiring real APIs.
 */
export function delay(ms = 200): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
