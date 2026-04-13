import { Container } from "@/components/common/container";
import { Eyebrow } from "@/components/common/eyebrow";
import { Section } from "@/components/common/section";
import { AppleMusicIcon } from "@/components/icons/brand/apple-music";
import { GoogleCalendarIcon } from "@/components/icons/brand/google-calendar";
import { NotionIcon } from "@/components/icons/brand/notion";
import { SpotifyIcon } from "@/components/icons/brand/spotify";
import { WazeIcon } from "@/components/icons/brand/waze";
import { WhatsappIcon } from "@/components/icons/brand/whatsapp";
import { Card } from "@/components/ui/card";

const integrations = [
  { label: "Spotify", Icon: SpotifyIcon },
  { label: "Apple Music", Icon: AppleMusicIcon },
  { label: "WhatsApp", Icon: WhatsappIcon },
  { label: "Waze", Icon: WazeIcon },
  { label: "Calendar", Icon: GoogleCalendarIcon },
  { label: "Notion", Icon: NotionIcon },
];

export function Integrations() {
  return (
    <Section id="integrations" className="bg-surface-lowest">
      <Container className="text-center">
        <Eyebrow>Deeply Integrated With</Eyebrow>
        <div className="mt-12 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
          {integrations.map(({ label, Icon }) => (
            <Card
              key={label}
              className="text-muted-foreground/60 ring-border hover:text-foreground hover:ring-border-strong flex aspect-square cursor-pointer items-center justify-center gap-3 rounded-lg border-0 bg-transparent p-6 ring-1 transition-colors"
            >
              <Icon className="size-8" />
              <span className="font-heading text-sm font-bold tracking-wider uppercase">
                {label}
              </span>
            </Card>
          ))}
        </div>
      </Container>
    </Section>
  );
}
