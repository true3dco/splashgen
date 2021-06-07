import { ReactElement } from "react";
import StackLayout from "../layouts/StackLayout";

export interface CTABarProps {
  primary: ReactElement;
  secondary: ReactElement;
}

export default function CTABar({ primary, secondary }: CTABarProps) {
  return (
    <StackLayout direction="horizontal" className="py-4">
      {primary}
      {secondary}
    </StackLayout>
  );
}
