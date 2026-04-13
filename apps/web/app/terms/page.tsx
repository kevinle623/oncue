import type { Metadata } from "next";
import { DocPage } from "@/components/layout/doc-page";

export const metadata: Metadata = {
  title: "Terms of Service — OnCue",
  description: "The rules for using OnCue.",
};

export default function TermsPage() {
  return (
    <DocPage eyebrow="Legal" title="Terms of Service" updated="April 2026">
      <p>
        By using OnCue you agree to these terms. If you don&apos;t, please
        don&apos;t use the service.
      </p>

      <h2>Use of the service</h2>
      <p>
        OnCue is provided as-is during beta. It is intended for hands-free use
        by drivers who already comply with local laws regarding phone use while
        operating a vehicle.
      </p>

      <h2>Accounts &amp; integrations</h2>
      <p>
        You are responsible for the accounts and integrations you connect. We
        act on voice commands in good faith; we are not liable for actions
        triggered on third-party services you&apos;ve authorized.
      </p>

      <h2>Availability</h2>
      <p>
        Beta features may change or be withdrawn without notice. We aim for high
        availability but do not guarantee uninterrupted service.
      </p>

      <h2>Contact</h2>
      <p>
        Questions: <a href="mailto:hello@oncue.app">hello@oncue.app</a>.
      </p>
    </DocPage>
  );
}
