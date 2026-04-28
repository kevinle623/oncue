import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { SectionBody } from "@/components/common/section-body";
import { SectionLabel } from "@/components/common/section-label";

export function BillingScreen() {
  return (
    <Container className="px-8 py-16">
      <SectionLabel>Billing</SectionLabel>
      <DisplayHeading className="mt-5" size="md">
        Plan and usage.
      </DisplayHeading>
      <SectionBody className="mt-5">
        Stripe-backed subscription and usage metering. Wired up alongside the
        hosted launch.
      </SectionBody>
    </Container>
  );
}
