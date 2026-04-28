"use client";

import { Container } from "@/components/common/container";
import { DisplayHeading } from "@/components/common/display-heading";
import { SectionBody } from "@/components/common/section-body";
import { SectionLabel } from "@/components/common/section-label";
import { Wordmark } from "@/components/common/wordmark";
import { useProfile } from "@/hooks/queries/use-profile";

export function DashboardScreen() {
  const { data: profile, isLoading } = useProfile();
  const firstName = profile?.display_name?.split(" ")[0] ?? "there";

  return (
    <Container className="px-8 py-16">
      <SectionLabel>Dashboard</SectionLabel>
      <DisplayHeading className="mt-5" size="md">
        {isLoading ? (
          <>
            Welcome to <Wordmark size="inherit" />.
          </>
        ) : (
          <>
            Good morning, {firstName}.
          </>
        )}
      </DisplayHeading>
      <SectionBody className="mt-5">
        Your <Wordmark size="inherit" /> number is active and ready to take
        calls. Real screen content lands once the design is translated; this
        page proves the data layer is wired (TanStack Query → service layer →
        mock fixtures).
      </SectionBody>
    </Container>
  );
}
