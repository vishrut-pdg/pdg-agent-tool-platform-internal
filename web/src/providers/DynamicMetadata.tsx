"use client";

import { useEffect, useMemo } from "react";
import { useSettingsContext } from "@/providers/SettingsProvider";

export default function DynamicMetadata() {
  const { enterpriseSettings } = useSettingsContext();

  useEffect(() => {
    const title = enterpriseSettings?.application_name || "Onyx";
    if (document.title !== title) {
      document.title = title;
    }
  }, [enterpriseSettings]);

  // Expose the white-label brand color as a CSS custom property at the root
  // so it can be referenced by any component (e.g. via `style={{ color: "var(--brand-primary)" }}`)
  // or by the tailwind `brand` color in tailwind config.
  useEffect(() => {
    const root = document.documentElement;
    const color = enterpriseSettings?.primary_brand_color;
    if (color) {
      root.style.setProperty("--brand-primary", color);
    } else {
      root.style.removeProperty("--brand-primary");
    }
  }, [enterpriseSettings]);

  // Cache-buster so the favicon re-fetches after an admin uploads a new logo.
  const cacheBuster = useMemo(
    () => Date.now(),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [enterpriseSettings]
  );

  // Precedence: env-driven favicon_url > admin-uploaded logo > default favicon.
  const favicon = enterpriseSettings?.favicon_url
    ? enterpriseSettings.favicon_url
    : enterpriseSettings?.use_custom_logo
      ? `/api/enterprise-settings/logo?v=${cacheBuster}`
      : "/onyx.ico";

  return <link rel="icon" href={favicon} />;
}
