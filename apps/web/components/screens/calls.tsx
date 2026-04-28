import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { SectionBody } from "@/components/common/section-body";
import { SectionLabel } from "@/components/common/section-label";

export function CallsScreen() {
  return (
    <Container className="px-8 py-16">
      <SectionLabel>Calls</SectionLabel>
      <DisplayHeading className="mt-5" size="md">
        Call history.
      </DisplayHeading>
      <SectionBody className="mt-5">
        A turn-by-turn transcript of every call, plus the actions OnCue took.
        Coming with the hosted launch.
      </SectionBody>
    </Container>
  );
}
