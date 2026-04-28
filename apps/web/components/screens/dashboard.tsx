import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { SectionBody } from "@/components/common/section-body";
import { SectionLabel } from "@/components/common/section-label";

export function DashboardScreen() {
  return (
    <Container className="px-8 py-16">
      <SectionLabel>Dashboard</SectionLabel>
      <DisplayHeading className="mt-5" size="md">
        Welcome to OnCue.
      </DisplayHeading>
      <SectionBody className="mt-5">
        The hosted product is in active development. This is the shell — auth,
        Spotify connection, call history, and billing land here.
      </SectionBody>
    </Container>
  );
}
