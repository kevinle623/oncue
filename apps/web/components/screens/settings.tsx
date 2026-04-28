import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { SectionBody } from "@/components/common/section-body";
import { SectionLabel } from "@/components/common/section-label";

export function SettingsScreen() {
  return (
    <Container className="px-8 py-16">
      <SectionLabel>Settings</SectionLabel>
      <DisplayHeading className="mt-5" size="md">
        Account settings.
      </DisplayHeading>
      <SectionBody className="mt-5">
        Phone number, connected integrations, voice preferences. Coming with
        the hosted launch.
      </SectionBody>
    </Container>
  );
}
