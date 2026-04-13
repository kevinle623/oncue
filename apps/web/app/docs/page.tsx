import type { Metadata } from "next";
import { DocPage } from "@/components/layout/doc-page";

export const metadata: Metadata = {
  title: "Documentation — OnCue",
  description: "How OnCue works and what you can say to it.",
};

export default function DocsPage() {
  return (
    <DocPage eyebrow="Documentation" title="How OnCue works">
      <p>
        OnCue is a voice assistant that runs over a phone call. Save the OnCue
        number to your speed dial, call it, and speak naturally. We translate
        your intent into actions on the services you&apos;ve connected.
      </p>

      <h2>Getting started</h2>
      <ul>
        <li>Reserve your access — beta slots open monthly.</li>
        <li>Connect an integration (Spotify is live, more coming).</li>
        <li>Save OnCue to your speed dial. Call it. Talk to it.</li>
      </ul>

      <h2>What you can say</h2>
      <ul>
        <li>
          <code>&ldquo;Play something sad.&rdquo;</code>
        </li>
        <li>
          <code>&ldquo;Shuffle my late night drive playlist at 40%.&rdquo;</code>
        </li>
        <li>
          <code>&ldquo;Turn on the driveway lights.&rdquo;</code>
        </li>
        <li>
          <code>&ldquo;Summarize my last call.&rdquo;</code>
        </li>
      </ul>

      <h2>Supported integrations</h2>
      <ul>
        <li>Spotify (available now)</li>
        <li>Apple Music, WhatsApp, Waze, Google Calendar, Notion (in progress)</li>
      </ul>

      <h2>Open source</h2>
      <p>
        OnCue is developed in the open at{" "}
        <a
          href="https://github.com/kevinle623/oncue"
          target="_blank"
          rel="noopener noreferrer"
        >
          github.com/kevinle623/oncue
        </a>
        . Issues and contributions welcome.
      </p>
    </DocPage>
  );
}
