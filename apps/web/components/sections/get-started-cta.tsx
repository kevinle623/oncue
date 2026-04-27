import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { PrimaryButton } from "@/components/common/primary-button";
import { Reveal } from "@/components/common/reveal";
import { Section } from "@/components/common/section";

const REPO_README = "https://github.com/kevinle623/oncue#readme";

export function GetStartedCta() {
  return (
    <Section
      id="get-started"
      tone="surface-low"
      className="text-center"
      style={{ paddingBlock: 120 }}
    >
      <Container className="max-w-[560px] px-6">
        <Reveal>
          <DisplayHeading size="lg">
            Two ways in.
            <br />
            <em>One available today.</em>
          </DisplayHeading>
          <p className="text-muted-foreground mx-auto mt-5 mb-11 max-w-[460px] text-base leading-[1.6] font-light">
            OnCue is open source. Clone the repo, plug in your own keys, and
            you have a working voice assistant in an afternoon. A hosted
            version with a full UI is coming — sit tight or build now.
          </p>
          <PrimaryButton href={REPO_README}>Read the setup guide</PrimaryButton>
          <p className="text-muted-foreground mt-4 text-xs tracking-[0.04em]">
            Self-host today &nbsp;·&nbsp; Hosted product coming
          </p>
        </Reveal>
      </Container>
    </Section>
  );
}
