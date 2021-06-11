import { PropsWithChildren, createContext, Context, useContext } from "react";

export interface Branding {
  name: string;
  logo: string;
  theme: "light" | "dark";
}

export interface BrandingProviderProps {
  branding: Branding;
}

const BrandingContext: Context<Branding | null> = createContext(
  null as Branding | null
);
export function BrandingProvider({
  branding,
  children,
}: PropsWithChildren<BrandingProviderProps>) {
  return (
    <BrandingContext.Provider value={branding}>
      {children}
    </BrandingContext.Provider>
  );
}

export function useBranding(): Branding {
  const ctx = useContext(BrandingContext);
  if (!ctx) {
    throw new Error(
      "Failed to find BrandingProvider. This is an error of the framework; please report it."
    );
  }
  return ctx;
}
