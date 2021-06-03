import React, { Children, PropsWithChildren } from "react";

// TODO: Figure out a better way to keep this in sync w/ python
export type StackLayoutProps = PropsWithChildren<{
  direction: "horizontal" | "vertical";
  spacing: number;
}>;

export default function StackLayout({
  direction,
  spacing,
  children,
}: StackLayoutProps) {
  const marginKey = `margin${direction === "horizontal" ? "Right" : "Bottom"}`;
  const len = Children.count(children);
  return (
    <div
      style={{
        display: "flex",
        flexDirection: direction === "horizontal" ? "row" : "column",
      }}
    >
      {Children.map(children, (child, i) => (
        <div key={i} style={{ [marginKey]: i == len - 1 ? 0 : spacing }}>
          {child}
        </div>
      ))}
    </div>
  );
}
