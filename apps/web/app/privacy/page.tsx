import type { Metadata } from "next";
import { DocPage } from "@/components/layout/doc-page";

export const metadata: Metadata = {
  title: "Privacy Policy — OnCue",
  description: "How OnCue collects, uses, and protects your data.",
};

export default function PrivacyPage() {
  return (
    <DocPage eyebrow="Legal" title="Privacy Policy" updated="April 2026">
      <p>
        OnCue (&ldquo;we&rdquo;, &ldquo;us&rdquo;) is a voice assistant that
        operates over a phone call. This policy describes what we collect, why,
        and how you can control it.
      </p>

      <h2>What we collect</h2>
      <ul>
        <li>
          <strong>Call audio</strong> — streamed to our speech-to-text provider
          during an active call and discarded once transcribed.
        </li>
        <li>
          <strong>Transcripts &amp; intents</strong> — retained to improve
          accuracy. You can request deletion at any time.
        </li>
        <li>
          <strong>Integration tokens</strong> — OAuth credentials for services
          you connect (e.g. Spotify). Stored encrypted and only used to execute
          the actions you request.
        </li>
        <li>
          <strong>Account metadata</strong> — phone number, email, usage
          timestamps.
        </li>
      </ul>

      <h2>What we don&apos;t do</h2>
      <ul>
        <li>We do not sell your data.</li>
        <li>We do not use your voice to train third-party models.</li>
        <li>
          We do not record calls for any purpose beyond real-time transcription.
        </li>
      </ul>

      <h2>Your controls</h2>
      <p>
        Email <a href="mailto:privacy@oncue.app">privacy@oncue.app</a> to export
        your data, disconnect an integration, or delete your account.
      </p>
    </DocPage>
  );
}
