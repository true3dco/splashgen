import { PropsWithChildren } from "react";
import StackLayout from "./StackLayout";

export default function CenteredHeroLayout({
  children,
}: PropsWithChildren<{}>) {
  return (
    <div className="col-lg-6 mx-auto text-center">
      <StackLayout direction="vertical" alignx="center">
        {children}
      </StackLayout>
    </div>
  );
}
