"use client";

import React, { useContext } from "react";
import { SettingsContext } from "@/providers/SettingsProvider";
import Text from "@/refresh-components/texts/Text";

export default function LoginText() {
  const settings = useContext(SettingsContext);
  const enterpriseSettings = settings?.enterpriseSettings;
  const applicationName = enterpriseSettings?.application_name || "Onyx";

  // The upstream "open source AI platform" tagline is Onyx-specific brand copy.
  // Hide it whenever the deployment has been renamed (white-label) or when an
  // admin has explicitly turned off Onyx branding via the existing flag.
  const isRenamed =
    !!enterpriseSettings?.application_name &&
    enterpriseSettings.application_name !== "Onyx";
  const showOnyxTagline =
    !isRenamed && !enterpriseSettings?.hide_onyx_branding;

  return (
    <div className="w-full flex flex-col ">
      <Text as="p" headingH2 text05>
        Welcome to {applicationName}
      </Text>
      {showOnyxTagline && (
        <Text as="p" text03 mainUiMuted>
          Your open source AI platform for work
        </Text>
      )}
    </div>
  );
}
