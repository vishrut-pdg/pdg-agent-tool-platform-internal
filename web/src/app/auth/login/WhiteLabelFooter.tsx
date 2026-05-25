"use client";

import React, { useContext } from "react";
import { SettingsContext } from "@/providers/SettingsProvider";
import Text from "@/refresh-components/texts/Text";

export default function WhiteLabelFooter() {
  const settings = useContext(SettingsContext);
  const enterpriseSettings = settings?.enterpriseSettings;

  const supportEmail = enterpriseSettings?.support_email;
  const supportUrl = enterpriseSettings?.support_url;
  const footerBranding = enterpriseSettings?.footer_branding;

  if (!supportEmail && !supportUrl && !footerBranding) {
    return null;
  }

  return (
    <div className="w-full flex flex-col items-center gap-2 mt-6">
      {(supportEmail || supportUrl) && (
        <div className="flex flex-row items-center gap-3">
          {supportEmail && (
            <a
              href={`mailto:${supportEmail}`}
              className="text-text-03 hover:text-text-05 underline-offset-2 hover:underline"
            >
              <Text secondaryBody text03>
                Contact support
              </Text>
            </a>
          )}
          {supportEmail && supportUrl && (
            <Text secondaryBody text03>
              ·
            </Text>
          )}
          {supportUrl && (
            <a
              href={supportUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-text-03 hover:text-text-05 underline-offset-2 hover:underline"
            >
              <Text secondaryBody text03>
                Help center
              </Text>
            </a>
          )}
        </div>
      )}
      {footerBranding && (
        <Text as="p" secondaryBody text03>
          {footerBranding}
        </Text>
      )}
    </div>
  );
}
